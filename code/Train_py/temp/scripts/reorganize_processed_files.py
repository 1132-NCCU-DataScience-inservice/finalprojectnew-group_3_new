#!/usr/bin/env python3
"""
重新組織 processed 文件到正確的目錄結構
將分散在 data/processed/ 根目錄的文件移動到對應的子目錄
"""

import os
import shutil
from pathlib import Path
from typing import Dict, List
import logging
from datetime import datetime

# 設置日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(f'reorganize_files_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

class FileReorganizer:
    """文件重新組織器"""
    
    def __init__(self):
        self.processed_dir = Path("data/processed")
        self.backup_dir = Path("data/backup_processed")
        
        # 定義目標目錄結構
        self.target_dirs = {
            'separate': self.processed_dir / 'separate',
            'separate_norm': self.processed_dir / 'separate_norm', 
            'combine': self.processed_dir / 'combine',
            'combine_norm': self.processed_dir / 'combine_norm',
            'station_specific': self.processed_dir / 'station_specific'
        }
        
        # 創建目標目錄
        for dir_path in self.target_dirs.values():
            dir_path.mkdir(parents=True, exist_ok=True)
            
        # 創建備份目錄
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    def classify_file(self, file_path: Path) -> str:
        """根據文件名分類文件"""
        filename = file_path.name
        
        if filename.startswith('separate_norm_'):
            return 'separate_norm'
        elif filename.startswith('separate_'):
            return 'separate'
        elif filename.startswith('combine_norm_'):
            return 'combine_norm'
        elif filename.startswith('combine_'):
            return 'combine'
        elif filename.startswith('station_'):
            return 'station_specific'
        else:
            return 'unknown'
    
    def backup_file(self, file_path: Path) -> Path:
        """備份原文件"""
        backup_path = self.backup_dir / file_path.name
        shutil.copy2(file_path, backup_path)
        logger.info(f"備份文件: {file_path.name} -> {backup_path}")
        return backup_path
    
    def move_file(self, file_path: Path, target_category: str) -> bool:
        """移動文件到目標目錄"""
        try:
            if target_category == 'unknown':
                logger.warning(f"無法分類文件: {file_path.name}，跳過移動")
                return False
            
            target_dir = self.target_dirs[target_category]
            target_path = target_dir / file_path.name
            
            # 備份原文件
            self.backup_file(file_path)
            
            # 移動文件
            shutil.move(str(file_path), str(target_path))
            logger.info(f"移動文件: {file_path.name} -> {target_category}/")
            
            return True
            
        except Exception as e:
            logger.error(f"移動文件失敗 {file_path.name}: {e}")
            return False
    
    def get_files_to_reorganize(self) -> List[Path]:
        """獲取需要重新組織的文件列表"""
        files = []
        
        # 獲取所有需要重新組織的文件
        patterns = [
            'separate_*.npz',
            'separate_norm_*.npz', 
            'combine_*.npz',
            'combine_norm_*.npz',
            'station_*.npz',
            'separate_scaler.pkl'
        ]
        
        for pattern in patterns:
            files.extend(self.processed_dir.glob(pattern))
        
        # 過濾掉已經在子目錄中的文件
        root_files = [f for f in files if f.parent == self.processed_dir]
        
        logger.info(f"找到 {len(root_files)} 個需要重新組織的文件")
        return root_files
    
    def reorganize_all(self) -> Dict[str, int]:
        """重新組織所有文件"""
        logger.info("🚀 開始重新組織 processed 文件")
        
        files_to_move = self.get_files_to_reorganize()
        
        if not files_to_move:
            logger.info("沒有需要重新組織的文件")
            return {}
        
        # 統計結果
        results = {
            'separate': 0,
            'separate_norm': 0,
            'combine': 0, 
            'combine_norm': 0,
            'station_specific': 0,
            'unknown': 0,
            'failed': 0
        }
        
        for file_path in files_to_move:
            logger.info(f"處理文件: {file_path.name}")
            
            # 分類文件
            category = self.classify_file(file_path)
            
            if category == 'unknown':
                results['unknown'] += 1
                continue
            
            # 移動文件
            success = self.move_file(file_path, category)
            
            if success:
                results[category] += 1
            else:
                results['failed'] += 1
        
        return results
    
    def verify_reorganization(self) -> Dict[str, List[str]]:
        """驗證重新組織結果"""
        logger.info("🔍 驗證重新組織結果")
        
        verification = {}
        
        for category, dir_path in self.target_dirs.items():
            files = list(dir_path.glob('*.npz')) + list(dir_path.glob('*.pkl'))
            verification[category] = [f.name for f in files]
            logger.info(f"{category}: {len(files)} 個文件")
        
        return verification
    
    def generate_summary_report(self, results: Dict[str, int], verification: Dict[str, List[str]]) -> str:
        """生成總結報告"""
        report = f"""
# 📁 Processed 文件重新組織報告

## 📊 移動統計

### 成功移動的文件:
- **separate**: {results.get('separate', 0)} 個文件
- **separate_norm**: {results.get('separate_norm', 0)} 個文件  
- **combine**: {results.get('combine', 0)} 個文件
- **combine_norm**: {results.get('combine_norm', 0)} 個文件
- **station_specific**: {results.get('station_specific', 0)} 個文件

### 異常情況:
- **無法分類**: {results.get('unknown', 0)} 個文件
- **移動失敗**: {results.get('failed', 0)} 個文件

## 📂 目錄結構驗證

"""
        
        for category, files in verification.items():
            report += f"### {category}/ ({len(files)} 個文件)\n"
            if files:
                for file in sorted(files)[:5]:  # 只顯示前5個
                    report += f"- {file}\n"
                if len(files) > 5:
                    report += f"- ... 還有 {len(files) - 5} 個文件\n"
            else:
                report += "- (空目錄)\n"
            report += "\n"
        
        report += f"""
## 🔄 備份信息

所有移動的文件都已備份到: `data/backup_processed/`

## ✅ 重新組織完成

現在 processed 文件已經按照正確的目錄結構組織：

```
data/processed/
├── separate/           # 單測站原始數據
├── separate_norm/      # 單測站標準化數據  
├── combine/           # 組合原始數據
├── combine_norm/      # 組合標準化數據
└── station_specific/  # 測站特定數據
```

---
*報告生成時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        return report

def main():
    """主執行函數"""
    logger.info("=" * 60)
    logger.info("🗂️  開始重新組織 processed 文件")
    logger.info("=" * 60)
    
    reorganizer = FileReorganizer()
    
    try:
        # 重新組織文件
        results = reorganizer.reorganize_all()
        
        # 驗證結果
        verification = reorganizer.verify_reorganization()
        
        # 生成報告
        report = reorganizer.generate_summary_report(results, verification)
        
        # 保存報告
        report_path = f"file_reorganization_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info("=" * 60)
        logger.info("🎉 文件重新組織完成!")
        logger.info(f"📊 總計移動: {sum(v for k, v in results.items() if k not in ['unknown', 'failed'])} 個文件")
        logger.info(f"📁 報告保存: {report_path}")
        logger.info("=" * 60)
        
        # 打印簡要結果
        print("\n✨ 重新組織結果:")
        for category, count in results.items():
            if count > 0:
                print(f"  {category}: {count} 個文件")
        
    except Exception as e:
        logger.error(f"💥 重新組織過程中發生錯誤: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 