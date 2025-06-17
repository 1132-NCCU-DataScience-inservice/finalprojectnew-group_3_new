#!/usr/bin/env python3
"""
AQI預測系統 - 報告分析器
能夠分析和比較所有訓練報告，提供深度洞察
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple, Any
import argparse
import warnings
warnings.filterwarnings('ignore')

# 中文字體設定
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

class ReportAnalyzer:
    """報告分析器"""
    
    def __init__(self, reports_dir: str = "outputs/reports"):
        self.reports_dir = Path(reports_dir)
        self.data = []
        self.comparison_data = []
        
    def load_all_reports(self):
        """載入所有JSON報告"""
        print("🔍 載入報告數據...")
        
        json_files = list(self.reports_dir.glob("*.json"))
        print(f"發現 {len(json_files)} 個JSON報告文件")
        
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                if 'results' in data:
                    for result in data['results']:
                        if result.get('success', False):
                            self.data.append(result)
                            
            except Exception as e:
                print(f"⚠️ 載入 {json_file.name} 失敗: {e}")
                
        print(f"✅ 成功載入 {len(self.data)} 個訓練結果")
        
    def create_comparison_dataframe(self) -> pd.DataFrame:
        """創建比較用的DataFrame"""
        comparison_data = []
        
        for item in self.data:
            base_info = {
                'pipeline_mode': item['pipeline_mode'],
                'station': item['station'],
                'timestamp': item['timestamp'],
                'success': item['success']
            }
            
            for model_name, model_data in item['models'].items():
                if model_data:  # 確保模型數據存在
                    row = base_info.copy()
                    row['model'] = model_name
                    row['training_time'] = model_data.get('training_time', 0)
                    
                    # 驗證集指標
                    val_metrics = model_data.get('val_metrics', {})
                    row['val_mae'] = val_metrics.get('mae', np.nan)
                    row['val_rmse'] = val_metrics.get('rmse', np.nan)
                    row['val_mape'] = val_metrics.get('mape', np.nan)
                    row['val_r2'] = val_metrics.get('r2', np.nan)
                    
                    # 訓練集指標
                    train_metrics = model_data.get('train_metrics', {})
                    row['train_mae'] = train_metrics.get('mae', np.nan)
                    row['train_rmse'] = train_metrics.get('rmse', np.nan)
                    row['train_mape'] = train_metrics.get('mape', np.nan)
                    row['train_r2'] = train_metrics.get('r2', np.nan)
                    
                    comparison_data.append(row)
        
        return pd.DataFrame(comparison_data)
    
    def analyze_model_performance(self, df: pd.DataFrame):
        """分析模型性能"""
        print("\n" + "="*60)
        print("📊 模型性能分析")
        print("="*60)
        
        # 1. 整體模型比較
        print("\n1️⃣ 整體模型性能比較")
        print("-" * 30)
        
        model_stats = df.groupby('model').agg({
            'val_mae': ['mean', 'std', 'min', 'max', 'count'],
            'val_r2': ['mean', 'std', 'min', 'max'],
            'training_time': ['mean', 'std', 'min', 'max']
        }).round(4)
        
        print(model_stats)
        
        # 2. 模式別性能比較
        print("\n2️⃣ 不同訓練模式性能比較")
        print("-" * 30)
        
        mode_stats = df.groupby(['pipeline_mode', 'model']).agg({
            'val_mae': 'mean',
            'val_r2': 'mean',
            'training_time': 'mean'
        }).round(4)
        
        print(mode_stats)
        
        # 3. 找出最佳模型組合
        print("\n3️⃣ 最佳模型組合")
        print("-" * 30)
        
        # 依據MAE找出最佳模型
        best_by_mae = df.loc[df['val_mae'].idxmin()]
        print(f"最低MAE: {best_by_mae['station']} - {best_by_mae['model']} - {best_by_mae['pipeline_mode']}")
        print(f"MAE: {best_by_mae['val_mae']:.4f}, R²: {best_by_mae['val_r2']:.4f}")
        
        # 依據R²找出最佳模型
        best_by_r2 = df.loc[df['val_r2'].idxmax()]
        print(f"最高R²: {best_by_r2['station']} - {best_by_r2['model']} - {best_by_r2['pipeline_mode']}")
        print(f"MAE: {best_by_r2['val_mae']:.4f}, R²: {best_by_r2['val_r2']:.4f}")
    
    def analyze_station_performance(self, df: pd.DataFrame):
        """分析測站性能"""
        print("\n" + "="*60)
        print("🏢 測站性能分析")
        print("="*60)
        
        # 1. 測站性能排名
        station_stats = df.groupby('station').agg({
            'val_mae': 'mean',
            'val_r2': 'mean',
            'training_time': 'mean'
        }).round(4)
        
        # 依MAE排序
        station_ranking = station_stats.sort_values('val_mae')
        print("\n📈 測站性能排名 (依MAE)")
        print("-" * 30)
        print(station_ranking.head(10))
        
        # 2. 表現最佳和最差的測站
        print(f"\n🏆 表現最佳測站: {station_ranking.index[0]} (MAE: {station_ranking.iloc[0]['val_mae']:.4f})")
        print(f"💔 表現最差測站: {station_ranking.index[-1]} (MAE: {station_ranking.iloc[-1]['val_mae']:.4f})")
    
    def analyze_pipeline_modes(self, df: pd.DataFrame):
        """分析不同Pipeline模式的效果"""
        print("\n" + "="*60)
        print("⚙️ Pipeline模式分析")
        print("="*60)
        
        mode_comparison = df.groupby(['pipeline_mode', 'model']).agg({
            'val_mae': ['mean', 'count'],
            'val_r2': 'mean',
            'training_time': 'mean'
        }).round(4)
        
        print(mode_comparison)
        
        # 模式效果分析
        print("\n📊 模式效果對比")
        print("-" * 30)
        
        for mode in df['pipeline_mode'].unique():
            mode_data = df[df['pipeline_mode'] == mode]
            avg_mae = mode_data['val_mae'].mean()
            avg_r2 = mode_data['val_r2'].mean()
            avg_time = mode_data['training_time'].mean()
            count = len(mode_data)
            
            print(f"{mode:15} | MAE: {avg_mae:.4f} | R²: {avg_r2:.4f} | 時間: {avg_time:.2f}s | 樣本: {count}")
    
    def create_visualization(self, df: pd.DataFrame):
        """創建視覺化圖表"""
        print("\n🎨 生成視覺化報告...")
        
        # 設定圖形大小
        fig, axes = plt.subplots(2, 3, figsize=(20, 12))
        fig.suptitle('AQI預測系統 - 模型性能分析報告', fontsize=16, fontweight='bold')
        
        # 1. 模型MAE比較
        ax1 = axes[0, 0]
        model_mae = df.groupby('model')['val_mae'].mean().sort_values()
        model_mae.plot(kind='bar', ax=ax1, color=['#FF6B6B', '#4ECDC4'])
        ax1.set_title('模型MAE比較', fontweight='bold')
        ax1.set_ylabel('MAE')
        ax1.tick_params(axis='x', rotation=45)
        
        # 2. 模型R²比較
        ax2 = axes[0, 1]
        model_r2 = df.groupby('model')['val_r2'].mean().sort_values(ascending=False)
        model_r2.plot(kind='bar', ax=ax2, color=['#45B7D1', '#96CEB4'])
        ax2.set_title('模型R²比較', fontweight='bold')
        ax2.set_ylabel('R²')
        ax2.tick_params(axis='x', rotation=45)
        
        # 3. 訓練時間比較
        ax3 = axes[0, 2]
        model_time = df.groupby('model')['training_time'].mean().sort_values()
        model_time.plot(kind='bar', ax=ax3, color=['#FECA57', '#FF9FF3'])
        ax3.set_title('模型訓練時間比較', fontweight='bold')
        ax3.set_ylabel('時間 (秒)')
        ax3.tick_params(axis='x', rotation=45)
        
        # 4. Pipeline模式效果
        ax4 = axes[1, 0]
        mode_mae = df.groupby('pipeline_mode')['val_mae'].mean().sort_values()
        mode_mae.plot(kind='bar', ax=ax4, color=['#6C5CE7', '#A29BFE'])
        ax4.set_title('Pipeline模式MAE比較', fontweight='bold')
        ax4.set_ylabel('MAE')
        ax4.tick_params(axis='x', rotation=45)
        
        # 5. MAE vs R² 散點圖
        ax5 = axes[1, 1]
        colors = {'lightgbm': '#FF6B6B', 'lstm': '#4ECDC4'}
        for model in df['model'].unique():
            model_data = df[df['model'] == model]
            ax5.scatter(model_data['val_mae'], model_data['val_r2'], 
                       alpha=0.6, label=model, color=colors.get(model, '#999999'))
        ax5.set_xlabel('MAE')
        ax5.set_ylabel('R²')
        ax5.set_title('MAE vs R² 分布', fontweight='bold')
        ax5.legend()
        
        # 6. 測站性能熱力圖 (Top 15)
        ax6 = axes[1, 2]
        station_pivot = df.pivot_table(values='val_mae', index='station', columns='model', aggfunc='mean')
        station_pivot_top = station_pivot.head(15)  # 只顯示前15個測站
        
        if not station_pivot_top.empty:
            sns.heatmap(station_pivot_top, annot=True, fmt='.3f', cmap='RdYlBu_r', ax=ax6)
            ax6.set_title('測站MAE熱力圖 (Top 15)', fontweight='bold')
        
        plt.tight_layout()
        
        # 保存圖表
        output_path = self.reports_dir / "model_analysis_report.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"✅ 視覺化報告已保存: {output_path}")
        
        plt.show()
    
    def generate_summary_report(self, df: pd.DataFrame):
        """生成總結報告"""
        print("\n" + "="*60)
        print("📋 總結報告")
        print("="*60)
        
        total_experiments = len(df)
        unique_stations = df['station'].nunique()
        unique_modes = df['pipeline_mode'].nunique()
        
        print(f"🔢 總實驗數量: {total_experiments}")
        print(f"🏢 涵蓋測站數: {unique_stations}")
        print(f"⚙️ 測試模式數: {unique_modes}")
        
        # 模型勝率分析
        print("\n🏆 模型勝率分析")
        print("-" * 30)
        
        station_best = df.loc[df.groupby('station')['val_mae'].idxmin()]
        model_wins = station_best['model'].value_counts()
        print(model_wins)
        
        # 推薦配置
        print("\n💡 推薦配置")
        print("-" * 30)
        
        # 找出表現最穩定的配置
        config_stats = df.groupby(['pipeline_mode', 'model']).agg({
            'val_mae': ['mean', 'std'],
            'val_r2': 'mean',
            'training_time': 'mean'
        })
        
        # 計算綜合分數 (低MAE + 高R² + 低變異)
        config_stats['score'] = (
            1 / config_stats[('val_mae', 'mean')] * 100 +  # MAE越低越好
            config_stats[('val_r2', 'mean')] * 100 +       # R²越高越好
            1 / (config_stats[('val_mae', 'std')] + 0.001)  # 變異越低越好
        )
        
        best_config = config_stats.sort_values('score', ascending=False).index[0]
        print(f"最佳配置: {best_config[0]} + {best_config[1]}")
        
        # 生成JSON報告
        summary = {
            'analysis_timestamp': pd.Timestamp.now().isoformat(),
            'total_experiments': int(total_experiments),
            'unique_stations': int(unique_stations),
            'unique_modes': int(unique_modes),
            'model_performance': {
                model: {
                    'avg_mae': float(df[df['model'] == model]['val_mae'].mean()),
                    'avg_r2': float(df[df['model'] == model]['val_r2'].mean()),
                    'avg_training_time': float(df[df['model'] == model]['training_time'].mean()),
                    'sample_count': int(len(df[df['model'] == model]))
                }
                for model in df['model'].unique()
            },
            'best_configuration': {
                'pipeline_mode': best_config[0],
                'model': best_config[1],
                'score': float(config_stats.loc[best_config, 'score'])
            },
            'model_wins': model_wins.to_dict()
        }
        
        # 保存報告
        report_path = self.reports_dir / "summary_analysis_report.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 總結報告已保存: {report_path}")
    
    def run_analysis(self):
        """執行完整分析"""
        print("🚀 開始報告分析...")
        
        # 載入數據
        self.load_all_reports()
        
        if not self.data:
            print("❌ 沒有找到可分析的報告數據")
            return
        
        # 創建DataFrame
        df = self.create_comparison_dataframe()
        print(f"📊 分析數據形狀: {df.shape}")
        
        # 執行各種分析
        self.analyze_model_performance(df)
        self.analyze_station_performance(df)
        self.analyze_pipeline_modes(df)
        
        # 生成視覺化
        self.create_visualization(df)
        
        # 生成總結報告
        self.generate_summary_report(df)
        
        print("\n🎉 分析完成！")

def main():
    """主函數"""
    parser = argparse.ArgumentParser(description="AQI預測系統報告分析器")
    parser.add_argument(
        "--reports-dir", 
        default="outputs/reports",
        help="報告目錄路徑 (默認: outputs/reports)"
    )
    
    args = parser.parse_args()
    
    analyzer = ReportAnalyzer(args.reports_dir)
    analyzer.run_analysis()

if __name__ == "__main__":
    main() 