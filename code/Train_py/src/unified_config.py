"""
AQI 預測系統 - 統一配置管理
支援5種標準化訓練模式的統一配置
"""

import os
import torch
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Optional, Union
from datetime import datetime

# === 專案路徑 ===
PROJECT_ROOT = Path(__file__).parent.parent
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_INTERIM = PROJECT_ROOT / "data" / "interim"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
DATA_SLIDING_WINDOWS = PROJECT_ROOT / "data" / "sliding_windows"
MODELS_DIR = PROJECT_ROOT / "models"
REPORTS_DIR = PROJECT_ROOT / "reports"
LOGS_DIR = PROJECT_ROOT / "logs"

# 確保目錄存在
for dir_path in [DATA_INTERIM, DATA_PROCESSED, DATA_SLIDING_WINDOWS, MODELS_DIR, REPORTS_DIR, LOGS_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# === 計算資源設定 ===
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
GPU_AVAILABLE = torch.cuda.is_available()
GPU_COUNT = torch.cuda.device_count() if GPU_AVAILABLE else 0
CPU_COUNT = os.cpu_count()

@dataclass
class PerformanceConfig:
    """性能配置"""
    use_gpu: bool = GPU_AVAILABLE
    device: str = DEVICE
    num_workers: int = min(4, CPU_COUNT)
    pin_memory: bool = GPU_AVAILABLE
    chunk_size: int = 50000
    mixed_precision: bool = GPU_AVAILABLE

@dataclass
class TimeConfig:
    """時間相關配置 - 所有訓練統一"""
    window_size: int = 24          # 輸入時間窗口（小時）
    horizon: int = 6               # 預測時間範圍（小時）
    stride: int = 1                # 滑動步長
    train_ratio: float = 0.8       # 訓練集比例
    val_ratio: float = 0.1         # 驗證集比例
    test_ratio: float = 0.1        # 測試集比例

@dataclass
class LGBMConfig:
    """LightGBM統一配置"""
    objective: str = 'regression'
    metric: str = 'mae'
    boosting_type: str = 'gbdt'
    num_leaves: int = 31
    learning_rate: float = 0.1
    feature_fraction: float = 0.8
    bagging_fraction: float = 0.8
    bagging_freq: int = 5
    verbose: int = -1
    max_bin: int = 511
    min_data_in_leaf: int = 100
    n_estimators: int = 1000
    max_depth: int = 8
    n_jobs: int = CPU_COUNT
    force_col_wise: bool = True
    early_stopping_rounds: int = 100
    random_state: int = 42

@dataclass
class LSTMConfig:
    """LSTM統一配置"""
    hidden_size: int = 128
    num_layers: int = 3
    dropout: float = 0.2
    learning_rate: float = 0.001
    batch_size: int = 64 if not GPU_AVAILABLE else 128
    epochs: int = 100
    early_stopping_patience: int = 10
    grad_clip: float = 1.0
    device: str = DEVICE
    num_workers: int = min(4, CPU_COUNT)
    pin_memory: bool = GPU_AVAILABLE
    weight_decay: float = 1e-5
    scheduler_factor: float = 0.5
    scheduler_patience: int = 5
    random_state: int = 42

@dataclass
class DataPipelineConfig:
    """數據管道配置"""
    name: str
    description: str
    raw_path: Optional[Path] = None
    raw_dir: Optional[Path] = None
    output_prefix: str = ""
    is_normalized: bool = False
    is_combined: bool = False
    
    def __post_init__(self):
        if self.output_prefix == "":
            self.output_prefix = self.name.lower()

# === 五種標準化訓練模式 ===
TRAINING_MODES = {
    'combine': DataPipelineConfig(
        name='combine',
        description='完整合併數據（原始）',
        raw_path=DATA_RAW / "Combine" / "Combine_AllData.csv",
        is_normalized=False,
        is_combined=True
    ),
    'combine_norm': DataPipelineConfig(
        name='combine_norm',
        description='完整合併數據（標準化）',
        raw_path=DATA_RAW / "Combine_Nomolization" / "Nomorlization_Combine_AllData.csv",
        is_normalized=True,
        is_combined=True
    ),
    'separate': DataPipelineConfig(
        name='separate',
        description='各測站分別數據（原始）',
        raw_dir=DATA_RAW / "Separate",
        is_normalized=False,
        is_combined=False
    ),
    'separate_norm': DataPipelineConfig(
        name='separate_norm',
        description='各測站分別數據（標準化）',
        raw_dir=DATA_RAW / "Separate_Nomorlization",
        is_normalized=True,
        is_combined=False
    ),
    'station_specific': DataPipelineConfig(
        name='station_specific',
        description='指定測站（原始+標準化）',
        raw_dir=None,  # 動態設定
        is_normalized=False,  # 包含兩種
        is_combined=False
    )
}

# === 評估指標配置 ===
@dataclass
class MetricsConfig:
    """評估指標配置"""
    metrics: List[str] = None
    target_mae_threshold: float = 1.0
    target_rmse_threshold: float = 1.5
    target_mape_threshold: float = 15.0
    
    def __post_init__(self):
        if self.metrics is None:
            self.metrics = ['mae', 'rmse', 'mape', 'r2']

# === 研究標準配置 ===
@dataclass
class ResearchStandardConfig:
    """研究標準配置"""
    # 實驗重現性
    random_seed: int = 42
    
    # 交叉驗證
    cv_folds: int = 5
    cv_strategy: str = 'time_series'  # time_series, stratified, kfold
    
    # 統計顯著性
    significance_level: float = 0.05
    confidence_interval: float = 0.95
    
    # 效果量
    effect_size_threshold: float = 0.5
    
    # 模型比較
    comparison_metrics: List[str] = None
    statistical_test: str = 'wilcoxon'  # wilcoxon, ttest, mannwhitney
    
    # 報告標準
    decimal_places: int = 4
    p_value_format: str = '%.4f'
    
    def __post_init__(self):
        if self.comparison_metrics is None:
            self.comparison_metrics = ['mae', 'rmse', 'mape']

# === 統一配置類 ===
class UnifiedConfig:
    """統一配置管理器"""
    
    def __init__(self, 
                 mode: str = 'combine',
                 station: Optional[str] = None,
                 custom_time_config: Optional[TimeConfig] = None,
                 custom_lgbm_config: Optional[LGBMConfig] = None,
                 custom_lstm_config: Optional[LSTMConfig] = None):
        
        # 基礎配置
        self.mode = mode
        self.station = station
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 數據管道配置
        if mode not in TRAINING_MODES:
            raise ValueError(f"不支援的訓練模式: {mode}. 支援的模式: {list(TRAINING_MODES.keys())}")
        self.pipeline_config = TRAINING_MODES[mode]
        
        # 時間配置（統一）
        self.time_config = custom_time_config or TimeConfig()
        
        # 模型配置
        self.lgbm_config = custom_lgbm_config or LGBMConfig()
        self.lstm_config = custom_lstm_config or LSTMConfig()
        
        # 性能配置
        self.performance_config = PerformanceConfig()
        
        # 評估配置
        self.metrics_config = MetricsConfig()
        
        # 研究標準配置
        self.research_config = ResearchStandardConfig()
        
        # 設定隨機種子
        self._set_random_seeds()
        
    def _set_random_seeds(self):
        """設定統一的隨機種子"""
        import random
        import numpy as np
        
        seed = self.research_config.random_seed
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed(seed)
            torch.cuda.manual_seed_all(seed)
            torch.backends.cudnn.deterministic = True
            torch.backends.cudnn.benchmark = False
    
    def get_output_paths(self) -> Dict[str, Path]:
        """獲取輸出路徑"""
        base_name = f"{self.mode}"
        if self.station:
            base_name += f"_{self.station}"
        base_name += f"_{self.timestamp}"
        
        # 根據模式決定子目錄結構
        if self.mode in ['separate', 'separate_norm']:
            processed_dir = DATA_PROCESSED / self.mode
            windows_dir = DATA_SLIDING_WINDOWS / self.mode
            models_dir = MODELS_DIR / "lightgbm" / self.mode
            lstm_models_dir = MODELS_DIR / "lstm" / self.mode
        else:
            processed_dir = DATA_PROCESSED
            windows_dir = DATA_SLIDING_WINDOWS
            models_dir = MODELS_DIR
            lstm_models_dir = MODELS_DIR
        
        return {
            'processed_data': processed_dir / f"{base_name}_processed.npz",
            'windows_data_npz': windows_dir / f"{base_name}_windows.npz",
            'windows_data_pt': windows_dir / f"{base_name}_windows.pt",
            'lgbm_model': models_dir / f"{base_name}_lgbm.pkl",
            'lstm_model': lstm_models_dir / f"{base_name}_lstm.pt",
            'evaluation_report': REPORTS_DIR / f"{base_name}_evaluation.json",
            'comparison_report': REPORTS_DIR / f"{base_name}_comparison.md",
            'log_file': LOGS_DIR / f"{base_name}_training.log"
        }
    
    def get_input_paths(self) -> Union[Path, List[Path]]:
        """獲取輸入路徑"""
        if self.pipeline_config.raw_path:
            return self.pipeline_config.raw_path
        elif self.pipeline_config.raw_dir:
            if self.station:
                # 指定測站
                raw_files = []
                for suffix in ["", "_norm"]:
                    pattern = f"*{self.station}*{suffix}_combined.csv"
                    matching_files = list(self.pipeline_config.raw_dir.glob(pattern))
                    raw_files.extend(matching_files)
                return raw_files
            else:
                # 所有測站
                return list(self.pipeline_config.raw_dir.glob("*_combined.csv"))
        else:
            raise ValueError(f"無法確定輸入路徑: {self.mode}")
    
    def to_dict(self) -> Dict:
        """轉換為字典格式"""
        return {
            'mode': self.mode,
            'station': self.station,
            'timestamp': self.timestamp,
            'pipeline_config': self.pipeline_config.__dict__,
            'time_config': self.time_config.__dict__,
            'lgbm_config': self.lgbm_config.__dict__,
            'lstm_config': self.lstm_config.__dict__,
            'performance_config': self.performance_config.__dict__,
            'metrics_config': self.metrics_config.__dict__,
            'research_config': self.research_config.__dict__,
        }
    
    def save_config(self, output_path: Path):
        """保存配置到文件"""
        import json
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2, default=str)
    
    def __str__(self) -> str:
        """字符串表示"""
        return f"UnifiedConfig(mode={self.mode}, station={self.station}, timestamp={self.timestamp})"

