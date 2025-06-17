"""
AQI 預測系統 - 統一時間窗口生成模組
支援5種標準化訓練模式的統一時間窗口生成
"""

import numpy as np
import torch
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
from sklearn.model_selection import train_test_split
import joblib

from .unified_config import UnifiedConfig

# 為了向後兼容，也導入ConfigManager
try:
    from .config_manager import ConfigManager
except ImportError:
    ConfigManager = None

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UnifiedWindowGenerator:
    """統一時間窗口生成器"""
    
    def __init__(self, config: UnifiedConfig):
        self.config = config
        self.X_windows = None
        self.y_windows = None
        self.metadata = None
        
        # 設置日誌
        self.logger = self._setup_logger()
        
    def _setup_logger(self) -> logging.Logger:
        """設置專用日誌器"""
        logger = logging.getLogger(f"windows_{self.config.mode}_{self.config.station or 'global'}")
        logger.setLevel(logging.INFO)
        
        # 添加文件處理器
        log_path = self.config.get_output_paths()['log_file']
        handler = logging.FileHandler(log_path, encoding='utf-8', mode='a')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def load_processed_data(self) -> Dict:
        """載入預處理後的數據"""
        processed_path = self.config.get_output_paths()['processed_data']
        
        if not processed_path.exists():
            raise FileNotFoundError(f"預處理數據不存在: {processed_path}")
        
        self.logger.info(f"載入預處理數據: {processed_path}")
        
        data = np.load(processed_path, allow_pickle=True)
        
        # 轉換為字典格式
        data_dict = {
            'X': data['X'],
            'y': data['y'], 
            'dates': data['dates'],
            'metadata': data['metadata'].item()
        }
        
        if 'stations' in data:
            data_dict['stations'] = data['stations']
        
        self.metadata = data_dict['metadata']
        self.logger.info(f"數據載入完成: X={data_dict['X'].shape}, y={data_dict['y'].shape}")
        
        return data_dict
    
    def create_sliding_windows(self, data_dict: Dict) -> Tuple[np.ndarray, np.ndarray]:
        """創建滑動時間窗口"""
        self.logger.info("開始創建滑動時間窗口")
        
        X = data_dict['X']
        y = data_dict['y']
        
        window_size = self.config.time_config.window_size
        horizon = self.config.time_config.horizon
        stride = self.config.time_config.stride
        
        self.logger.info(f"窗口參數: window_size={window_size}, horizon={horizon}, stride={stride}")
        
        # 處理多測站數據
        if 'stations' in data_dict:
            return self._create_windows_multi_station(data_dict)
        else:
            return self._create_windows_single_series(X, y, window_size, horizon, stride)
    
    def _create_windows_single_series(self, X: np.ndarray, y: np.ndarray, 
                                     window_size: int, horizon: int, stride: int) -> Tuple[np.ndarray, np.ndarray]:
        """為單一時間序列創建窗口"""
        n_samples, n_features = X.shape
        n_targets = y.shape[1]
        
        # 計算可以創建的窗口數量
        max_start = n_samples - window_size - horizon + 1
        n_windows = max(0, (max_start - 1) // stride + 1)
        
        if n_windows == 0:
            raise ValueError(f"數據長度不足以創建窗口: 需要至少 {window_size + horizon} 個樣本，實際 {n_samples}")
        
        # 初始化窗口數組
        X_windows = np.zeros((n_windows, window_size, n_features))
        y_windows = np.zeros((n_windows, horizon, n_targets))
        
        # 創建窗口
        for i in range(n_windows):
            start_idx = i * stride
            end_idx = start_idx + window_size
            target_start = end_idx
            target_end = target_start + horizon
            
            X_windows[i] = X[start_idx:end_idx]
            y_windows[i] = y[target_start:target_end]
        
        self.logger.info(f"單序列窗口創建完成: {n_windows} 個窗口")
        return X_windows, y_windows
    
    def _create_windows_multi_station(self, data_dict: Dict) -> Tuple[np.ndarray, np.ndarray]:
        """為多測站數據創建窗口"""
        X = data_dict['X']
        y = data_dict['y']
        stations = data_dict['stations']
        
        window_size = self.config.time_config.window_size
        horizon = self.config.time_config.horizon
        stride = self.config.time_config.stride
        
        # 按測站分組
        unique_stations = np.unique(stations)
        all_X_windows = []
        all_y_windows = []
        
        self.logger.info(f"處理 {len(unique_stations)} 個測站的數據")
        
        for station in unique_stations:
            station_mask = stations == station
            station_X = X[station_mask]
            station_y = y[station_mask]
            
            try:
                station_X_windows, station_y_windows = self._create_windows_single_series(
                    station_X, station_y, window_size, horizon, stride
                )
                all_X_windows.append(station_X_windows)
                all_y_windows.append(station_y_windows)
                
                self.logger.info(f"測站 {station}: {station_X_windows.shape[0]} 個窗口")
                
            except ValueError as e:
                self.logger.warning(f"測站 {station} 數據不足，跳過: {e}")
                continue
        
        if not all_X_windows:
            raise ValueError("所有測站數據都不足以創建窗口")
        
        # 合併所有測站的窗口
        X_windows = np.concatenate(all_X_windows, axis=0)
        y_windows = np.concatenate(all_y_windows, axis=0)
        
        self.logger.info(f"多測站窗口創建完成: 總計 {X_windows.shape[0]} 個窗口")
        return X_windows, y_windows
    
    def split_data(self, X_windows: np.ndarray, y_windows: np.ndarray) -> Dict[str, Dict[str, np.ndarray]]:
        """分割數據為訓練、驗證、測試集"""
        self.logger.info("開始分割數據集")
        
        train_ratio = self.config.time_config.train_ratio
        val_ratio = self.config.time_config.val_ratio
        test_ratio = self.config.time_config.test_ratio
        
        n_samples = X_windows.shape[0]
        
        # 計算分割點（時間序列分割，不打亂）
        train_end = int(n_samples * train_ratio)
        val_end = int(n_samples * (train_ratio + val_ratio))
        
        # 分割數據
        splits = {
            'train': {
                'X': X_windows[:train_end],
                'y': y_windows[:train_end]
            },
            'val': {
                'X': X_windows[train_end:val_end],
                'y': y_windows[train_end:val_end]
            },
            'test': {
                'X': X_windows[val_end:],
                'y': y_windows[val_end:]
            }
        }
        
        # 記錄分割結果
        for split_name, split_data in splits.items():
            self.logger.info(f"{split_name}: X={split_data['X'].shape}, y={split_data['y'].shape}")
        
        return splits
    
    def save_numpy_format(self, splits: Dict, X_windows: np.ndarray, y_windows: np.ndarray) -> None:
        """保存為NumPy格式（用於LightGBM）"""
        output_path = self.config.get_output_paths()['windows_data_npz']
        
        # 準備保存的數據
        save_dict = {
            'X_train': splits['train']['X'],
            'y_train': splits['train']['y'],
            'X_val': splits['val']['X'],
            'y_val': splits['val']['y'],
            'X_test': splits['test']['X'],
            'y_test': splits['test']['y'],
            'X_full': X_windows,
            'y_full': y_windows,
            'metadata': self.metadata
        }
        
        # 更新元數據
        save_dict['metadata'].update({
            'window_size': self.config.time_config.window_size,
            'horizon': self.config.time_config.horizon,
            'stride': self.config.time_config.stride,
            'train_samples': splits['train']['X'].shape[0],
            'val_samples': splits['val']['X'].shape[0],
            'test_samples': splits['test']['X'].shape[0],
            'total_windows': X_windows.shape[0]
        })
        
        np.savez_compressed(output_path, **save_dict)
        self.logger.info(f"NumPy格式數據已保存: {output_path}")
    
    def save_pytorch_format(self, splits: Dict, X_windows: np.ndarray, y_windows: np.ndarray) -> None:
        """保存為PyTorch格式（用於LSTM）"""
        output_path = self.config.get_output_paths()['windows_data_pt']
        
        # 轉換為PyTorch張量
        torch_splits = {}
        for split_name, split_data in splits.items():
            torch_splits[split_name] = {
                'X': torch.FloatTensor(split_data['X']),
                'y': torch.FloatTensor(split_data['y'])
            }
        
        # 準備保存的數據
        save_dict = {
            'train': torch_splits['train'],
            'val': torch_splits['val'],
            'test': torch_splits['test'],
            'X_full': torch.FloatTensor(X_windows),
            'y_full': torch.FloatTensor(y_windows),
            'metadata': self.metadata.copy()
        }
        
        # 更新元數據
        save_dict['metadata'].update({
            'window_size': self.config.time_config.window_size,
            'horizon': self.config.time_config.horizon,
            'stride': self.config.time_config.stride,
            'train_samples': splits['train']['X'].shape[0],
            'val_samples': splits['val']['X'].shape[0],
            'test_samples': splits['test']['X'].shape[0],
            'total_windows': X_windows.shape[0]
        })
        
        torch.save(save_dict, output_path)
        self.logger.info(f"PyTorch格式數據已保存: {output_path}")
    
    def process_full_pipeline(self) -> str:
        """執行完整的窗口生成管道"""
        try:
            self.logger.info("=" * 50)
            self.logger.info(f"開始執行 {self.config.mode} 模式的時間窗口生成")
            self.logger.info("=" * 50)
            
            # 1. 載入預處理數據
            data_dict = self.load_processed_data()
            
            # 2. 創建滑動窗口
            X_windows, y_windows = self.create_sliding_windows(data_dict)
            
            # 3. 分割數據
            splits = self.split_data(X_windows, y_windows)
            
            # 4. 保存NumPy格式
            self.save_numpy_format(splits, X_windows, y_windows)
            
            # 5. 保存PyTorch格式
            self.save_pytorch_format(splits, X_windows, y_windows)
            
            # 6. 生成摘要報告
            summary = self._generate_summary(X_windows, y_windows, splits)
            
            self.logger.info("時間窗口生成管道執行完成")
            return summary
            
        except Exception as e:
            self.logger.error(f"時間窗口生成管道執行失敗: {e}")
            raise
    
    def _generate_summary(self, X_windows: np.ndarray, y_windows: np.ndarray, 
                         splits: Dict) -> str:
        """生成處理摘要"""
        summary = f"""
時間窗口生成摘要報告
====================

模式: {self.config.mode}
測站: {self.config.station or '全部'}
時間戳: {self.config.timestamp}

窗口參數:
- 輸入窗口大小: {self.config.time_config.window_size} 小時
- 預測時間範圍: {self.config.time_config.horizon} 小時
- 滑動步長: {self.config.time_config.stride}

數據形狀:
- 輸入特徵: {X_windows.shape}
- 輸出目標: {y_windows.shape}

數據分割:
- 訓練集: {splits['train']['X'].shape[0]} 個窗口 ({self.config.time_config.train_ratio:.1%})
- 驗證集: {splits['val']['X'].shape[0]} 個窗口 ({self.config.time_config.val_ratio:.1%})
- 測試集: {splits['test']['X'].shape[0]} 個窗口 ({self.config.time_config.test_ratio:.1%})

輸出檔案:
- NumPy格式: {self.config.get_output_paths()['windows_data_npz']}
- PyTorch格式: {self.config.get_output_paths()['windows_data_pt']}
"""
        return summary

# === 便利函數 ===
def generate_windows_by_mode(mode: str, station: Optional[str] = None,
                            custom_config: Optional["ConfigManager"] = None) -> str:
    """按模式生成時間窗口的便利函數"""
    if custom_config is None:
        from .config_manager import ConfigManager
        config = ConfigManager(pipeline_mode=mode, station=station)
    else:
        config = custom_config
    
    generator = UnifiedWindowGenerator(config)
    return generator.process_full_pipeline()

def batch_generate_windows(modes: List[str], stations: Optional[List[str]] = None) -> Dict[str, str]:
    """批量生成時間窗口"""
    results = {}
    
    for mode in modes:
        if mode in ['separate', 'separate_norm', 'station_specific'] and stations:
            for station in stations:
                key = f"{mode}_{station}"
                try:
                    results[key] = generate_windows_by_mode(mode, station)
                except Exception as e:
                    results[key] = f"失敗: {e}"
        else:
            try:
                results[mode] = generate_windows_by_mode(mode)
            except Exception as e:
                results[mode] = f"失敗: {e}"
    
    return results

# === 數據載入工具 ===
def load_windows_data(mode: str, station: Optional[str] = None, 
                     format_type: str = 'numpy') -> Dict:
    """載入時間窗口數據"""
    from .config_manager import ConfigManager
    config = ConfigManager(pipeline_mode=mode, station=station)
    
    if format_type == 'numpy':
        data_path = config.get_output_paths()['windows_data_npz']
        if not data_path.exists():
            raise FileNotFoundError(f"NumPy數據文件不存在: {data_path}")
        return dict(np.load(data_path, allow_pickle=True))
    
    elif format_type == 'pytorch':
        data_path = config.get_output_paths()['windows_data_pt']
        if not data_path.exists():
            raise FileNotFoundError(f"PyTorch數據文件不存在: {data_path}")
        return torch.load(data_path, weights_only=False)
    
    else:
        raise ValueError(f"不支援的格式類型: {format_type}. 支援: 'numpy', 'pytorch'") 