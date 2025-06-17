"""
資料 IO 工具函式
支援 CSV ↔ Parquet ↔ NPZ 的轉換與讀寫
"""

import numpy as np
import pandas as pd
import torch
from pathlib import Path
from typing import Tuple, Optional, List, Dict, Any, Union
import logging
import pickle
import joblib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def read_csv_with_encoding(file_path: Path, encodings: List[str] = None) -> pd.DataFrame:
    """
    嘗試多種編碼讀取 CSV 檔案
    
    Args:
        file_path: CSV 檔案路徑
        encodings: 嘗試的編碼列表
    
    Returns:
        DataFrame
    """
    if encodings is None:
        encodings = ['utf-8', 'utf-8-sig', 'cp950', 'big5', 'gbk']
    
    for encoding in encodings:
        try:
            df = pd.read_csv(file_path, encoding=encoding)
            logger.info(f"成功使用 {encoding} 編碼讀取 {file_path}")
            return df
        except (UnicodeDecodeError, UnicodeError):
            continue
    
    raise ValueError(f"無法使用任何編碼讀取檔案: {file_path}")

def save_parquet(df: pd.DataFrame, output_path: Path, compression: str = 'snappy') -> None:
    """
    儲存 DataFrame 為 Parquet 格式
    
    Args:
        df: 要儲存的 DataFrame
        output_path: 輸出路徑
        compression: 壓縮方式
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(output_path, compression=compression, index=False)
    logger.info(f"已儲存 Parquet 檔案: {output_path} (shape: {df.shape})")

def load_parquet(file_path: Path) -> pd.DataFrame:
    """
    讀取 Parquet 檔案
    
    Args:
        file_path: Parquet 檔案路徑
    
    Returns:
        DataFrame
    """
    df = pd.read_parquet(file_path)
    logger.info(f"已讀取 Parquet 檔案: {file_path} (shape: {df.shape})")
    return df

def save_sliding_windows_npz(
    X: np.ndarray, 
    y: np.ndarray, 
    output_path: Path,
    feature_names: Optional[List[str]] = None,
    target_names: Optional[List[str]] = None
) -> None:
    """
    儲存滑動窗資料為 NPZ 格式 (適用於 LightGBM)
    
    Args:
        X: 特徵陣列 (N, seq_len, n_features)
        y: 目標陣列 (N, horizon, n_targets)  
        output_path: 輸出路徑
        feature_names: 特徵名稱列表
        target_names: 目標名稱列表
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    save_dict = {
        'X': X,
        'y': y,
        'X_shape': X.shape,
        'y_shape': y.shape
    }
    
    if feature_names:
        save_dict['feature_names'] = np.array(feature_names)
    if target_names:
        save_dict['target_names'] = np.array(target_names)
    
    np.savez_compressed(output_path, **save_dict)
    logger.info(f"已儲存 NPZ 檔案: {output_path} (X: {X.shape}, y: {y.shape})")

def load_sliding_windows_npz(file_path: Path) -> Tuple[np.ndarray, np.ndarray, Dict[str, Any]]:
    """
    讀取滑動窗 NPZ 檔案
    
    Args:
        file_path: NPZ 檔案路徑
    
    Returns:
        X, y, metadata
    """
    data = np.load(file_path, allow_pickle=True)
    X = data['X']
    y = data['y']
    
    metadata = {}
    for key in data.files:
        if key not in ['X', 'y']:
            metadata[key] = data[key]
    
    logger.info(f"已讀取 NPZ 檔案: {file_path} (X: {X.shape}, y: {y.shape})")
    return X, y, metadata

