"""
AQI 預測系統 - 統一模型訓練模組
支援5種標準化訓練模式的統一模型訓練
"""

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import lightgbm as lgb
import pickle
import logging
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union, Any
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

from .unified_config import UnifiedConfig
from .unified_window_generator import load_windows_data
from .utils.metrics import calculate_mape, calculate_rmse

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LSTMModel(nn.Module):
    """LSTM模型"""
    
    def __init__(self, input_size: int, hidden_size: int, num_layers: int, 
                 output_size: int, dropout: float = 0.2):
        super(LSTMModel, self).__init__()
        
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        
        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            dropout=dropout if num_layers > 1 else 0,
            batch_first=True
        )
        
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(hidden_size, output_size)
        
    def forward(self, x):
        # x shape: (batch_size, seq_len, input_size)
        lstm_out, _ = self.lstm(x)
        
        # 取最後一個時間步的輸出
        lstm_out = lstm_out[:, -1, :]  # (batch_size, hidden_size)
        
        output = self.dropout(lstm_out)
        output = self.fc(output)  # (batch_size, output_size)
        
        return output

class UnifiedTrainer:
    """統一模型訓練器"""
    
    def __init__(self, config: UnifiedConfig):
        self.config = config
        self.lgbm_model = None
        self.lstm_model = None
        self.training_history = {}
        
        # 設置日誌
        self.logger = self._setup_logger()
        
        # 設置設備
        self.device = torch.device(config.performance_config.device)
        self.logger.info(f"使用設備: {self.device}")
        
    def _setup_logger(self) -> logging.Logger:
        """設置專用日誌器"""
        logger = logging.getLogger(f"trainer_{self.config.mode}_{self.config.station or 'global'}")
        logger.setLevel(logging.INFO)
        
        # 添加文件處理器
        log_path = self.config.get_output_paths()['log_file']
        handler = logging.FileHandler(log_path, encoding='utf-8', mode='a')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def load_training_data(self) -> Dict:
        """載入訓練數據"""
        self.logger.info("載入訓練數據")
        
        # 直接使用配置的路徑
        numpy_path = self.config.get_output_paths()['windows_data_npz']
        pytorch_path = self.config.get_output_paths()['windows_data_pt']
        
        # 載入NumPy格式數據（用於LightGBM）
        if not numpy_path.exists():
            raise FileNotFoundError(f"NumPy數據文件不存在: {numpy_path}")
        numpy_data = dict(np.load(numpy_path, allow_pickle=True))
        
        # 載入PyTorch格式數據（用於LSTM）
        if not pytorch_path.exists():
            raise FileNotFoundError(f"PyTorch數據文件不存在: {pytorch_path}")
        pytorch_data = torch.load(pytorch_path, weights_only=False)
        
        return {
            'numpy': numpy_data,
            'pytorch': pytorch_data
        }
    
    def train_lightgbm(self, data: Dict) -> Dict[str, Any]:
        """訓練LightGBM模型"""
        self.logger.info("開始訓練LightGBM模型")
        start_time = time.time()
        
        # 準備數據
        numpy_data = data['numpy']
        
        # 重塑數據為2D格式（LightGBM需要）
        X_train = numpy_data['X_train'].reshape(numpy_data['X_train'].shape[0], -1)
        y_train = numpy_data['y_train'].reshape(numpy_data['y_train'].shape[0], -1)
        X_val = numpy_data['X_val'].reshape(numpy_data['X_val'].shape[0], -1)
        y_val = numpy_data['y_val'].reshape(numpy_data['y_val'].shape[0], -1)
        
        # LightGBM需要1D標籤，所以我們訓練第一個目標列作為示例
        y_train_1d = y_train[:, 0]  # 使用第一個目標
        y_val_1d = y_val[:, 0]
        
        self.logger.info(f"LightGBM數據形狀: X_train={X_train.shape}, y_train={y_train.shape}")
        
        # 準備LightGBM參數
        lgbm_params = self.config.lgbm_config.__dict__.copy()
        
        # 移除非LightGBM參數
        lgbm_params.pop('random_state', None)
        lgbm_params.pop('early_stopping_rounds', None)
        
        # 創建數據集
        train_dataset = lgb.Dataset(X_train, label=y_train_1d)
        val_dataset = lgb.Dataset(X_val, label=y_val_1d, reference=train_dataset)
        
        # 訓練模型
        self.lgbm_model = lgb.train(
            lgbm_params,
            train_dataset,
            valid_sets=[train_dataset, val_dataset],
            valid_names=['train', 'val'],
            callbacks=[
                lgb.early_stopping(stopping_rounds=self.config.lgbm_config.early_stopping_rounds),
                lgb.log_evaluation(period=100)
            ]
        )
        
        training_time = time.time() - start_time
        
        # 評估模型
        train_pred = self.lgbm_model.predict(X_train)
        val_pred = self.lgbm_model.predict(X_val)
        
        # 計算指標（使用1D目標）
        train_metrics = self._calculate_metrics(y_train_1d, train_pred)
        val_metrics = self._calculate_metrics(y_val_1d, val_pred)
        
        # 保存模型
        model_path = self.config.get_output_paths()['lgbm_model']
        joblib.dump(self.lgbm_model, model_path)
        
        results = {
            'model_path': str(model_path),
            'training_time': training_time,
            'train_metrics': train_metrics,
            'val_metrics': val_metrics,
            'feature_importance': dict(zip(
                [f'feature_{i}' for i in range(X_train.shape[1])],
                self.lgbm_model.feature_importance()
            ))
        }
        
        self.logger.info(f"LightGBM訓練完成: {training_time:.2f}s")
        self.logger.info(f"驗證集MAE: {val_metrics['mae']:.4f}")
        
        return results
    
    def train_lstm(self, data: Dict) -> Dict[str, Any]:
        """訓練LSTM模型"""
        self.logger.info("開始訓練LSTM模型")
        start_time = time.time()
        
        # 準備數據
        pytorch_data = data['pytorch']
        
        X_train = pytorch_data['train']['X'].to(self.device)
        y_train = pytorch_data['train']['y'].to(self.device)
        X_val = pytorch_data['val']['X'].to(self.device)
        y_val = pytorch_data['val']['y'].to(self.device)
        
        self.logger.info(f"LSTM數據形狀: X_train={X_train.shape}, y_train={y_train.shape}")
        
        # 準備數據加載器
        train_dataset = TensorDataset(X_train, y_train.view(y_train.size(0), -1))  # 展平y
        val_dataset = TensorDataset(X_val, y_val.view(y_val.size(0), -1))
        
        train_loader = DataLoader(
            train_dataset,
            batch_size=self.config.lstm_config.batch_size,
            shuffle=True,
            num_workers=0,  # 在CUDA上時設為0避免多進程問題
            pin_memory=False  # 數據已經在CUDA上，不需要pin_memory
        )
        
        val_loader = DataLoader(
            val_dataset,
            batch_size=self.config.lstm_config.batch_size,
            shuffle=False,
            num_workers=0,  # 在CUDA上時設為0避免多進程問題
            pin_memory=False  # 數據已經在CUDA上，不需要pin_memory
        )
        
        # 創建模型
        input_size = X_train.size(-1)
        output_size = y_train.view(y_train.size(0), -1).size(-1)
        
        self.lstm_model = LSTMModel(
            input_size=input_size,
            hidden_size=self.config.lstm_config.hidden_size,
            num_layers=self.config.lstm_config.num_layers,
            output_size=output_size,
            dropout=self.config.lstm_config.dropout
        ).to(self.device)
        
        # 優化器和損失函數
        optimizer = optim.Adam(
            self.lstm_model.parameters(),
            lr=self.config.lstm_config.learning_rate,
            weight_decay=self.config.lstm_config.weight_decay
        )
        
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(
            optimizer,
            mode='min',
            factor=self.config.lstm_config.scheduler_factor,
            patience=self.config.lstm_config.scheduler_patience
        )
        
        criterion = nn.MSELoss()
        
        # 訓練循環
        best_val_loss = float('inf')
        patience_counter = 0
        training_history = {'train_loss': [], 'val_loss': []}
        
        for epoch in range(self.config.lstm_config.epochs):
            # 訓練階段
            self.lstm_model.train()
            train_loss = 0.0
            
            for batch_X, batch_y in train_loader:
                optimizer.zero_grad()
                
                outputs = self.lstm_model(batch_X)
                loss = criterion(outputs, batch_y)
                
                loss.backward()
                
                # 梯度裁剪
                torch.nn.utils.clip_grad_norm_(
                    self.lstm_model.parameters(),
                    self.config.lstm_config.grad_clip
                )
                
                optimizer.step()
                train_loss += loss.item()
            
            # 驗證階段
            self.lstm_model.eval()
            val_loss = 0.0
            
            with torch.no_grad():
                for batch_X, batch_y in val_loader:
                    outputs = self.lstm_model(batch_X)
                    loss = criterion(outputs, batch_y)
                    val_loss += loss.item()
            
            train_loss /= len(train_loader)
            val_loss /= len(val_loader)
            
            training_history['train_loss'].append(train_loss)
            training_history['val_loss'].append(val_loss)
            
            # 學習率調整
            scheduler.step(val_loss)
            
            # 早停檢查
            if val_loss < best_val_loss:
                best_val_loss = val_loss
                patience_counter = 0
                
                # 保存最佳模型
                best_model_state = self.lstm_model.state_dict().copy()
            else:
                patience_counter += 1
            
            if epoch % 10 == 0:
                self.logger.info(f"Epoch {epoch}: Train Loss={train_loss:.6f}, Val Loss={val_loss:.6f}")
            
            if patience_counter >= self.config.lstm_config.early_stopping_patience:
                self.logger.info(f"早停於 epoch {epoch}")
                break
        
        # 恢復最佳模型
        self.lstm_model.load_state_dict(best_model_state)
        
        training_time = time.time() - start_time
        
        # 評估模型
        self.lstm_model.eval()
        with torch.no_grad():
            train_pred = self.lstm_model(X_train).cpu().numpy()
            val_pred = self.lstm_model(X_val).cpu().numpy()
            
            y_train_np = y_train.view(y_train.size(0), -1).cpu().numpy()
            y_val_np = y_val.view(y_val.size(0), -1).cpu().numpy()
        
        # 計算指標
        train_metrics = self._calculate_metrics(y_train_np, train_pred)
        val_metrics = self._calculate_metrics(y_val_np, val_pred)
        
        # 保存模型
        model_path = self.config.get_output_paths()['lstm_model']
        torch.save({
            'model_state_dict': self.lstm_model.state_dict(),
            'model_config': {
                'input_size': input_size,
                'hidden_size': self.config.lstm_config.hidden_size,
                'num_layers': self.config.lstm_config.num_layers,
                'output_size': output_size,
                'dropout': self.config.lstm_config.dropout
            },
            'training_config': self.config.lstm_config.__dict__,
            'training_history': training_history
        }, model_path)
        
        results = {
            'model_path': str(model_path),
            'training_time': training_time,
            'train_metrics': train_metrics,
            'val_metrics': val_metrics,
            'training_history': training_history,
            'final_epoch': epoch,
            'best_val_loss': best_val_loss
        }
        
        self.logger.info(f"LSTM訓練完成: {training_time:.2f}s")
        self.logger.info(f"驗證集MAE: {val_metrics['mae']:.4f}")
        
        return results
    
    def _calculate_metrics(self, y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
        """計算評估指標"""
        # 確保形狀一致
        if y_true.shape != y_pred.shape:
            if len(y_true.shape) > len(y_pred.shape):
                y_pred = y_pred.reshape(y_true.shape)
            else:
                y_true = y_true.reshape(y_pred.shape)
        
        # 計算各項指標
        mae = mean_absolute_error(y_true.flatten(), y_pred.flatten())
        rmse = np.sqrt(mean_squared_error(y_true.flatten(), y_pred.flatten()))
        mape = calculate_mape(y_true.flatten(), y_pred.flatten())
        r2 = r2_score(y_true.flatten(), y_pred.flatten())
        
        return {
            'mae': float(mae),
            'rmse': float(rmse),
            'mape': float(mape),
            'r2': float(r2)
        }
    
    def train_all_models(self) -> Dict[str, Any]:
        """訓練所有模型（向後兼容性別名）"""
        return self.train_both_models()
    
    def train_both_models(self) -> Dict[str, Any]:
        """訓練兩個模型"""
        self.logger.info("=" * 50)
        self.logger.info(f"開始執行 {self.config.mode} 模式的模型訓練")
        self.logger.info("=" * 50)
        
        try:
            # 載入數據
            data = self.load_training_data()
            
            results = {}
            
            # 訓練LightGBM
            try:
                self.logger.info("訓練LightGBM模型...")
                results['lightgbm'] = self.train_lightgbm(data)
            except Exception as e:
                self.logger.error(f"LightGBM訓練失敗: {e}")
                results['lightgbm'] = {'error': str(e)}
            
            # 訓練LSTM
            try:
                self.logger.info("訓練LSTM模型...")
                results['lstm'] = self.train_lstm(data)
            except Exception as e:
                self.logger.error(f"LSTM訓練失敗: {e}")
                results['lstm'] = {'error': str(e)}
            
            # 生成比較報告
            comparison_report = self._generate_comparison_report(results)
            
            # 保存結果
            evaluation_path = self.config.get_output_paths()['evaluation_report']
            import json
            with open(evaluation_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2, default=str)
            
            # 保存比較報告
            comparison_path = self.config.get_output_paths()['comparison_report']
            with open(comparison_path, 'w', encoding='utf-8') as f:
                f.write(comparison_report)
            
            self.logger.info("模型訓練管道執行完成")
            return results
            
        except Exception as e:
            self.logger.error(f"訓練管道執行失敗: {e}")
            raise
    
    def _generate_comparison_report(self, results: Dict[str, Any]) -> str:
        """生成模型比較報告"""
        report = f"""
# {self.config.mode} 模式模型訓練報告

## 基本信息
- **模式**: {self.config.mode}
- **測站**: {self.config.station or '全部'}
- **時間戳**: {self.config.timestamp}
- **設備**: {self.device}

## 配置參數
- **時間窗口**: {self.config.time_config.window_size} 小時
- **預測範圍**: {self.config.time_config.horizon} 小時
- **訓練比例**: {self.config.time_config.train_ratio:.1%}

## 模型比較

### LightGBM 結果
"""
        
        if 'lightgbm' in results and 'error' not in results['lightgbm']:
            lgbm_results = results['lightgbm']
            report += f"""
- **訓練時間**: {lgbm_results['training_time']:.2f} 秒
- **驗證集指標**:
  - MAE: {lgbm_results['val_metrics']['mae']:.4f}
  - RMSE: {lgbm_results['val_metrics']['rmse']:.4f}
  - MAPE: {lgbm_results['val_metrics']['mape']:.2f}%
  - R²: {lgbm_results['val_metrics']['r2']:.4f}
"""
        else:
            report += f"\n- **錯誤**: {results.get('lightgbm', {}).get('error', '未知錯誤')}\n"
        
        report += "\n### LSTM 結果\n"
        
        if 'lstm' in results and 'error' not in results['lstm']:
            lstm_results = results['lstm']
            report += f"""
- **訓練時間**: {lstm_results['training_time']:.2f} 秒
- **最終輪數**: {lstm_results['final_epoch']}
- **驗證集指標**:
  - MAE: {lstm_results['val_metrics']['mae']:.4f}
  - RMSE: {lstm_results['val_metrics']['rmse']:.4f}
  - MAPE: {lstm_results['val_metrics']['mape']:.2f}%
  - R²: {lstm_results['val_metrics']['r2']:.4f}
"""
        else:
            report += f"\n- **錯誤**: {results.get('lstm', {}).get('error', '未知錯誤')}\n"
        
        # 添加比較總結
        if ('lightgbm' in results and 'error' not in results['lightgbm'] and
            'lstm' in results and 'error' not in results['lstm']):
            
            lgbm_mae = results['lightgbm']['val_metrics']['mae']
            lstm_mae = results['lstm']['val_metrics']['mae']
            
            better_model = "LightGBM" if lgbm_mae < lstm_mae else "LSTM"
            mae_diff = abs(lgbm_mae - lstm_mae)
            
            report += f"""
## 總結

- **較佳模型**: {better_model} (MAE差異: {mae_diff:.4f})
- **建議使用**: {better_model} 模型用於此配置
"""
        
        report += f"""

## 輸出檔案
- **LightGBM模型**: {self.config.get_output_paths()['lgbm_model']}
- **LSTM模型**: {self.config.get_output_paths()['lstm_model']}
- **評估報告**: {self.config.get_output_paths()['evaluation_report']}
"""
        
        return report

# === 便利函數 ===
def train_models_by_mode(mode: str, station: Optional[str] = None,
                        custom_config: Optional[UnifiedConfig] = None) -> Dict[str, Any]:
    """按模式訓練模型的便利函數"""
    if custom_config is None:
        config = UnifiedConfig(mode=mode, station=station)
    else:
        config = custom_config
    
    trainer = UnifiedTrainer(config)
    return trainer.train_both_models()

def batch_train_models(modes: List[str], stations: Optional[List[str]] = None) -> Dict[str, Dict[str, Any]]:
    """批量訓練模型"""
    results = {}
    
    for mode in modes:
        if mode in ['separate', 'separate_norm', 'station_specific'] and stations:
            for station in stations:
                key = f"{mode}_{station}"
                try:
                    results[key] = train_models_by_mode(mode, station)
                except Exception as e:
                    results[key] = {'error': str(e)}
        else:
            try:
                results[mode] = train_models_by_mode(mode)
            except Exception as e:
                results[mode] = {'error': str(e)}
    
    return results 