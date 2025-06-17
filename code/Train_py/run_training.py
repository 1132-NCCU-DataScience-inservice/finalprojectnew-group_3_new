#!/usr/bin/env python3
"""
AQI預測系統 - 主執行腳本 (重構版)
Main Training Script with New Configuration System
"""

import sys
import argparse
import logging
from pathlib import Path
from typing import List, Optional
import json
from datetime import datetime

# 添加src目錄到路徑
sys.path.append(str(Path(__file__).parent / "src"))

from src.config_manager import create_config_manager, get_available_pipelines, get_available_stations
from src.unified_config import UnifiedConfig
from src.unified_preprocessor import UnifiedPreprocessor  
from src.unified_window_generator import UnifiedWindowGenerator
from src.unified_trainer import UnifiedTrainer

def setup_logging() -> logging.Logger:
    """設置日志"""
    logger = logging.getLogger("aqi_training_main")
    
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    
    return logger

def train_single_pipeline_station(pipeline_mode: str, station: Optional[str] = None) -> dict:
    """訓練單個管道-測站組合"""
    logger = logging.getLogger(f"train_{pipeline_mode}_{station or 'global'}")
    
    try:
        # 創建統一配置
        config = UnifiedConfig(mode=pipeline_mode, station=station)
        logger.info(f"開始訓練: {config}")
        
        # 1. 數據預處理
        logger.info("步驟1: 數據預處理")
        preprocessor = UnifiedPreprocessor(config)
        preprocessor.process_full_pipeline()
        logger.info("✅ 預處理完成")
        
        # 2. 時間窗口生成
        logger.info("步驟2: 時間窗口生成")
        window_generator = UnifiedWindowGenerator(config)
        window_generator.process_full_pipeline()
        logger.info("✅ 窗口生成完成")
        
        # 3. 模型訓練
        logger.info("步驟3: 模型訓練")
        trainer = UnifiedTrainer(config)
        training_results = trainer.train_all_models()
        logger.info("✅ 模型訓練完成")
        
        # 4. 結果彙整
        result = {
            "pipeline_mode": pipeline_mode,
            "station": station,
            "timestamp": config.timestamp,
            "success": True,
            "models": training_results,
            "config_summary": {
                "time_settings": {
                    "window_size": config.time_config.window_size,
                    "horizon": config.time_config.horizon,
                    "train_ratio": config.time_config.train_ratio
                },
                "hardware": {
                    "use_gpu": config.performance_config.use_gpu,
                    "device": config.performance_config.device
                }
            }
        }
        
        logger.info(f"✅ 訓練成功完成: {pipeline_mode} - {station or 'global'}")
        return result
        
    except Exception as e:
        error_msg = f"訓練失敗: {pipeline_mode} - {station or 'global'}: {e}"
        logger.error(error_msg)
        return {
            "pipeline_mode": pipeline_mode,
            "station": station,
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S")
        }

