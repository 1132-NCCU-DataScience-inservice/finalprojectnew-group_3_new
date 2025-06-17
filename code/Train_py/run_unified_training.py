#!/usr/bin/env python3
"""
AQI 預測系統 - 統一訓練執行腳本
支援5種標準化訓練模式，移除桃園專用代碼，符合研究標準
"""

import os
import sys
import logging
import argparse
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

# 添加項目根目錄到Python路徑
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 導入統一配置和模組
from src.unified_config import (
    UnifiedConfig, ConfigFactory, validate_research_standards,
    ALL_MODES, STATION_REQUIRED_MODES, GLOBAL_MODES
)
from src.unified_preprocessor import preprocess_data_by_mode, batch_preprocess
from src.unified_window_generator import generate_windows_by_mode, batch_generate_windows
from src.unified_trainer import train_models_by_mode, batch_train_models

# 設置日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(f'unified_training_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

def detect_available_stations() -> List[str]:
    """檢測可用的測站"""
    stations = set()
    
    # 從原始數據目錄檢測
    separate_dir = Path("data/raw/Separate")
    if separate_dir.exists():
        for file in separate_dir.glob("*_combined.csv"):
            station = file.stem.split('_')[0]
            stations.add(station)
    
    separate_norm_dir = Path("data/raw/Separate_Nomorlization")
    if separate_norm_dir.exists():
        for file in separate_norm_dir.glob("*_combined.csv"):
            station = file.stem.split('_')[0]
            stations.add(station)
    
    return sorted(list(stations))

def run_mode_combine(mode: str) -> Dict:
    """運行合併模式（combine 或 combine_norm）"""
    logger.info(f"=" * 60)
    logger.info(f"開始執行模式: {mode}")
    logger.info(f"=" * 60)
    
    try:
        # 步驟1: 數據預處理
        logger.info("步驟1: 數據預處理")
        preprocess_result = preprocess_data_by_mode(mode)
        logger.info("✅ 數據預處理完成")
        
        # 步驟2: 時間窗口生成
        logger.info("步驟2: 時間窗口生成")
        windows_result = generate_windows_by_mode(mode)
        logger.info("✅ 時間窗口生成完成")
        
        # 步驟3: 模型訓練
        logger.info("步驟3: 模型訓練")
        training_result = train_models_by_mode(mode)
        logger.info("✅ 模型訓練完成")
        
        return {
            'status': 'success',
            'mode': mode,
            'preprocess': preprocess_result,
            'windows': windows_result,
            'training': training_result
        }
        
    except Exception as e:
        logger.error(f"❌ 模式 {mode} 執行失敗: {e}")
        return {
            'status': 'failed',
            'mode': mode,
            'error': str(e)
        }

def run_mode_separate(mode: str, stations: Optional[List[str]] = None) -> Dict:
    """運行分離模式（separate 或 separate_norm）"""
    logger.info(f"=" * 60)
    logger.info(f"開始執行模式: {mode}")
    logger.info(f"=" * 60)
    
    if stations is None:
        stations = detect_available_stations()
    
    if not stations:
        return {
            'status': 'failed',
            'mode': mode,
            'error': '未檢測到可用的測站數據'
        }
    
    logger.info(f"處理 {len(stations)} 個測站: {stations}")
    
    try:
        # 批量處理所有步驟
        logger.info("步驟1: 批量數據預處理")
        preprocess_results = batch_preprocess([mode], stations)
        logger.info("✅ 批量數據預處理完成")
        
        logger.info("步驟2: 批量時間窗口生成")
        windows_results = batch_generate_windows([mode], stations)
        logger.info("✅ 批量時間窗口生成完成")
        
        logger.info("步驟3: 批量模型訓練")
        training_results = batch_train_models([mode], stations)
        logger.info("✅ 批量模型訓練完成")
        
        # 統計成功失敗
        successful = []
        failed = []
        
        for station in stations:
            key = f"{mode}_{station}"
            if key in training_results and isinstance(training_results[key], dict) and 'error' not in training_results[key]:
                successful.append(station)
            else:
                failed.append(station)
        
        return {
            'status': 'success' if not failed else 'partial',
            'mode': mode,
            'total_stations': len(stations),
            'successful_stations': successful,
            'failed_stations': failed,
            'preprocess': preprocess_results,
            'windows': windows_results,
            'training': training_results
        }
        
    except Exception as e:
        logger.error(f"❌ 模式 {mode} 執行失敗: {e}")
        return {
            'status': 'failed',
            'mode': mode,
            'error': str(e)
        }

