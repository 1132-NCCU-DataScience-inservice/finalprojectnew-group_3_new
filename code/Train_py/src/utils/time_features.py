"""
時間特徵工程工具
提供 sin/cos 變換、工作日、節假日等時間特徵的產生
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Optional, Dict

def add_cyclical_time_features(df: pd.DataFrame, time_col: str) -> pd.DataFrame:
    """
    為 DataFrame 新增循環時間特徵 (sin/cos)
    
    Args:
        df: 包含時間欄位的 DataFrame
        time_col: 時間欄位名稱
    
    Returns:
        新增時間特徵的 DataFrame
    """
    df = df.copy()
    
    # 確保時間欄位為 datetime
    df[time_col] = pd.to_datetime(df[time_col])
    
    # 提取時間組件
    df['year'] = df[time_col].dt.year
    df['month'] = df[time_col].dt.month
    df['day'] = df[time_col].dt.day
    df['hour'] = df[time_col].dt.hour
    df['dayofweek'] = df[time_col].dt.dayofweek  # 0=Monday, 6=Sunday
    df['dayofyear'] = df[time_col].dt.dayofyear
    
    # 循環特徵：月份 (1-12)
    df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
    df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)
    
    # 循環特徵：小時 (0-23)
    df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
    df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
    
    # 循環特徵：一年中的天數 (1-365/366)
    max_day = df['dayofyear'].max()
    df['day_sin'] = np.sin(2 * np.pi * df['dayofyear'] / max_day)
    df['day_cos'] = np.cos(2 * np.pi * df['dayofyear'] / max_day)
    
    # 循環特徵：星期 (0-6)
    df['weekday_sin'] = np.sin(2 * np.pi * df['dayofweek'] / 7)
    df['weekday_cos'] = np.cos(2 * np.pi * df['dayofweek'] / 7)
    
    return df

def add_working_day_features(df: pd.DataFrame, time_col: str) -> pd.DataFrame:
    """
    新增工作日相關特徵
    
    Args:
        df: 包含時間欄位的 DataFrame
        time_col: 時間欄位名稱
    
    Returns:
        新增工作日特徵的 DataFrame
    """
    df = df.copy()
    df[time_col] = pd.to_datetime(df[time_col])
    
    # 基本工作日判斷 (0=Monday, 6=Sunday)
    df['is_weekend'] = (df[time_col].dt.dayofweek >= 5).astype(int)
    df['is_weekday'] = (df[time_col].dt.dayofweek < 5).astype(int)
    
    # 工作時間判斷 (9-17點)
    df['is_work_hour'] = ((df[time_col].dt.hour >= 9) & 
                          (df[time_col].dt.hour <= 17)).astype(int)
    
    # 通勤時間 (7-9, 17-19點)
    df['is_rush_hour'] = (((df[time_col].dt.hour >= 7) & (df[time_col].dt.hour <= 9)) |
                          ((df[time_col].dt.hour >= 17) & (df[time_col].dt.hour <= 19))).astype(int)
    
    # 夜間時間 (22-6點)
    df['is_night'] = ((df[time_col].dt.hour >= 22) | 
                      (df[time_col].dt.hour <= 6)).astype(int)
    
    return df

def add_taiwan_holidays(df: pd.DataFrame, time_col: str) -> pd.DataFrame:
    """
    新增台灣節假日特徵
    
    Args:
        df: 包含時間欄位的 DataFrame
        time_col: 時間欄位名稱
    
    Returns:
        新增節假日特徵的 DataFrame
    """
    df = df.copy()
    df[time_col] = pd.to_datetime(df[time_col])
    
    # 固定節假日
    fixed_holidays = {
        (1, 1): "元旦",
        (2, 28): "和平紀念日", 
        (4, 4): "兒童節",
        (5, 1): "勞動節",
        (10, 10): "國慶日",
        (12, 25): "行憲紀念日"
    }
    
    # 檢查固定節假日
    df['is_fixed_holiday'] = 0
    df['holiday_name'] = ''
    
    for (month, day), name in fixed_holidays.items():
        mask = (df[time_col].dt.month == month) & (df[time_col].dt.day == day)
        df.loc[mask, 'is_fixed_holiday'] = 1
        df.loc[mask, 'holiday_name'] = name
    
    # 春節期間 (簡化版：農曆新年前後幾天)
    # 這裡使用簡化的邏輯，實際應該要農曆轉換
    chinese_new_year_dates = {
        2020: (1, 25),  # 2020年農曆新年
        2021: (2, 12),  # 2021年農曆新年
        2022: (2, 1),   # 2022年農曆新年
        2023: (1, 22),  # 2023年農曆新年
        2024: (2, 10),  # 2024年農曆新年
    }
    
    df['is_chinese_new_year'] = 0
    for year, (month, day) in chinese_new_year_dates.items():
        # 春節前後7天
        start_date = datetime(year, month, day) - timedelta(days=3)
        end_date = datetime(year, month, day) + timedelta(days=3)
        
        mask = ((df[time_col].dt.date >= start_date.date()) & 
                (df[time_col].dt.date <= end_date.date()))
        df.loc[mask, 'is_chinese_new_year'] = 1
    
    # 總體節假日指標
    df['is_holiday'] = ((df['is_fixed_holiday'] == 1) | 
                        (df['is_chinese_new_year'] == 1)).astype(int)
    
    return df

def add_season_features(df: pd.DataFrame, time_col: str) -> pd.DataFrame:
    """
    新增季節特徵
    
    Args:
        df: 包含時間欄位的 DataFrame
        time_col: 時間欄位名稱
    
    Returns:
        新增季節特徵的 DataFrame
    """
    df = df.copy()
    df[time_col] = pd.to_datetime(df[time_col])
    
    # 季節劃分 (北半球)
    def get_season(month):
        if month in [12, 1, 2]:
            return 0  # 冬季
        elif month in [3, 4, 5]:
            return 1  # 春季
        elif month in [6, 7, 8]:
            return 2  # 夏季
        else:  # [9, 10, 11]
            return 3  # 秋季
    
    df['season'] = df[time_col].dt.month.apply(get_season)
    
    # One-hot 編碼季節
    for season_idx, season_name in enumerate(['winter', 'spring', 'summer', 'autumn']):
        df[f'season_{season_name}'] = (df['season'] == season_idx).astype(int)
    
    return df

def create_lag_features(
    df: pd.DataFrame, 
    target_cols: List[str], 
    lags: List[int],
    group_col: Optional[str] = None
) -> pd.DataFrame:
    """
    建立滯後特徵
    
    Args:
        df: DataFrame
        target_cols: 目標欄位列表
        lags: 滯後期數列表
        group_col: 分組欄位 (例如站點ID)
    
    Returns:
        新增滯後特徵的 DataFrame
    """
    df = df.copy()
    
    for col in target_cols:
        for lag in lags:
            lag_col_name = f'{col}_lag_{lag}'
            
            if group_col:
                # 按組別建立滯後特徵
                df[lag_col_name] = df.groupby(group_col)[col].shift(lag)
            else:
                # 全體建立滯後特徵
                df[lag_col_name] = df[col].shift(lag)
    
    return df

def create_rolling_features(
    df: pd.DataFrame,
    target_cols: List[str],
    windows: List[int],
    group_col: Optional[str] = None,
    agg_funcs: List[str] = None
) -> pd.DataFrame:
    """
    建立滾動窗口特徵
    
    Args:
        df: DataFrame
        target_cols: 目標欄位列表
        windows: 窗口大小列表
        group_col: 分組欄位
        agg_funcs: 聚合函數列表
    
    Returns:
        新增滾動特徵的 DataFrame
    """
    if agg_funcs is None:
        agg_funcs = ['mean', 'std', 'min', 'max']
    
    df = df.copy()
    
    for col in target_cols:
        for window in windows:
            for func in agg_funcs:
                rolling_col_name = f'{col}_rolling_{window}_{func}'
                
                if group_col:
                    # 按組別建立滾動特徵
                    df[rolling_col_name] = (df.groupby(group_col)[col]
                                           .rolling(window, min_periods=1)
                                           .agg(func)
                                           .reset_index(level=0, drop=True))
                else:
                    # 全體建立滾動特徵
                    df[rolling_col_name] = (df[col]
                                           .rolling(window, min_periods=1)
                                           .agg(func))
    
    return df

def get_time_feature_columns() -> Dict[str, List[str]]:
    """
    取得各類時間特徵的欄位名稱
    
    Returns:
        時間特徵欄位字典
    """
    return {
        'cyclical': [
            'month_sin', 'month_cos', 'hour_sin', 'hour_cos',
            'day_sin', 'day_cos', 'weekday_sin', 'weekday_cos'
        ],
        'working_day': [
            'is_weekend', 'is_weekday', 'is_work_hour', 
            'is_rush_hour', 'is_night'
        ],
        'holiday': [
            'is_fixed_holiday', 'is_chinese_new_year', 'is_holiday'
        ],
        'season': [
            'season', 'season_winter', 'season_spring', 
            'season_summer', 'season_autumn'
        ]
    }

def add_time_features(df: pd.DataFrame, time_col: str = 'date') -> pd.DataFrame:
    """添加時間相關特徵"""
    df = df.copy()
    
    # 確保時間列是datetime格式
    if not pd.api.types.is_datetime64_any_dtype(df[time_col]):
        df[time_col] = pd.to_datetime(df[time_col])
    
    # 提取基本時間特徵
    df['year'] = df[time_col].dt.year
    df['month'] = df[time_col].dt.month
    df['day'] = df[time_col].dt.day
    df['hour'] = df[time_col].dt.hour
    df['day_of_week'] = df[time_col].dt.dayofweek
    df['day_of_year'] = df[time_col].dt.dayofyear
    
    # 添加週期性特徵（sin/cos編碼）
    # 月份週期（12個月）
    df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
    df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)
    
    # 小時週期（24小時）
    df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
    df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
    
    # 一週中的天（7天）
    df['day_sin'] = np.sin(2 * np.pi * df['day_of_week'] / 7)
    df['day_cos'] = np.cos(2 * np.pi * df['day_of_week'] / 7)
    
    # 一年中的天（365天）
    df['dayofyear_sin'] = np.sin(2 * np.pi * df['day_of_year'] / 365)
    df['dayofyear_cos'] = np.cos(2 * np.pi * df['day_of_year'] / 365)
    
    # 添加季節特徵
    df['season'] = df['month'].map({
        12: 0, 1: 0, 2: 0,  # 冬季
        3: 1, 4: 1, 5: 1,   # 春季
        6: 2, 7: 2, 8: 2,   # 夏季
        9: 3, 10: 3, 11: 3  # 秋季
    })
    
    # 添加是否為週末
    df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
    
    return df 