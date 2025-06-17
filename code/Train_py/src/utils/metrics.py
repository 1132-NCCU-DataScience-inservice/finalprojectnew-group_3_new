"""
評估指標計算工具
提供 MAE、RMSE、DTW、MAPE 等指標的計算功能
"""

import numpy as np
import pandas as pd
from typing import Tuple, Dict, List, Optional, Union
import warnings
warnings.filterwarnings('ignore')

def mae(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    計算平均絕對誤差 (Mean Absolute Error)
    
    Args:
        y_true: 真實值
        y_pred: 預測值
    
    Returns:
        MAE 值
    """
    return np.mean(np.abs(y_true - y_pred))

def rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    計算均方根誤差 (Root Mean Square Error)
    
    Args:
        y_true: 真實值  
        y_pred: 預測值
    
    Returns:
        RMSE 值
    """
    return np.sqrt(np.mean((y_true - y_pred) ** 2))

def calculate_mape(y_true: np.ndarray, y_pred: np.ndarray, epsilon: float = 1e-8) -> float:
    """計算MAPE (Mean Absolute Percentage Error)"""
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    
    # 避免除零錯誤
    denominator = np.maximum(np.abs(y_true), epsilon)
    mape = np.mean(np.abs((y_true - y_pred) / denominator)) * 100
    
    return float(mape)

def calculate_rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """計算RMSE (Root Mean Square Error)"""
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    
    mse = np.mean((y_true - y_pred) ** 2)
    rmse = np.sqrt(mse)
    
    return float(rmse)

def dtw_distance(x: np.ndarray, y: np.ndarray) -> float:
    """
    計算動態時間規整距離 (Dynamic Time Warping)
    
    Args:
        x: 序列 1
        y: 序列 2
    
    Returns:
        DTW 距離
    """
    n, m = len(x), len(y)
    
    # 建立距離矩陣
    dtw_matrix = np.full((n + 1, m + 1), np.inf)
    dtw_matrix[0, 0] = 0
    
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = abs(x[i-1] - y[j-1])
            dtw_matrix[i, j] = cost + min(
                dtw_matrix[i-1, j],      # insertion
                dtw_matrix[i, j-1],      # deletion
                dtw_matrix[i-1, j-1]     # match
            )
    
    return dtw_matrix[n, m]

def persistence_baseline(y_train: np.ndarray, horizon: int) -> np.ndarray:
    """
    持續性基線預測 (Persistence Baseline)
    使用最後一個值作為未來所有時間步的預測
    
    Args:
        y_train: 訓練資料的最後部分
        horizon: 預測時間範圍
    
    Returns:
        持續性預測
    """
    if len(y_train.shape) == 1:
        # 單變量
        return np.full(horizon, y_train[-1])
    else:
        # 多變量 
        return np.tile(y_train[-1], (horizon, 1))

def calculate_batch_metrics(
    y_true: np.ndarray, 
    y_pred: np.ndarray,
    target_names: Optional[List[str]] = None
) -> Dict[str, Dict[str, float]]:
    """
    批次計算多個目標的評估指標
    
    Args:
        y_true: 真實值 (N, horizon, n_targets) 或 (N, n_targets)
        y_pred: 預測值 (N, horizon, n_targets) 或 (N, n_targets) 
        target_names: 目標變數名稱列表
    
    Returns:
        字典形式的指標結果
    """
    if len(y_true.shape) == 3:
        # 3D: (N, horizon, n_targets) -> reshape to (N*horizon, n_targets)
        y_true_2d = y_true.reshape(-1, y_true.shape[-1])
        y_pred_2d = y_pred.reshape(-1, y_pred.shape[-1])
    else:
        # 2D: (N, n_targets)
        y_true_2d = y_true
        y_pred_2d = y_pred
    
    n_targets = y_true_2d.shape[1]
    
    if target_names is None:
        target_names = [f'target_{i}' for i in range(n_targets)]
    
    results = {}
    
    # 整體指標
    results['overall'] = {
        'mae': mae(y_true_2d, y_pred_2d),
        'rmse': rmse(y_true_2d, y_pred_2d),
        'mape': calculate_mape(y_true_2d, y_pred_2d)
    }
    
    # 各目標指標
    for i, target_name in enumerate(target_names):
        results[target_name] = {
            'mae': mae(y_true_2d[:, i], y_pred_2d[:, i]),
            'rmse': rmse(y_true_2d[:, i], y_pred_2d[:, i]),
            'mape': calculate_mape(y_true_2d[:, i], y_pred_2d[:, i])
        }
    
    return results

def calculate_temporal_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    horizon_labels: Optional[List[str]] = None
) -> Dict[str, Dict[str, float]]:
    """
    計算不同時間步的評估指標
    
    Args:
        y_true: 真實值 (N, horizon, n_targets)
        y_pred: 預測值 (N, horizon, n_targets)
        horizon_labels: 時間步標籤
    
    Returns:
        各時間步的指標結果
    """
    if len(y_true.shape) != 3:
        raise ValueError("需要 3D 陣列: (N, horizon, n_targets)")
    
    N, horizon, n_targets = y_true.shape
    
    if horizon_labels is None:
        horizon_labels = [f'hour_{i+1}' for i in range(horizon)]
    
    results = {}
    
    for h in range(horizon):
        # 取得該時間步的所有樣本和目標
        y_true_h = y_true[:, h, :].reshape(-1)  # (N * n_targets,)
        y_pred_h = y_pred[:, h, :].reshape(-1)  # (N * n_targets,)
        
        results[horizon_labels[h]] = {
            'mae': mae(y_true_h, y_pred_h),
            'rmse': rmse(y_true_h, y_pred_h),
            'mape': calculate_mape(y_true_h, y_pred_h)
        }
    
    return results