# === 預定義配置 ===
def get_standard_configs() -> Dict[str, UnifiedConfig]:
    """獲取標準配置"""
    configs = {}
    
    for mode in TRAINING_MODES.keys():
        configs[mode] = UnifiedConfig(mode=mode)
    
    return configs

def get_station_configs(station: str) -> Dict[str, UnifiedConfig]:
    """獲取指定測站的配置"""
    return {
        'separate': UnifiedConfig(mode='separate', station=station),
        'separate_norm': UnifiedConfig(mode='separate_norm', station=station),
        'station_specific': UnifiedConfig(mode='station_specific', station=station)
    }

# === 研究標準驗證 ===
def validate_research_standards(config: UnifiedConfig) -> Dict[str, bool]:
    """驗證研究標準"""
    validations = {}
    
    # 檢查隨機種子設定
    validations['random_seed_set'] = config.research_config.random_seed is not None
    
    # 檢查時間窗口統一性
    validations['time_window_consistent'] = (
        config.time_config.window_size == 24 and 
        config.time_config.horizon == 6
    )
    
    # 檢查數據分割一致性
    total_ratio = (config.time_config.train_ratio + 
                  config.time_config.val_ratio + 
                  config.time_config.test_ratio)
    validations['data_split_valid'] = abs(total_ratio - 1.0) < 1e-6
    
    # 檢查評估指標標準化
    required_metrics = {'mae', 'rmse', 'mape'}
    validations['metrics_standardized'] = required_metrics.issubset(set(config.metrics_config.metrics))
    
    return validations

