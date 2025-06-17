#!/usr/bin/env python3
"""
配置管理器 - 支持層次化YAML配置
Configuration Manager with Hierarchical YAML Support
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass, field
from datetime import datetime
import logging

# 基礎路徑配置
PROJECT_ROOT = Path(__file__).parent.parent
CONFIGS_DIR = PROJECT_ROOT / "configs"

@dataclass
class PathConfig:
    """路徑配置類"""
    # 數據路徑
    data_raw: Path
    data_processed: Path
    data_windows: Path
    
    # 模型路徑
    models_lightgbm: Path
    models_lstm: Path
    
    # 輸出路徑
    outputs_reports: Path
    outputs_predictions: Path
    outputs_evaluations: Path
    outputs_comparisons: Path
    
    # 日志路徑
    logs_training: Path
    logs_preprocessing: Path
    logs_evaluation: Path
    logs_system: Path

@dataclass
class TimeConfig:
    """時間配置類"""
    window_size: int = 24
    horizon: int = 6
    stride: int = 1
    train_ratio: float = 0.8
    val_ratio: float = 0.1
    test_ratio: float = 0.1

@dataclass
class HardwareConfig:
    """硬體配置類"""
    use_gpu: bool = True
    device: str = "cuda"
    num_workers: int = 4
    pin_memory: bool = True
    mixed_precision: bool = True

@dataclass
class MetricsConfig:
    """評估指標配置類"""
    primary: List[str] = field(default_factory=lambda: ["mae", "rmse", "mape", "r2"])
    thresholds: Dict[str, float] = field(default_factory=lambda: {
        "mae": 2.0, "rmse": 3.0, "mape": 15.0, "r2": 0.7
    })

@dataclass
class ModelConfig:
    """模型配置基類"""
    pass

@dataclass
class LightGBMConfig(ModelConfig):
    """LightGBM配置類"""
    # 基本參數
    objective: str = "regression"
    metric: str = "mae"
    boosting_type: str = "gbdt"
    
    # 樹結構參數
    num_leaves: int = 31
    max_depth: int = 8
    min_data_in_leaf: int = 100
    
    # 學習參數
    learning_rate: float = 0.1
    n_estimators: int = 1000
    
    # 特徵選擇參數
    feature_fraction: float = 0.8
    bagging_fraction: float = 0.8
    bagging_freq: int = 5
    
    # 正則化參數
    lambda_l1: float = 0.0
    lambda_l2: float = 0.0
    
    # 其他參數
    verbose: int = -1
    max_bin: int = 511
    force_col_wise: bool = True
    early_stopping_rounds: int = 100
    random_state: int = 42
    
    # 交叉驗證參數
    cv_folds: int = 5
    cv_stratified: bool = False

@dataclass
class LSTMConfig(ModelConfig):
    """LSTM配置類"""
    # 模型架構參數
    hidden_size: int = 128
    num_layers: int = 3
    dropout: float = 0.2
    bidirectional: bool = False
    
    # 訓練參數
    learning_rate: float = 0.001
    batch_size: int = 128
    epochs: int = 100
    early_stopping_patience: int = 10
    weight_decay: float = 1e-5
    
    # 優化器和調度器參數
    scheduler_factor: float = 0.5
    scheduler_patience: int = 5
    grad_clip: float = 1.0
    
    # 數據載入參數
    num_workers: int = 4
    
    # 其他參數
    random_state: int = 42
    pin_memory: bool = True

@dataclass
class PipelineConfig:
    """管道配置類"""
    name: str
    description: str
    type: str  # global, station_specific
    data_source: Dict[str, Any]
    preprocessing: Dict[str, Any]
    output_paths: Dict[str, Any]
    training: Dict[str, Any]
    is_normalized: bool = False
    special_config: Dict[str, Any] = field(default_factory=dict)

class ConfigManager:
    """統一配置管理器"""
    
    def __init__(self, pipeline_mode: str = "separate", station: Optional[str] = None):
        self.pipeline_mode = pipeline_mode
        self.mode = pipeline_mode  # 向後兼容性
        self.station = station
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 載入配置
        self.base_config = self._load_base_config()
        self.model_config = self._load_model_config()
        self.pipeline_config = self._load_pipeline_config(pipeline_mode)
        self.station_config = self._load_station_config()
        
        # 創建配置對象
        self.paths = self._create_path_config()
        self.time_settings = self._create_time_config()
        self.time_config = self.time_settings  # 向後兼容性
        self.hardware = self._create_hardware_config()
        self.performance_config = self.hardware  # 向後兼容性
        self.metrics = self._create_metrics_config()
        self.lightgbm = self._create_lightgbm_config()
        self.lstm = self._create_lstm_config()
        
        # 設置日志
        self.logger = self._setup_logger()
        
    def _load_yaml(self, file_path: Path) -> Dict[str, Any]:
        """載入YAML文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            self.logger.warning(f"配置文件不存在: {file_path}")
            return {}
        except yaml.YAMLError as e:
            self.logger.error(f"YAML格式錯誤: {e}")
            return {}
    
    def _load_base_config(self) -> Dict[str, Any]:
        """載入基礎配置"""
        return self._load_yaml(CONFIGS_DIR / "base_config.yaml")
    
    def _load_model_config(self) -> Dict[str, Any]:
        """載入模型配置"""
        return self._load_yaml(CONFIGS_DIR / "model_configs.yaml")
    
    def _load_pipeline_config(self, pipeline_mode: str) -> PipelineConfig:
        """載入管道配置"""
        config_file = CONFIGS_DIR / "pipelines" / f"{pipeline_mode}.yaml"
        config_dict = self._load_yaml(config_file)
        
        if config_dict:
            # 判斷是否為標準化模式
            is_normalized = "norm" in pipeline_mode or config_dict.get("is_normalized", False)
            
            return PipelineConfig(
                name=config_dict.get("name", pipeline_mode),
                description=config_dict.get("description", f"{pipeline_mode} pipeline"),
                type=config_dict.get("type", "station_specific"),
                data_source=config_dict.get("data_source", {}),
                preprocessing=config_dict.get("preprocessing", {}),
                output_paths=config_dict.get("output_paths", {}),
                training=config_dict.get("training", {}),
                is_normalized=is_normalized,
                special_config=config_dict.get("special_config", {})
            )
        else:
            # 回退到默認配置
            is_normalized = "norm" in pipeline_mode
            return PipelineConfig(
                name=pipeline_mode,
                description=f"{pipeline_mode} pipeline",
                type="station_specific" if pipeline_mode.startswith("separate") else "global",
                data_source={},
                preprocessing={},
                output_paths={},
                training={},
                is_normalized=is_normalized,
                special_config={}
            )
    
    def _load_station_config(self) -> Dict[str, Any]:
        """載入測站配置"""
        return self._load_yaml(CONFIGS_DIR / "stations" / "station_list.yaml")
    
    def _create_path_config(self) -> PathConfig:
        """創建路徑配置"""
        base_paths = self.base_config.get("paths", {})
        
        # 根據管道模式調整路徑
        pipeline_paths = self.pipeline_config.output_paths
        
        return PathConfig(
            data_raw=PROJECT_ROOT / base_paths.get("data", {}).get("raw", "data/raw"),
            data_processed=PROJECT_ROOT / pipeline_paths.get("processed_data", "data/processed"),
            data_windows=PROJECT_ROOT / pipeline_paths.get("windows_data", "data/windows"),
            
            models_lightgbm=PROJECT_ROOT / pipeline_paths.get("models", {}).get("lightgbm", "models/lightgbm"),
            models_lstm=PROJECT_ROOT / pipeline_paths.get("models", {}).get("lstm", "models/lstm"),
            
            outputs_reports=PROJECT_ROOT / pipeline_paths.get("reports", "outputs/reports"),
            outputs_predictions=PROJECT_ROOT / base_paths.get("outputs", {}).get("predictions", "outputs/predictions"),
            outputs_evaluations=PROJECT_ROOT / base_paths.get("outputs", {}).get("evaluations", "outputs/evaluations"),
            outputs_comparisons=PROJECT_ROOT / base_paths.get("outputs", {}).get("comparisons", "outputs/comparisons"),
            
            logs_training=PROJECT_ROOT / base_paths.get("logs", {}).get("training", "logs/training"),
            logs_preprocessing=PROJECT_ROOT / base_paths.get("logs", {}).get("preprocessing", "logs/preprocessing"),
            logs_evaluation=PROJECT_ROOT / base_paths.get("logs", {}).get("evaluation", "logs/evaluation"),
            logs_system=PROJECT_ROOT / base_paths.get("logs", {}).get("system", "logs/system")
        )
    
    def _create_time_config(self) -> TimeConfig:
        """創建時間配置"""
        time_settings = self.base_config.get("time_settings", {})
        return TimeConfig(**time_settings)
    
    def _create_hardware_config(self) -> HardwareConfig:
        """創建硬體配置"""
        hardware_settings = self.base_config.get("hardware", {})
        
        # 智能設備檢測
        if hardware_settings.get("device") == "auto":
            try:
                import torch
                device = "cuda" if torch.cuda.is_available() else "cpu"
                hardware_settings["device"] = device
            except ImportError:
                hardware_settings["device"] = "cpu"
        
        return HardwareConfig(**hardware_settings)
    
    def _create_metrics_config(self) -> MetricsConfig:
        """創建評估指標配置"""
        metrics_settings = self.base_config.get("metrics", {})
        return MetricsConfig(**metrics_settings)
    
    def _create_lightgbm_config(self) -> LightGBMConfig:
        """創建LightGBM配置"""
        lgbm_settings = self.model_config.get("lightgbm", {})
        return LightGBMConfig(**lgbm_settings)
    
    def _create_lstm_config(self) -> LSTMConfig:
        """創建LSTM配置"""
        lstm_settings = self.model_config.get("lstm", {})
        
        # 處理嵌套配置
        architecture = lstm_settings.get("architecture", {})
        training = lstm_settings.get("training", {})
        
        # 合併配置
        merged_config = {**architecture, **training}
        merged_config.update({k: v for k, v in lstm_settings.items() 
                             if k not in ["architecture", "training", "optimizer", "scheduler", "regularization"]})
        
        return LSTMConfig(**merged_config)
    
    def _setup_logger(self) -> logging.Logger:
        """設置日志"""
        logger = logging.getLogger(f"config_{self.pipeline_mode}_{self.station or 'global'}")
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                self.base_config.get("logging", {}).get("format", 
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
            level = self.base_config.get("logging", {}).get("level", "INFO")
            logger.setLevel(getattr(logging, level))
        
        return logger
    
    def get_output_file_path(self, file_type: str, model_type: Optional[str] = None) -> Path:
        """獲取輸出文件路徑"""
        base_name = f"{self.pipeline_mode}"
        if self.station:
            base_name += f"_{self.station}"
        base_name += f"_{self.timestamp}"
        
        if file_type == "processed_data":
            return self.paths.data_processed / f"{base_name}_processed.npz"
        elif file_type == "windows_data_npz":
            return self.paths.data_windows / f"{base_name}_windows.npz"
        elif file_type == "windows_data_pt":
            return self.paths.data_windows / f"{base_name}_windows.pt"
        elif file_type == "model" and model_type:
            if model_type == "lightgbm":
                return self.paths.models_lightgbm / f"{base_name}_lgbm.pkl"
            elif model_type == "lstm":
                return self.paths.models_lstm / f"{base_name}_lstm.pt"
        elif file_type == "evaluation_report":
            return self.paths.outputs_reports / f"{base_name}_evaluation.json"
        elif file_type == "comparison_report":
            return self.paths.outputs_reports / f"{base_name}_comparison.md"
        elif file_type == "log_file":
            return self.paths.logs_training / f"{base_name}_training.log"
        
        raise ValueError(f"不支援的文件類型: {file_type}")
    
    def get_output_paths(self) -> Dict[str, Path]:
        """獲取輸出路徑（向後兼容性）"""
        base_name = f"{self.pipeline_mode}"
        if self.station:
            base_name += f"_{self.station}"
        base_name += f"_{self.timestamp}"
        
        return {
            'processed_data': self.paths.data_processed / f"{base_name}_processed.npz",
            'windows_data_npz': self.paths.data_windows / f"{base_name}_windows.npz",
            'windows_data_pt': self.paths.data_windows / f"{base_name}_windows.pt",
            'lgbm_model': self.paths.models_lightgbm / f"{base_name}_lgbm.pkl",
            'lstm_model': self.paths.models_lstm / f"{base_name}_lstm.pt",
            'evaluation_report': self.paths.outputs_reports / f"{base_name}_evaluation.json",
            'comparison_report': self.paths.outputs_reports / f"{base_name}_comparison.md",
            'log_file': self.paths.logs_training / f"{base_name}_training.log"
        }
    
    def get_input_paths(self) -> Union[Path, List[Path]]:
        """獲取輸入路徑（向後兼容性）"""
        # 從管道配置獲取數據源信息
        data_source = self.pipeline_config.data_source
        
        if self.pipeline_mode == "combine":
            # combine模式 - 單一文件
            return self.paths.data_raw / "Combine/Combine_AllData.csv"
        elif self.pipeline_mode == "combine_norm":
            # combine_norm模式 - 單一標準化文件
            return self.paths.data_raw / "Combine_Nomolization/Nomorlization_Combine_AllData.csv"
        elif self.pipeline_mode == "separate":
            # separate模式 - 測站特定文件
            if self.station:
                # 查找以測站名稱開頭的文件
                pattern = f"{self.station}_*_combined.csv"
                matching_files = list((self.paths.data_raw / "Separate").glob(pattern))
                if matching_files:
                    return matching_files[0]  # 返回第一個匹配的文件
                else:
                    raise ValueError(f"找不到測站 {self.station} 的數據文件")
            else:
                # 所有測站文件
                return list((self.paths.data_raw / "Separate").glob("*_combined.csv"))
        elif self.pipeline_mode == "separate_norm":
            # separate_norm模式 - 標準化測站文件
            if self.station:
                # 查找以測站名稱開頭的標準化文件
                # 修復：Nomorlization檔名格式為 Nomorlization_站名_代碼_combined.csv
                pattern = f"Nomorlization_{self.station}_*_combined.csv"
                matching_files = list((self.paths.data_raw / "Separate_Nomorlization").glob(pattern))
                if matching_files:
                    return matching_files[0]  # 返回第一個匹配的文件
                else:
                    # 回退：嘗試標準格式
                    pattern = f"{self.station}_*_combined.csv"
                    matching_files = list((self.paths.data_raw / "Separate_Nomorlization").glob(pattern))
                    if matching_files:
                        return matching_files[0]
                    else:
                        raise ValueError(f"找不到測站 {self.station} 的標準化數據文件")
            else:
                # 所有標準化測站文件
                return list((self.paths.data_raw / "Separate_Nomorlization").glob("*_combined.csv"))
        elif self.pipeline_mode == "station_specific":
            # station_specific模式 - 指定測站的多個文件
            if self.station:
                raw_files = []
                # 原始數據
                pattern = f"{self.station}_*_combined.csv"
                separate_files = list((self.paths.data_raw / "Separate").glob(pattern))
                if separate_files:
                    raw_files.extend(separate_files)
                # 標準化數據
                norm_files = list((self.paths.data_raw / "Separate_Nomorlization").glob(pattern))
                if norm_files:
                    raw_files.extend(norm_files)
                return raw_files if raw_files else [separate_files[0]] if separate_files else []
            else:
                raise ValueError("station_specific模式需要指定測站")
        else:
            raise ValueError(f"不支援的管道模式: {self.pipeline_mode}")
    
    def get_station_list(self, category: Optional[str] = None) -> List[str]:
        """獲取測站列表"""
        if category:
            return self.station_config.get("default_stations", {}).get(category, [])
        
        # 返回所有測站
        all_stations = []
        stations_config = self.station_config.get("stations", {})
        for category_stations in stations_config.values():
            if isinstance(category_stations, list):
                for station in category_stations:
                    if isinstance(station, dict) and "name" in station:
                        all_stations.append(station["name"])
        
        return all_stations
    
    def get_station_info(self, station_name: str) -> Optional[Dict[str, Any]]:
        """獲取特定測站信息"""
        stations_config = self.station_config.get("stations", {})
        for category_stations in stations_config.values():
            if isinstance(category_stations, list):
                for station in category_stations:
                    if isinstance(station, dict) and station.get("name") == station_name:
                        return station
        return None
    
    def save_config(self, output_path: Optional[Path] = None):
        """保存當前配置到文件"""
        if output_path is None:
            output_path = self.get_output_file_path("config")
        
        config_dict = {
            "pipeline_mode": self.pipeline_mode,
            "station": self.station,
            "timestamp": self.timestamp,
            "base_config": self.base_config,
            "model_config": self.model_config,
            "pipeline_config": self.pipeline_config,
            "station_config": self.station_config
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(config_dict, f, ensure_ascii=False, indent=2)
        
        self.logger.info(f"配置已保存到: {output_path}")
    
    def to_dict(self) -> Dict[str, Any]:
        """轉換為字典格式（向後兼容性）"""
        return {
            'mode': self.mode,
            'pipeline_mode': self.pipeline_mode,
            'station': self.station,
            'timestamp': self.timestamp,
            'pipeline_config': {
                'name': self.pipeline_config.name,
                'description': self.pipeline_config.description,
                'type': self.pipeline_config.type,
                'data_source': self.pipeline_config.data_source,
                'preprocessing': self.pipeline_config.preprocessing,
                'output_paths': self.pipeline_config.output_paths,
                'training': self.pipeline_config.training,
                'is_normalized': self.pipeline_config.is_normalized,
                'special_config': self.pipeline_config.special_config,
            },
            'base_config': self.base_config,
            'model_config': self.model_config,
            'station_config': self.station_config
        }
    
    def __str__(self) -> str:
        return f"ConfigManager(pipeline={self.pipeline_mode}, station={self.station}, timestamp={self.timestamp})"

# 便利函數
def create_config_manager(pipeline_mode: str = "separate", 
                         station: Optional[str] = None) -> ConfigManager:
    """創建配置管理器的便利函數"""
    return ConfigManager(pipeline_mode=pipeline_mode, station=station)

def get_available_pipelines() -> List[str]:
    """獲取可用的管道模式"""
    pipelines_dir = CONFIGS_DIR / "pipelines"
    if pipelines_dir.exists():
        return [f.stem for f in pipelines_dir.glob("*.yaml")]
    return []

def get_available_stations() -> List[str]:
    """獲取可用的測站列表"""
    config_manager = ConfigManager()
    return config_manager.get_station_list()

if __name__ == "__main__":
    # 測試配置管理器
    config_manager = create_config_manager("separate", "桃園")
    print(config_manager)
    print(f"可用管道: {get_available_pipelines()}")
    print(f"可用測站: {get_available_stations()}") 