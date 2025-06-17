"""
AQI 預測系統 - 統一數據預處理模組
支援5種標準化訓練模式的統一數據預處理
"""

import pandas as pd
import numpy as np
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import joblib

from .unified_config import UnifiedConfig, TimeConfig
from .utils.time_features import add_time_features
from .utils.io import load_data, save_data

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UnifiedPreprocessor:
    """統一數據預處理器"""
    
    def __init__(self, config: UnifiedConfig):
        self.config = config
        self.scaler = None
        self.feature_columns = None
        self.target_columns = None
        self.station_info = {}
        
        # 設置日誌
        self.logger = self._setup_logger()
        
    def _setup_logger(self) -> logging.Logger:
        """設置專用日誌器"""
        logger = logging.getLogger(f"preprocessor_{self.config.mode}_{self.config.station or 'global'}")
        logger.setLevel(logging.INFO)
        
        # 添加文件處理器
        log_path = self.config.get_output_paths()['log_file']
        handler = logging.FileHandler(log_path, encoding='utf-8')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def load_raw_data(self) -> pd.DataFrame:
        """載入原始數據"""
        self.logger.info(f"開始載入 {self.config.mode} 模式的原始數據")
        
        input_paths = self.config.get_input_paths()
        
        if isinstance(input_paths, Path):
            # 單一文件模式（combine, combine_norm）
            self.logger.info(f"載入單一文件: {input_paths}")
            df = pd.read_csv(input_paths)
            
        elif isinstance(input_paths, list):
            # 多文件模式（separate, separate_norm, station_specific）
            if not input_paths:
                raise ValueError(f"未找到匹配的數據文件: {self.config.mode}, station: {self.config.station}")
            
            dataframes = []
            for path in input_paths:
                self.logger.info(f"載入文件: {path}")
                df_temp = pd.read_csv(path)
                
                # 添加測站信息
                station_name = self._extract_station_name(path)
                df_temp['station'] = station_name
                dataframes.append(df_temp)
                
                # 記錄測站信息
                self.station_info[station_name] = {
                    'file_path': str(path),
                    'record_count': len(df_temp),
                    'is_normalized': 'Nomorlization' in str(path)
                }
            
            # 合併所有數據
            df = pd.concat(dataframes, ignore_index=True)
            self.logger.info(f"合併 {len(dataframes)} 個文件，總記錄數: {len(df)}")
            
        else:
            raise ValueError(f"無效的輸入路徑類型: {type(input_paths)}")
        
        # 基本數據驗證
        self._validate_raw_data(df)
        
        self.logger.info(f"原始數據載入完成: {df.shape}")
        return df
    
    def _extract_station_name(self, file_path: Path) -> str:
        """從文件路徑提取測站名稱"""
        filename = file_path.stem  # 去除副檔名
        
        # 修復：處理不同的檔名格式
        if "Nomorlization" in str(file_path):
            # Nomorlization檔名格式：Nomorlization_站名_代碼_combined
            parts = filename.split('_')
            if len(parts) >= 3 and parts[0] == "Nomorlization":
                return parts[1]  # 站名在第二個位置
        
        # 標準格式：站名_代碼_combined 或其他格式
        parts = filename.split('_')
        if parts:
            return parts[0]  # 站名在第一個位置
        
        # 回退：使用整個檔名（去除combined後綴）
        return filename.replace('_combined', '')
    
    def _validate_raw_data(self, df: pd.DataFrame) -> None:
        """驗證原始數據"""
        required_columns = ['date']  # 最基本的必需列
        
        missing_cols = set(required_columns) - set(df.columns)
        if missing_cols:
            raise ValueError(f"缺少必需的列: {missing_cols}")
        
        # 檢查數據完整性
        if df.empty:
            raise ValueError("數據為空")
        
        # 檢查時間列
        if 'date' in df.columns:
            try:
                pd.to_datetime(df['date'])
            except Exception as e:
                raise ValueError(f"時間列格式錯誤: {e}")
        
        self.logger.info(f"數據驗證通過: {df.shape}, 時間範圍: {df['date'].min()} 到 {df['date'].max()}")
    
    def preprocess_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """預處理數據"""
        self.logger.info("開始數據預處理")
        
        # 1. 時間處理
        df = self._process_datetime(df)
        
        # 2. 特徵工程
        df = self._feature_engineering(df)
        
        # 3. 數據清理
        df = self._clean_data(df)
        
        # 4. 特徵選擇
        df = self._select_features(df)
        
        # 5. 數據標準化（如果需要）
        if self._needs_scaling():
            df = self._scale_data(df)
        
        self.logger.info(f"數據預處理完成: {df.shape}")
        return df
    
    def _process_datetime(self, df: pd.DataFrame) -> pd.DataFrame:
        """處理時間相關特徵"""
        # 使用新的時間特徵處理邏輯
        df = self.process_time_features(df)
        
        # 排序
        df = df.sort_values('date').reset_index(drop=True)
        
        return df
    
    def _feature_engineering(self, df: pd.DataFrame) -> pd.DataFrame:
        """特徵工程"""
        self.logger.info("執行特徵工程")
        
        # 識別數值列
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        # 移除時間和標識列
        exclude_cols = ['date', 'station'] if 'station' in df.columns else ['date']
        numeric_cols = [col for col in numeric_cols if col not in exclude_cols]
        
        # 創建滯後特徵（前1-3小時）
        for lag in [1, 2, 3]:
            for col in numeric_cols[:10]:  # 限制特徵數量
                if col.startswith('AQI_'):
                    df[f'{col}_lag_{lag}'] = df[col].shift(lag)
        
        # 創建滾動統計特徵
        window_sizes = [6, 12, 24]  # 6小時, 12小時, 24小時
        for window in window_sizes:
            for col in numeric_cols[:5]:  # 主要污染物
                if col.startswith('AQI_'):
                    df[f'{col}_mean_{window}h'] = df[col].rolling(window=window, min_periods=1).mean()
                    df[f'{col}_std_{window}h'] = df[col].rolling(window=window, min_periods=1).std()
        
        # 創建交互特徵
        if 'AQI_pm2.5' in df.columns and 'AQI_pm10' in df.columns:
            df['pm_ratio'] = df['AQI_pm2.5'] / (df['AQI_pm10'] + 1e-8)
        
        if 'AQI_o3' in df.columns and 'AQI_no2' in df.columns:
            df['o3_no2_ratio'] = df['AQI_o3'] / (df['AQI_no2'] + 1e-8)
        
        return df
    
    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """數據清理"""
        self.logger.info("執行數據清理")
        
        initial_count = len(df)
        
        # 處理異常值
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if col.startswith('AQI_'):
                # 移除明顯異常的值
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 3 * IQR
                upper_bound = Q3 + 3 * IQR
                
                outlier_mask = (df[col] < lower_bound) | (df[col] > upper_bound)
                df.loc[outlier_mask, col] = np.nan
        
        # 處理缺失值
        # 對於數值列，使用前向填充 + 後向填充
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df[numeric_cols].fillna(method='ffill').fillna(method='bfill')
        
        # 移除仍有缺失值的行
        before_drop = len(df)
        df = df.dropna()
        after_drop = len(df)
        
        if before_drop != after_drop:
            self.logger.warning(f"移除 {before_drop - after_drop} 行包含缺失值的數據")
        
        self.logger.info(f"數據清理完成: {initial_count} -> {len(df)} 行")
        return df
    
    def _select_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """特徵選擇"""
        self.logger.info("執行特徵選擇")
        
        # 識別特徵列和目標列
        feature_cols = []
        target_cols = []
        
        for col in df.columns:
            if col in ['date', 'station']:
                continue
            elif col.startswith('AQI_'):
                if not any(suffix in col for suffix in ['_lag_', '_mean_', '_std_']):
                    target_cols.append(col)
                else:
                    feature_cols.append(col)
            elif col.startswith(('Weather_', 'month_', 'hour_', 'day_', 'pm_', 'o3_')):
                feature_cols.append(col)
        
        # 保存列信息
        self.feature_columns = feature_cols
        self.target_columns = target_cols
        
        # 選擇最終的列
        keep_cols = ['date'] + feature_cols + target_cols
        if 'station' in df.columns:
            keep_cols.append('station')
        
        df = df[keep_cols]
        
        self.logger.info(f"特徵選擇完成: {len(feature_cols)} 個特徵, {len(target_cols)} 個目標")
        return df
    
    def _needs_scaling(self) -> bool:
        """判斷是否需要標準化"""
        # 如果原始數據已經是標準化的，則不需要再次標準化
        return not self.config.pipeline_config.is_normalized
    
    def _scale_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """數據標準化"""
        self.logger.info("執行數據標準化")
        
        if not self.feature_columns:
            return df
        
        # 初始化標準化器
        self.scaler = StandardScaler()
        
        # 只對特徵列進行標準化
        scaled_features = self.scaler.fit_transform(df[self.feature_columns])
        
        # 更新數據
        for i, col in enumerate(self.feature_columns):
            df[col] = scaled_features[:, i]
        
        # 保存標準化器
        scaler_path = self.config.get_output_paths()['processed_data'].parent / f"{self.config.mode}_scaler.pkl"
        joblib.dump(self.scaler, scaler_path)
        self.logger.info(f"標準化器已保存: {scaler_path}")
        
        return df
    
    def save_processed_data(self, df: pd.DataFrame) -> None:
        """保存處理後的數據"""
        output_path = self.config.get_output_paths()['processed_data']
        
        # 分離特徵和目標
        X = df[self.feature_columns].values
        y = df[self.target_columns].values
        dates = df['date'].values
        
        # 準備元數據
        metadata = {
            'feature_columns': self.feature_columns,
            'target_columns': self.target_columns,
            'mode': self.config.mode,
            'station': self.config.station,
            'timestamp': self.config.timestamp,
            'station_info': self.station_info,
            'config': self.config.to_dict()
        }
        
        if 'station' in df.columns:
            stations = df['station'].values
            metadata['stations'] = list(df['station'].unique())
        else:
            stations = None
        
        # 保存數據
        save_data_dict = {
            'X': X,
            'y': y,
            'dates': dates,
            'metadata': metadata
        }
        
        if stations is not None:
            save_data_dict['stations'] = stations
        
        np.savez_compressed(output_path, **save_data_dict)
        
        self.logger.info(f"處理後數據已保存: {output_path}")
        self.logger.info(f"數據形狀: X={X.shape}, y={y.shape}")
        
    def process_full_pipeline(self) -> str:
        """執行完整的預處理管道"""
        try:
            self.logger.info("=" * 50)
            self.logger.info(f"開始執行 {self.config.mode} 模式的完整預處理管道")
            self.logger.info("=" * 50)
            
            # 1. 載入原始數據
            raw_df = self.load_raw_data()
            
            # 2. 預處理數據
            processed_df = self.preprocess_data(raw_df)
            
            # 3. 保存處理後的數據
            self.save_processed_data(processed_df)
            
            # 4. 生成摘要報告
            summary = self._generate_summary(raw_df, processed_df)
            
            self.logger.info("預處理管道執行完成")
            return summary
            
        except Exception as e:
            self.logger.error(f"預處理管道執行失敗: {e}")
            raise
    
    def _generate_summary(self, raw_df: pd.DataFrame, processed_df: pd.DataFrame) -> str:
        """生成處理摘要"""
        summary = f"""
數據預處理摘要報告
==================

模式: {self.config.mode}
測站: {self.config.station or '全部'}
時間戳: {self.config.timestamp}

原始數據:
- 形狀: {raw_df.shape}
- 時間範圍: {raw_df['date'].min()} 到 {raw_df['date'].max()}

處理後數據:
- 形狀: {processed_df.shape}
- 特徵數量: {len(self.feature_columns)}
- 目標數量: {len(self.target_columns)}
- 標準化: {'是' if self._needs_scaling() else '否'}

測站信息: {len(self.station_info)} 個測站
輸出路徑: {self.config.get_output_paths()['processed_data']}
"""
        return summary

    def process_time_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """處理時間特徵"""
        self.logger.info("處理時間特徵")
        
        # 檢查是否已包含時間特徵（針對標準化數據）
        time_features = ['month_sin', 'hour_sin', 'day_sin']
        has_time_features = all(col in df.columns for col in time_features)
        
        if has_time_features and self.config.pipeline_config.is_normalized:
            self.logger.info("數據已包含時間特徵，跳過時間特徵處理")
            return df
        
        df = df.copy()
        
        # 確保date欄位存在且為datetime類型
        if 'date' not in df.columns:
            raise ValueError("數據中缺少必要的'date'欄位")
        
        df['date'] = pd.to_datetime(df['date'], utc=True)
        
        # 只在必要時創建時間特徵
        if not has_time_features:
            # 提取時間組件
            df['year'] = df['date'].dt.year
            df['month'] = df['date'].dt.month
            df['day'] = df['date'].dt.day
            df['hour'] = df['date'].dt.hour
            df['dayofweek'] = df['date'].dt.dayofweek
            df['dayofyear'] = df['date'].dt.dayofyear
            
            # 創建循環特徵（正弦/餘弦編碼）
            df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
            df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)
            df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
            df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
            df['day_sin'] = np.sin(2 * np.pi * df['day'] / 31)
            df['day_cos'] = np.cos(2 * np.pi * df['day'] / 31)
            df['dayofweek_sin'] = np.sin(2 * np.pi * df['dayofweek'] / 7)
            df['dayofweek_cos'] = np.cos(2 * np.pi * df['dayofweek'] / 7)
            
            self.logger.info(f"創建了時間特徵，數據形狀: {df.shape}")
        else:
            self.logger.info(f"保留現有時間特徵，數據形狀: {df.shape}")
        
        return df

# === 便利函數 ===
def preprocess_data_by_mode(mode: str, station: Optional[str] = None, 
                           custom_config: Optional[UnifiedConfig] = None) -> str:
    """按模式預處理數據的便利函數"""
    if custom_config is None:
        config = UnifiedConfig(mode=mode, station=station)
    else:
        config = custom_config
    
    preprocessor = UnifiedPreprocessor(config)
    return preprocessor.process_full_pipeline()

def batch_preprocess(modes: List[str], stations: Optional[List[str]] = None) -> Dict[str, str]:
    """批量預處理數據"""
    results = {}
    
    for mode in modes:
        if mode in ['separate', 'separate_norm', 'station_specific'] and stations:
            for station in stations:
                key = f"{mode}_{station}"
                try:
                    results[key] = preprocess_data_by_mode(mode, station)
                except Exception as e:
                    results[key] = f"失敗: {e}"
        else:
            try:
                results[mode] = preprocess_data_by_mode(mode)
            except Exception as e:
                results[mode] = f"失敗: {e}"
    
    return results 