# === 配置工廠 ===
class ConfigFactory:
    """配置工廠"""
    
    @staticmethod
    def create_research_config(mode: str, station: Optional[str] = None, **kwargs) -> UnifiedConfig:
        """創建符合研究標準的配置"""
        config = UnifiedConfig(mode=mode, station=station, **kwargs)
        
        # 驗證研究標準
        validations = validate_research_standards(config)
        failed_validations = [k for k, v in validations.items() if not v]
        
        if failed_validations:
            raise ValueError(f"配置不符合研究標準: {failed_validations}")
        
        return config
    
    @staticmethod
    def create_batch_configs(modes: List[str], stations: Optional[List[str]] = None) -> List[UnifiedConfig]:
        """批量創建配置"""
        configs = []
        
        for mode in modes:
            if mode in ['separate', 'separate_norm', 'station_specific'] and stations:
                for station in stations:
                    configs.append(ConfigFactory.create_research_config(mode, station))
            else:
                configs.append(ConfigFactory.create_research_config(mode))
        
        return configs

# === 常量定義 ===
# 所有支援的訓練模式
ALL_MODES = list(TRAINING_MODES.keys())

# 需要指定測站的模式
STATION_REQUIRED_MODES = ['separate', 'separate_norm', 'station_specific']

# 全域訓練模式
GLOBAL_MODES = ['combine', 'combine_norm']

# 默認測站列表（從數據目錄自動檢測）
DEFAULT_STATIONS = []
if (DATA_RAW / "Separate").exists():
    station_files = list((DATA_RAW / "Separate").glob("*_combined.csv"))
    DEFAULT_STATIONS = [f.stem.split('_')[0] for f in station_files]
    DEFAULT_STATIONS = sorted(list(set(DEFAULT_STATIONS)))  # 去重排序 