def train_pipeline_mode(pipeline_mode: str, stations: Optional[List[str]] = None) -> dict:
    """訓練特定管道模式"""
    logger = logging.getLogger(f"train_pipeline_{pipeline_mode}")
    
    # 確定要訓練的測站
    if pipeline_mode in ["combine", "combine_norm"]:
        # 全域模式，不需要指定測站
        stations_to_train = [None]
    else:
        # 測站特定模式
        if stations is None:
            # 獲取所有可用測站列表（從實際數據文件）
            if pipeline_mode == "separate":
                separate_dir = Path("data/raw/Separate")
                if separate_dir.exists():
                    station_files = list(separate_dir.glob("*_combined.csv"))
                    stations_to_train = [f.stem.split('_')[0] for f in station_files]
                    logger.info(f"從 Separate 目錄發現 {len(stations_to_train)} 個測站")
                else:
                    logger.error(f"Separate 目錄不存在: {separate_dir}")
                    stations_to_train = []
            elif pipeline_mode == "separate_norm":
                separate_norm_dir = Path("data/raw/Separate_Nomorlization")
                if separate_norm_dir.exists():
                    station_files = list(separate_norm_dir.glob("*_combined.csv"))
                    # 修復：Nomorlization檔名格式為 Nomorlization_站名_代碼_combined.csv
                    stations_to_train = []
                    for f in station_files:
                        parts = f.stem.split('_')
                        if len(parts) >= 3 and parts[0] == "Nomorlization":
                            # 檔名格式：Nomorlization_站名_代碼_combined
                            station_name = parts[1]
                            stations_to_train.append(station_name)
                        else:
                            # 回退：假設為標準格式 站名_代碼_combined
                            station_name = parts[0] if parts else f.stem
                            stations_to_train.append(station_name)
                    
                    # 去重並排序
                    stations_to_train = sorted(list(set(stations_to_train)))
                    logger.info(f"從 Separate_Nomorlization 目錄發現 {len(stations_to_train)} 個測站")
                else:
                    logger.error(f"Separate_Nomorlization 目錄不存在: {separate_norm_dir}")
                    stations_to_train = []
            else:
                # 其他模式，暫時使用空列表（需要後續實現）
                logger.warning(f"模式 {pipeline_mode} 的測站發現尚未實現，使用空列表")
                stations_to_train = []
        else:
            stations_to_train = stations
    
    results = []
    for station in stations_to_train:
        logger.info(f"開始訓練: {pipeline_mode} - {station or 'global'}")
        result = train_single_pipeline_station(pipeline_mode, station)
        results.append(result)
    
    # 彙總結果
    successful_runs = [r for r in results if r.get("success", False)]
    failed_runs = [r for r in results if not r.get("success", False)]
    
    summary = {
        "pipeline_mode": pipeline_mode,
        "total_runs": len(results),
        "successful_runs": len(successful_runs),
        "failed_runs": len(failed_runs),
        "success_rate": len(successful_runs) / len(results) if results else 0,
        "results": results,
        "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S")
    }
    
    logger.info(f"管道訓練完成: {pipeline_mode}")
    logger.info(f"成功: {len(successful_runs)}/{len(results)} ({summary['success_rate']:.1%})")
    
    return summary

def batch_training(pipeline_modes: List[str], stations: Optional[List[str]] = None) -> dict:
    """批量訓練多個管道模式"""
    logger = logging.getLogger("batch_training")
    logger.info("🚀 開始批量訓練")
    logger.info(f"管道模式: {pipeline_modes}")
    logger.info(f"測站: {stations or '預設'}")
    
    all_results = {}
    
    for pipeline_mode in pipeline_modes:
        logger.info(f"=" * 60)
        logger.info(f"開始執行管道模式: {pipeline_mode}")
        
        pipeline_result = train_pipeline_mode(pipeline_mode, stations)
        all_results[pipeline_mode] = pipeline_result
        
        if pipeline_result["success_rate"] > 0:
            logger.info(f"✅ {pipeline_mode} 完成 ({pipeline_result['success_rate']:.1%} 成功)")
        else:
            logger.error(f"❌ {pipeline_mode} 全部失敗")
    
    # 生成總結報告
    total_runs = sum(r["total_runs"] for r in all_results.values())
    total_successful = sum(r["successful_runs"] for r in all_results.values())
    
    batch_summary = {
        "batch_training": True,
        "pipeline_modes": pipeline_modes,
        "stations": stations,
        "total_runs": total_runs,
        "successful_runs": total_successful,
        "overall_success_rate": total_successful / total_runs if total_runs > 0 else 0,
        "pipeline_results": all_results,
        "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S")
    }
    
    logger.info("=" * 60)
    logger.info("🎉 批量訓練完成!")
    logger.info(f"總體成功率: {batch_summary['overall_success_rate']:.1%} ({total_successful}/{total_runs})")
    
    return batch_summary