def create_metrics_summary(
    metrics_dict: Dict[str, Dict[str, float]],
    focus_targets: Optional[List[str]] = None,
    focus_metrics: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    建立指標摘要表格
    
    Args:
        metrics_dict: 指標字典
        focus_targets: 重點目標清單
        focus_metrics: 重點指標清單
    
    Returns:
        指標摘要 DataFrame
    """
    if focus_metrics is None:
        focus_metrics = ['mae', 'rmse', 'mape']
    
    data = []
    for target, metrics in metrics_dict.items():
        if focus_targets is None or target in focus_targets:
            row = {'target': target}
            for metric in focus_metrics:
                if metric in metrics:
                    row[metric] = metrics[metric]
            data.append(row)
    
    return pd.DataFrame(data)

def check_target_thresholds(
    metrics_dict: Dict[str, Dict[str, float]],
    pm25_mae_threshold: float = 6.0,
    rmse_threshold: float = 10.0
) -> Dict[str, bool]:
    """
    檢查是否達到目標門檻
    
    Args:
        metrics_dict: 指標字典
        pm25_mae_threshold: PM2.5 MAE 門檻
        rmse_threshold: RMSE 門檻
    
    Returns:
        檢查結果
    """
    results = {}
    
    # 檢查 PM2.5 MAE
    if 'AQI_pm2.5' in metrics_dict:
        pm25_mae = metrics_dict['AQI_pm2.5']['mae']
        results['PM2.5_MAE_OK'] = pm25_mae <= pm25_mae_threshold
        results['PM2.5_MAE_value'] = pm25_mae
    
    # 檢查整體 RMSE
    if 'overall' in metrics_dict:
        overall_rmse = metrics_dict['overall']['rmse']
        results['Overall_RMSE_OK'] = overall_rmse <= rmse_threshold
        results['Overall_RMSE_value'] = overall_rmse
    
    return results

def compare_with_baseline(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_train_last: np.ndarray,
    target_names: Optional[List[str]] = None
) -> Dict[str, Dict[str, float]]:
    """
    與持續性基線比較
    
    Args:
        y_true: 真實值
        y_pred: 模型預測值  
        y_train_last: 訓練資料最後的值 (用於持續性預測)
        target_names: 目標名稱
    
    Returns:
        比較結果
    """
    # 產生持續性基線預測
    if len(y_true.shape) == 3:
        N, horizon, n_targets = y_true.shape
        y_persistence = np.tile(y_train_last, (N, horizon, 1))
    else:
        N, n_targets = y_true.shape  
        y_persistence = np.tile(y_train_last, (N, 1))
    
    # 計算模型指標
    model_metrics = calculate_batch_metrics(y_true, y_pred, target_names)
    
    # 計算基線指標  
    baseline_metrics = calculate_batch_metrics(y_true, y_persistence, target_names)
    
    # 計算改進程度
    improvement = {}
    for target in model_metrics.keys():
        improvement[target] = {}
        for metric in ['mae', 'rmse']:
            if metric in model_metrics[target] and metric in baseline_metrics[target]:
                model_val = model_metrics[target][metric]
                baseline_val = baseline_metrics[target][metric]
                
                if baseline_val > 0:
                    improve_pct = (baseline_val - model_val) / baseline_val * 100
                    improvement[target][f'{metric}_improvement_%'] = improve_pct
                    improvement[target][f'{metric}_model'] = model_val
                    improvement[target][f'{metric}_baseline'] = baseline_val
    
    return improvement 