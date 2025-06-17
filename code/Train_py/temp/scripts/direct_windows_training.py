#!/usr/bin/env python3
"""
直接使用已有預處理文件進行時間窗口生成和模型訓練
跳過路徑問題，直接處理現有數據
"""

import os
import sys
import numpy as np
import torch
import lightgbm as lgb
import logging
from pathlib import Path
from typing import List, Dict, Tuple
from datetime import datetime
import glob
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error

# 添加項目根目錄到Python路徑
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 設置日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(f'direct_windows_training_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

class DirectProcessor:
    """直接處理器，處理預處理數據到模型訓練"""
    
    def __init__(self):
        self.processed_dir = Path("data/processed")
        self.windows_dir = Path("data/sliding_windows")
        self.models_dir = Path("models")
        self.reports_dir = Path("reports")
        
        # 確保目錄存在
        for dir_path in [self.windows_dir, self.models_dir, self.reports_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def detect_processed_files(self) -> List[Path]:
        """檢測所有已預處理的文件"""
        pattern = "separate_*_*_processed.npz"
        files = list(self.processed_dir.glob(pattern))
        logger.info(f"檢測到 {len(files)} 個預處理文件")
        return sorted(files, key=lambda f: f.stat().st_mtime, reverse=True)
    
    def extract_station_info(self, file_path: Path) -> Tuple[str, str]:
        """從文件名提取測站和時間戳信息"""
        # 文件名格式: separate_測站名_時間戳_processed.npz
        parts = file_path.stem.split('_')
        if len(parts) >= 4:
            station = '_'.join(parts[1:-2])  # 測站名可能包含下劃線
            timestamp = parts[-2]  # 時間戳
            return station, timestamp
        else:
            raise ValueError(f"無法解析文件名: {file_path}")
    
    def load_processed_data(self, file_path: Path) -> Dict:
        """載入預處理數據"""
        logger.info(f"載入預處理數據: {file_path}")
        
        data = np.load(file_path, allow_pickle=True)
        
        data_dict = {
            'X': data['X'],
            'y': data['y'],
            'dates': data['dates'],
            'metadata': data['metadata'].item()
        }
        
        logger.info(f"數據載入完成: X={data_dict['X'].shape}, y={data_dict['y'].shape}")
        return data_dict
    
    def create_sliding_windows(self, X: np.ndarray, y: np.ndarray, 
                              window_size: int = 24, horizon: int = 6, stride: int = 1) -> Tuple[np.ndarray, np.ndarray]:
        """創建滑動時間窗口"""
        logger.info(f"創建滑動窗口: window_size={window_size}, horizon={horizon}, stride={stride}")
        
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
        
        logger.info(f"窗口創建完成: {n_windows} 個窗口")
        return X_windows, y_windows
    
    def split_data(self, X_windows: np.ndarray, y_windows: np.ndarray, 
                   train_ratio: float = 0.8, val_ratio: float = 0.1) -> Dict:
        """分割數據為訓練、驗證、測試集"""
        n_samples = X_windows.shape[0]
        
        # 計算分割點
        train_end = int(n_samples * train_ratio)
        val_end = int(n_samples * (train_ratio + val_ratio))
        
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
        
        logger.info(f"數據分割完成: train={splits['train']['X'].shape[0]}, "
                   f"val={splits['val']['X'].shape[0]}, test={splits['test']['X'].shape[0]}")
        
        return splits
    
    def save_windows_data(self, splits: Dict, station: str, timestamp: str) -> Path:
        """保存窗口數據"""
        output_path = self.windows_dir / f"separate_{station}_{timestamp}_windows.npz"
        
        np.savez_compressed(
            output_path,
            X_train=splits['train']['X'],
            y_train=splits['train']['y'],
            X_val=splits['val']['X'],
            y_val=splits['val']['y'],
            X_test=splits['test']['X'],
            y_test=splits['test']['y']
        )
        
        logger.info(f"窗口數據已保存: {output_path}")
        return output_path
    
    def reshape_for_lgbm(self, X_windows: np.ndarray) -> np.ndarray:
        """為LightGBM重新塑造數據"""
        # LightGBM需要2D數據 (n_samples, n_features)
        # 將窗口數據平展: (n_windows, window_size, n_features) -> (n_windows, window_size * n_features)
        n_windows, window_size, n_features = X_windows.shape
        return X_windows.reshape(n_windows, window_size * n_features)
    
    def train_lgbm_model(self, splits: Dict, station: str, timestamp: str) -> Path:
        """訓練LightGBM模型"""
        logger.info(f"開始訓練LightGBM模型: {station}")
        
        # 重新塑造數據
        X_train = self.reshape_for_lgbm(splits['train']['X'])
        X_val = self.reshape_for_lgbm(splits['val']['X'])
        
        # 取第一個時間步的目標值（簡化為單步預測）
        y_train = splits['train']['y'][:, 0, :]  # (n_samples, n_targets)
        y_val = splits['val']['y'][:, 0, :]
        
        # 平展目標值到1D（LightGBM一次只能預測一個目標）
        # 我們訓練多個模型，每個目標一個
        models = {}
        n_targets = y_train.shape[1]
        
        for target_idx in range(n_targets):
            logger.info(f"訓練目標 {target_idx + 1}/{n_targets}")
            
            # LightGBM參數
            params = {
                'objective': 'regression',
                'metric': 'mae',
                'boosting_type': 'gbdt',
                'num_leaves': 20,  # 輕量化
                'learning_rate': 0.1,
                'feature_fraction': 0.8,
                'bagging_fraction': 0.8,
                'bagging_freq': 5,
                'verbose': -1,
                'max_bin': 255,
                'min_data_in_leaf': 50,
                'n_estimators': 100,  # 輕量化
                'max_depth': 6,  # 輕量化
                'random_state': 42
            }
            
            # 訓練模型
            model = lgb.LGBMRegressor(**params)
            model.fit(
                X_train, y_train[:, target_idx],
                eval_set=[(X_val, y_val[:, target_idx])],
                callbacks=[lgb.early_stopping(50), lgb.log_evaluation(0)]
            )
            
            models[f'target_{target_idx}'] = model
        
        # 保存模型
        model_path = self.models_dir / f"separate_{station}_{timestamp}_lgbm.pkl"
        joblib.dump(models, model_path)
        
        logger.info(f"LightGBM模型已保存: {model_path}")
        return model_path
    
    def evaluate_model(self, model_path: Path, splits: Dict, station: str, timestamp: str) -> Dict:
        """評估模型性能"""
        logger.info(f"評估模型性能: {station}")
        
        # 載入模型
        models = joblib.load(model_path)
        
        # 準備測試數據
        X_test = self.reshape_for_lgbm(splits['test']['X'])
        y_test = splits['test']['y'][:, 0, :]  # 取第一個時間步
        
        # 進行預測
        predictions = {}
        metrics = {}
        
        for target_idx, (model_name, model) in enumerate(models.items()):
            y_pred = model.predict(X_test)
            y_true = y_test[:, target_idx]
            
            # 計算指標
            mae = mean_absolute_error(y_true, y_pred)
            rmse = np.sqrt(mean_squared_error(y_true, y_pred))
            mape = np.mean(np.abs((y_true - y_pred) / (y_true + 1e-8))) * 100
            
            predictions[model_name] = y_pred.tolist()
            metrics[model_name] = {
                'MAE': float(mae),
                'RMSE': float(rmse),
                'MAPE': float(mape)
            }
            
            logger.info(f"目標 {target_idx}: MAE={mae:.4f}, RMSE={rmse:.4f}, MAPE={mape:.2f}%")
        
        # 計算平均指標
        avg_metrics = {
            'MAE': np.mean([m['MAE'] for m in metrics.values()]),
            'RMSE': np.mean([m['RMSE'] for m in metrics.values()]),
            'MAPE': np.mean([m['MAPE'] for m in metrics.values()])
        }
        
        results = {
            'station': station,
            'timestamp': timestamp,
            'model_path': str(model_path),
            'individual_metrics': metrics,
            'average_metrics': avg_metrics,
            'predictions': predictions
        }
        
        # 保存評估結果
        import json
        results_path = self.reports_dir / f"separate_{station}_{timestamp}_evaluation.json"
        with open(results_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        logger.info(f"評估結果已保存: {results_path}")
        logger.info(f"平均性能: MAE={avg_metrics['MAE']:.4f}, RMSE={avg_metrics['RMSE']:.4f}, MAPE={avg_metrics['MAPE']:.2f}%")
        
        return results
    
    def process_single_station(self, file_path: Path) -> Dict:
        """處理單個測站的完整pipeline"""
        try:
            # 提取測站信息
            station, timestamp = self.extract_station_info(file_path)
            logger.info(f"開始處理測站: {station} (時間戳: {timestamp})")
            
            # 載入預處理數據
            data_dict = self.load_processed_data(file_path)
            
            # 創建滑動窗口
            X_windows, y_windows = self.create_sliding_windows(
                data_dict['X'], data_dict['y']
            )
            
            # 分割數據
            splits = self.split_data(X_windows, y_windows)
            
            # 保存窗口數據
            windows_path = self.save_windows_data(splits, station, timestamp)
            
            # 訓練模型
            model_path = self.train_lgbm_model(splits, station, timestamp)
            
            # 評估模型
            evaluation = self.evaluate_model(model_path, splits, station, timestamp)
            
            logger.info(f"✅ 測站 {station} 處理完成")
            return {
                'status': 'success',
                'station': station,
                'timestamp': timestamp,
                'windows_path': windows_path,
                'model_path': model_path,
                'evaluation': evaluation
            }
            
        except Exception as e:
            logger.error(f"❌ 處理測站失敗: {e}")
            return {
                'status': 'failed',
                'error': str(e),
                'file_path': str(file_path)
            }

def main():
    """主執行函數"""
    logger.info("🚀 開始直接處理所有測站的separate pipeline")
    
    processor = DirectProcessor()
    
    # 檢測所有預處理文件
    processed_files = processor.detect_processed_files()
    
    if not processed_files:
        logger.error("❌ 未找到任何預處理文件")
        return
    
    # 過濾掉norm文件，只處理原始separate文件
    original_files = [f for f in processed_files if 'norm_' not in f.name]
    logger.info(f"找到 {len(original_files)} 個原始separate預處理文件")
    
    # 統計結果
    results = []
    successful = 0
    failed = 0
    
    start_time = datetime.now()
    
    try:
        for i, file_path in enumerate(original_files, 1):
            logger.info(f"[{i}/{len(original_files)}] 處理文件: {file_path.name}")
            
            result = processor.process_single_station(file_path)
            results.append(result)
            
            if result['status'] == 'success':
                successful += 1
            else:
                failed += 1
        
        # 生成最終報告
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds()
        
        logger.info("=" * 80)
        logger.info("🎉 直接處理完成!")
        logger.info(f"⏱️  總執行時間: {execution_time:.2f} 秒")
        logger.info(f"📊 處理統計:")
        logger.info(f"  - 總文件數: {len(original_files)}")
        logger.info(f"  - 成功處理: {successful}")
        logger.info(f"  - 處理失敗: {failed}")
        logger.info(f"  - 成功率: {successful/len(original_files)*100:.1f}%")
        
        # 保存詳細結果
        import json
        summary = {
            'execution_info': {
                'start_time': start_time.isoformat(),
                'end_time': end_time.isoformat(),
                'execution_time': execution_time,
                'total_files': len(original_files),
                'successful': successful,
                'failed': failed
            },
            'detailed_results': results
        }
        
        output_file = f"direct_processing_results_{start_time.strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2, default=str)
        
        logger.info(f"📁 詳細結果已保存: {output_file}")
        logger.info("=" * 80)
        
    except Exception as e:
        logger.error(f"💥 執行過程中發生嚴重錯誤: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 