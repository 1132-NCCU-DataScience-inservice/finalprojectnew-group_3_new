#!/usr/bin/env python3
"""
完成所有測站separate pipeline的剩餘步驟
處理已完成預處理的數據，繼續進行時間窗口生成和模型訓練
"""

import os
import sys
import numpy as np
import logging
from pathlib import Path
from typing import List, Dict
from datetime import datetime
import glob

# 添加項目根目錄到Python路徑
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.unified_window_generator import generate_windows_by_mode
from src.unified_trainer import train_models_by_mode

# 設置日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(f'complete_separate_pipeline_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

def detect_preprocessed_stations() -> List[str]:
    """檢測已預處理的測站"""
    processed_dir = Path("data/processed")
    stations = set()
    
    # 尋找 separate_*_*_processed.npz 文件
    for file in processed_dir.glob("separate_*_*_processed.npz"):
        # 文件名格式: separate_測站名_時間戳_processed.npz
        parts = file.stem.split('_')
        if len(parts) >= 4:
            # 提取測站名（可能包含中文）
            station_part = '_'.join(parts[1:-2])  # 去掉 'separate' 和 時間戳_processed
            stations.add(station_part)
    
    return sorted(list(stations))

def find_latest_preprocessed_file(station: str) -> Path:
    """找到測站最新的預處理文件"""
    processed_dir = Path("data/processed")
    pattern = f"separate_{station}_*_processed.npz"
    files = list(processed_dir.glob(pattern))
    
    if not files:
        raise FileNotFoundError(f"未找到測站 {station} 的預處理文件")
    
    # 按修改時間排序，取最新的
    files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
    return files[0]

def process_station_windows(station: str) -> Dict:
    """處理單個測站的時間窗口生成"""
    try:
        logger.info(f"開始處理測站 {station} 的時間窗口生成")
        
        # 使用統一的時間窗口生成器，但指定特定的預處理文件
        preprocessed_file = find_latest_preprocessed_file(station)
        logger.info(f"使用預處理文件: {preprocessed_file}")
        
        # 直接調用時間窗口生成
        result = generate_windows_by_mode('separate', station)
        
        logger.info(f"✅ 測站 {station} 時間窗口生成成功")
        return {'status': 'success', 'result': result}
        
    except Exception as e:
        logger.error(f"❌ 測站 {station} 時間窗口生成失敗: {e}")
        return {'status': 'failed', 'error': str(e)}

def process_station_training(station: str) -> Dict:
    """處理單個測站的模型訓練"""
    try:
        logger.info(f"開始處理測站 {station} 的模型訓練")
        
        # 使用統一的模型訓練器
        result = train_models_by_mode('separate', station)
        
        logger.info(f"✅ 測站 {station} 模型訓練成功")
        return {'status': 'success', 'result': result}
        
    except Exception as e:
        logger.error(f"❌ 測站 {station} 模型訓練失敗: {e}")
        return {'status': 'failed', 'error': str(e)}

def main():
    """主執行函數"""
    logger.info("🚀 開始執行所有測站separate pipeline的剩餘步驟")
    
    # 檢測已預處理的測站
    stations = detect_preprocessed_stations()
    logger.info(f"檢測到 {len(stations)} 個已預處理的測站: {stations[:10]}...")  # 只顯示前10個
    
    if not stations:
        logger.error("❌ 未找到任何已預處理的測站數據")
        return
    
    # 統計結果
    windows_results = {}
    training_results = {}
    
    start_time = datetime.now()
    
    try:
        # 步驟1: 批量時間窗口生成
        logger.info(f"=" * 60)
        logger.info("步驟1: 批量時間窗口生成")
        logger.info(f"=" * 60)
        
        for i, station in enumerate(stations, 1):
            logger.info(f"[{i}/{len(stations)}] 處理測站: {station}")
            windows_results[station] = process_station_windows(station)
        
        # 統計時間窗口生成結果
        windows_success = sum(1 for r in windows_results.values() if r['status'] == 'success')
        logger.info(f"✅ 時間窗口生成完成: {windows_success}/{len(stations)} 成功")
        
        # 步驟2: 批量模型訓練（只處理時間窗口生成成功的測站）
        logger.info(f"=" * 60)
        logger.info("步驟2: 批量模型訓練")
        logger.info(f"=" * 60)
        
        successful_stations = [s for s, r in windows_results.items() if r['status'] == 'success']
        logger.info(f"將對 {len(successful_stations)} 個測站進行模型訓練")
        
        for i, station in enumerate(successful_stations, 1):
            logger.info(f"[{i}/{len(successful_stations)}] 訓練測站: {station}")
            training_results[station] = process_station_training(station)
        
        # 統計模型訓練結果
        training_success = sum(1 for r in training_results.values() if r['status'] == 'success')
        logger.info(f"✅ 模型訓練完成: {training_success}/{len(successful_stations)} 成功")
        
        # 生成最終報告
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds()
        
        logger.info("=" * 80)
        logger.info("🎉 所有測站separate pipeline執行完成!")
        logger.info(f"⏱️  總執行時間: {execution_time:.2f} 秒")
        logger.info(f"📊 處理統計:")
        logger.info(f"  - 總測站數: {len(stations)}")
        logger.info(f"  - 時間窗口生成成功: {windows_success}")
        logger.info(f"  - 模型訓練成功: {training_success}")
        logger.info(f"  - 完整pipeline成功: {training_success}")
        
        # 列出失敗的測站
        failed_windows = [s for s, r in windows_results.items() if r['status'] == 'failed']
        failed_training = [s for s, r in training_results.items() if r['status'] == 'failed']
        
        if failed_windows:
            logger.warning(f"⚠️  時間窗口生成失敗的測站 ({len(failed_windows)}): {failed_windows[:5]}...")
        
        if failed_training:
            logger.warning(f"⚠️  模型訓練失敗的測站 ({len(failed_training)}): {failed_training[:5]}...")
        
        # 保存詳細結果
        import json
        results = {
            'execution_info': {
                'start_time': start_time.isoformat(),
                'end_time': end_time.isoformat(),
                'execution_time': execution_time,
                'total_stations': len(stations)
            },
            'windows_results': windows_results,
            'training_results': training_results,
            'summary': {
                'windows_success': windows_success,
                'training_success': training_success,
                'failed_windows': failed_windows,
                'failed_training': failed_training
            }
        }
        
        output_file = f"complete_separate_pipeline_results_{start_time.strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2, default=str)
        
        logger.info(f"📁 詳細結果已保存: {output_file}")
        logger.info("=" * 80)
        
    except Exception as e:
        logger.error(f"💥 執行過程中發生嚴重錯誤: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 