def save_results(results: dict, output_dir: str = "outputs/reports"):
    """保存訓練結果"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    timestamp = results.get("timestamp", datetime.now().strftime("%Y%m%d_%H%M%S"))
    
    if results.get("batch_training", False):
        filename = f"batch_training_results_{timestamp}.json"
    else:
        pipeline = results.get("pipeline_mode", "unknown")
        filename = f"{pipeline}_training_results_{timestamp}.json"
    
    output_file = output_path / filename
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"📊 結果已保存: {output_file}")
    return output_file

def main():
    """主函數"""
    parser = argparse.ArgumentParser(
        description="AQI預測系統 - 統一訓練執行器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用範例:
  # 訓練單個管道模式
  python run_training.py --mode separate --stations 桃園 台北
  
  # 訓練多個管道模式
  python run_training.py --modes separate combine --stations 桃園
  
  # 批量訓練所有模式
  python run_training.py --modes all
  
  # 驗證配置
  python run_training.py --validate --mode separate --stations 桃園
        """
    )
    
    # 管道選擇參數
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        "--mode", 
        choices=get_available_pipelines() + ["all"],
        help="單個管道模式"
    )
    mode_group.add_argument(
        "--modes", 
        nargs="+",
        choices=get_available_pipelines() + ["all"],
        help="多個管道模式"
    )
    
    # 測站參數
    parser.add_argument(
        "--stations",
        nargs="+",
        help="指定測站列表"
    )
    
    # 其他參數
    parser.add_argument(
        "--validate",
        action="store_true",
        help="僅驗證配置，不執行訓練"
    )
    
    parser.add_argument(
        "--output-dir",
        default="outputs/reports",
        help="結果輸出目錄"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="詳細輸出"
    )
    
    args = parser.parse_args()
    
    # 設置日志
    logger = setup_logging()
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    # 確定要執行的管道模式
    if args.mode:
        pipeline_modes = [args.mode] if args.mode != "all" else get_available_pipelines()
    elif args.modes:
        if "all" in args.modes:
            pipeline_modes = get_available_pipelines()
        else:
            pipeline_modes = args.modes
    else:
        pipeline_modes = ["separate"]  # 預設模式
    
    # 驗證測站
    if args.stations:
        available_stations = get_available_stations()
        for station in args.stations:
            if station not in available_stations:
                logger.error(f"測站不存在: {station}")
                logger.info(f"可用測站: {available_stations}")
                sys.exit(1)
    
    # 僅驗證模式
    if args.validate:
        logger.info("🔍 配置驗證模式")
        for pipeline_mode in pipeline_modes:
            try:
                config = UnifiedConfig(mode=pipeline_mode, station=args.stations[0] if args.stations else None)
                logger.info(f"✅ {pipeline_mode}: 配置有效")
                logger.info(f"   時間設置: {config.time_config.window_size}h -> {config.time_config.horizon}h")
                logger.info(f"   硬體設置: GPU={config.performance_config.use_gpu}")
            except Exception as e:
                logger.error(f"❌ {pipeline_mode}: 配置無效 - {e}")
        return
    
    # 執行訓練
    try:
        if len(pipeline_modes) == 1:
            # 單個管道模式
            results = train_pipeline_mode(pipeline_modes[0], args.stations)
        else:
            # 批量訓練
            results = batch_training(pipeline_modes, args.stations)
        
        # 保存結果
        output_file = save_results(results, args.output_dir)
        
        # 顯示摘要
        if results.get("batch_training", False):
            success_rate = results["overall_success_rate"]
        else:
            success_rate = results["success_rate"]
        
        if success_rate > 0.8:
            logger.info("🎉 訓練圓滿完成!")
        elif success_rate > 0.5:
            logger.warning("⚠️ 訓練部分成功")
        else:
            logger.error("❌ 訓練大部分失敗")
        
        sys.exit(0 if success_rate > 0 else 1)
        
    except KeyboardInterrupt:
        logger.info("⏹️ 訓練被用戶中斷")
        sys.exit(130)
    except Exception as e:
        logger.error(f"💥 訓練執行失敗: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 