def save_sliding_windows_torch(
    X: np.ndarray, 
    y: np.ndarray, 
    output_path: Path,
    feature_names: Optional[List[str]] = None,
    target_names: Optional[List[str]] = None
) -> None:
    """
    儲存滑動窗資料為 PyTorch 格式 (適用於 LSTM)
    
    Args:
        X: 特徵陣列 (N, seq_len, n_features)
        y: 目標陣列 (N, horizon, n_targets)
        output_path: 輸出路徑  
        feature_names: 特徵名稱列表
        target_names: 目標名稱列表
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 轉換為 PyTorch tensors
    X_tensor = torch.from_numpy(X).float()
    y_tensor = torch.from_numpy(y).float()
    
    save_dict = {
        'X': X_tensor,
        'y': y_tensor,
        'X_shape': X.shape,
        'y_shape': y.shape
    }
    
    if feature_names:
        save_dict['feature_names'] = feature_names
    if target_names:
        save_dict['target_names'] = target_names
    
    torch.save(save_dict, output_path)
    logger.info(f"已儲存 PyTorch 檔案: {output_path} (X: {X.shape}, y: {y.shape})")

def load_sliding_windows_torch(file_path: Path) -> Tuple[torch.Tensor, torch.Tensor, Dict[str, Any]]:
    """
    讀取滑動窗 PyTorch 檔案
    
    Args:
        file_path: PyTorch 檔案路徑
    
    Returns:
        X_tensor, y_tensor, metadata
    """
    data = torch.load(file_path, map_location='cpu', weights_only=False)
    X = data['X']
    y = data['y']
    
    metadata = {}
    for key in data.keys():
        if key not in ['X', 'y']:
            metadata[key] = data[key]
    
    logger.info(f"已讀取 PyTorch 檔案: {file_path} (X: {X.shape}, y: {y.shape})")
    return X, y, metadata

def get_recent_data(
    df: pd.DataFrame, 
    time_col: str, 
    seq_len: int, 
    end_time: Optional[str] = None
) -> pd.DataFrame:
    """
    取得最近的 seq_len 小時資料
    
    Args:
        df: 完整的 DataFrame
        time_col: 時間欄位名稱
        seq_len: 要取得的時間長度 (小時)
        end_time: 結束時間，None 代表取最新的
    
    Returns:
        最近的 DataFrame
    """
    # 確保時間欄位為 datetime
    df[time_col] = pd.to_datetime(df[time_col])
    df_sorted = df.sort_values(time_col)
    
    if end_time is None:
        end_idx = len(df_sorted)
    else:
        end_time = pd.to_datetime(end_time)
        end_idx = df_sorted[df_sorted[time_col] <= end_time].index[-1] + 1
    
    start_idx = max(0, end_idx - seq_len)
    recent_data = df_sorted.iloc[start_idx:end_idx].copy()
    
    logger.info(f"取得最近 {len(recent_data)} 筆資料 (需要 {seq_len} 筆)")
    return recent_data

def list_station_files(directory: Path, pattern: str = "*_combined.csv") -> List[Path]:
    """
    列出指定目錄下的站點檔案
    
    Args:
        directory: 目錄路徑
        pattern: 檔案名稱模式
    
    Returns:
        檔案路徑列表
    """
    files = list(directory.glob(pattern))
    logger.info(f"在 {directory} 找到 {len(files)} 個站點檔案")
    return sorted(files)

def extract_station_id(file_path: Path) -> str:
    """
    從檔案路徑提取站點 ID
    
    Args:
        file_path: 檔案路徑
    
    Returns:
        站點 ID
    """
    # 例如：二林_C0G730_combined.csv -> C0G730
    filename = file_path.stem
    if 'Nomorlization_' in filename:
        filename = filename.replace('Nomorlization_', '')
    
    parts = filename.split('_')
    if len(parts) >= 2:
        return parts[1]  # 取得 station code
    else:
        return parts[0]

def load_data(file_path: Union[str, Path]) -> pd.DataFrame:
    """載入數據文件"""
    file_path = Path(file_path)
    
    if file_path.suffix == '.csv':
        return pd.read_csv(file_path)
    elif file_path.suffix == '.pkl':
        return pd.read_pickle(file_path)
    elif file_path.suffix in ['.xlsx', '.xls']:
        return pd.read_excel(file_path)
    else:
        raise ValueError(f"不支援的文件格式: {file_path.suffix}")

def save_data(data: Union[pd.DataFrame, Dict[str, Any]], file_path: Union[str, Path]) -> None:
    """保存數據"""
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    if isinstance(data, pd.DataFrame):
        if file_path.suffix == '.csv':
            data.to_csv(file_path, index=False)
        elif file_path.suffix == '.pkl':
            data.to_pickle(file_path)
        elif file_path.suffix in ['.xlsx', '.xls']:
            data.to_excel(file_path, index=False)
        else:
            raise ValueError(f"不支援的DataFrame格式: {file_path.suffix}")
    
    elif isinstance(data, dict):
        if file_path.suffix == '.pkl':
            with open(file_path, 'wb') as f:
                pickle.dump(data, f)
        elif file_path.suffix == '.npz':
            np.savez_compressed(file_path, **data)
        else:
            raise ValueError(f"不支援的字典格式: {file_path.suffix}")
    
    else:
        # 使用joblib作為通用保存方法
        joblib.dump(data, file_path) 