def run_mode_station_specific(target_stations: List[str]) -> Dict:
    """運行指定測站模式"""
    logger.info(f"=" * 60)
    logger.info(f"開始執行指定測站模式: {target_stations}")
    logger.info(f"=" * 60)
    
    available_stations = detect_available_stations()
    invalid_stations = [s for s in target_stations if s not in available_stations]
    
    if invalid_stations:
        return {
            'status': 'failed',
            'error': f'指定的測站不可用: {invalid_stations}. 可用測站: {available_stations}'
        }
    
    results = {}
    
    for station in target_stations:
        logger.info(f"處理測站: {station}")
        
        for mode in ['separate', 'separate_norm']:
            mode_key = f"{station}_{mode}"
            logger.info(f"  執行模式: {mode}")
            
            try:
                # 完整流程
                preprocess_result = preprocess_data_by_mode(mode, station)
                windows_result = generate_windows_by_mode(mode, station)
                training_result = train_models_by_mode(mode, station)
                
                results[mode_key] = {
                    'status': 'success',
                    'station': station,
                    'mode': mode,
                    'preprocess': preprocess_result,
                    'windows': windows_result,
                    'training': training_result
                }
                logger.info(f"  ✅ {mode} 完成")
                
            except Exception as e:
                logger.error(f"  ❌ {mode} 失敗: {e}")
                results[mode_key] = {
                    'status': 'failed',
                    'station': station,
                    'mode': mode,
                    'error': str(e)
                }
    
    successful = sum(1 for r in results.values() if r['status'] == 'success')
    
    return {
        'status': 'success' if successful == len(results) else 'partial',
        'target_stations': target_stations,
        'total_tasks': len(results),
        'successful_tasks': successful,
        'results': results
    }

def main():
    """主執行函數"""
    parser = argparse.ArgumentParser(description='AQI預測系統 - 統一訓練執行器')
    
    parser.add_argument('--mode', choices=['all', 'combine', 'combine_norm', 'separate', 'separate_norm', 'station_specific'],
                       default='all', help='執行模式')
    parser.add_argument('--stations', nargs='+', help='指定測站列表')
    parser.add_argument('--validate', action='store_true', help='僅驗證配置不執行訓練')
    
    args = parser.parse_args()
    
    logger.info("🚀 AQI預測系統 - 統一訓練開始")
    logger.info(f"執行模式: {args.mode}")
    
    # 檢測可用測站
    available_stations = detect_available_stations()
    logger.info(f"可用測站: {available_stations}")
    
    if args.validate:
        # 驗證模式
        logger.info("🔍 驗證研究標準配置...")
        
        modes_to_validate = ALL_MODES if args.mode == 'all' else [args.mode]
        
        for mode in modes_to_validate:
            if mode in STATION_REQUIRED_MODES:
                stations = args.stations or available_stations
                for station in stations:
                    config = UnifiedConfig(mode=mode, station=station)
                    validations = validate_research_standards(config)
                    logger.info(f"{mode}_{station}: {validations}")
            else:
                config = UnifiedConfig(mode=mode)
                validations = validate_research_standards(config)
                logger.info(f"{mode}: {validations}")
        
        return
    
    # 執行訓練
    results = {}
    start_time = datetime.now()
    
    try:
        if args.mode == 'all':
            # 執行所有5種模式
            logger.info("🎯 執行完整的5種標準化訓練模式")
            
            # 模式1: combine
            results['mode_1_combine'] = run_mode_combine('combine')
            
            # 模式2: combine_norm
            results['mode_2_combine_norm'] = run_mode_combine('combine_norm')
            
            # 模式3: separate (所有測站)
            results['mode_3_separate_all'] = run_mode_separate('separate')
            
            # 模式4: separate_norm (所有測站)
            results['mode_4_separate_norm_all'] = run_mode_separate('separate_norm')
            
            # 模式5: station_specific (如果指定了測站)
            if args.stations:
                results['mode_5_station_specific'] = run_mode_station_specific(args.stations)
        
        elif args.mode in ['combine', 'combine_norm']:
            results[args.mode] = run_mode_combine(args.mode)
        
        elif args.mode in ['separate', 'separate_norm']:
            results[args.mode] = run_mode_separate(args.mode, args.stations)
        
        elif args.mode == 'station_specific':
            if not args.stations:
                logger.error("❌ station_specific 模式需要指定 --stations 參數")
                return
            results['station_specific'] = run_mode_station_specific(args.stations)
        
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds()
        
        # 生成摘要
        logger.info("=" * 80)
        logger.info("🎉 執行完成!")
        logger.info(f"⏱️  總執行時間: {execution_time:.2f} 秒")
        
        # 統計結果
        total_modes = len(results)
        successful_modes = sum(1 for r in results.values() if r.get('status') == 'success')
        
        logger.info(f"📊 成功模式: {successful_modes}/{total_modes}")
        
        for mode_name, result in results.items():
            status = result.get('status', 'unknown')
            if status == 'success':
                logger.info(f"  ✅ {mode_name}")
            elif status == 'partial':
                logger.info(f"  ⚠️  {mode_name} (部分成功)")
            else:
                logger.info(f"  ❌ {mode_name} - {result.get('error', '未知錯誤')}")
        
        # 保存結果
        output_file = f"unified_training_results_{start_time.strftime('%Y%m%d_%H%M%S')}.json"
        import json
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                'execution_info': {
                    'start_time': start_time.isoformat(),
                    'end_time': end_time.isoformat(),
                    'execution_time': execution_time,
                    'mode': args.mode,
                    'stations': args.stations,
                    'available_stations': available_stations
                },
                'results': results
            }, f, ensure_ascii=False, indent=2, default=str)
        
        logger.info(f"📁 結果已保存: {output_file}")
        logger.info("=" * 80)
        
    except Exception as e:
        logger.error(f"💥 執行過程中發生嚴重錯誤: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 