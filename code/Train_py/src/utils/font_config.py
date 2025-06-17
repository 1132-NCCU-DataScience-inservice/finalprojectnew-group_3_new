# -*- coding: utf-8 -*-
"""
統一的中文字體配置模塊
解決matplotlib中文字體顯示問題
支持Windows、macOS、Linux多平台
"""

import matplotlib.pyplot as plt
import matplotlib
import platform
import os
from pathlib import Path

def get_system_chinese_fonts():
    """獲取系統可用的中文字體列表"""
    system = platform.system()
    
    if system == "Windows":
        fonts = [
            'Microsoft YaHei',  # 微軟雅黑 - 最常用
            'SimHei',           # 黑體
            'FangSong',         # 仿宋
            'KaiTi',            # 楷體 
            'Microsoft JhengHei', # 微軟正黑體
            'Arial Unicode MS'   # 備用
        ]
    elif system == "Darwin":  # macOS
        fonts = [
            'PingFang SC',      # 蘋方字體
            'Arial Unicode MS', # Arial Unicode
            'Heiti SC',         # 黑體-簡
            'STHeiti',          # 華文黑體
            'Hiragino Sans GB'  # 冬青黑體簡體中文
        ]
    else:  # Linux
        fonts = [
            'Noto Sans CJK SC',      # 思源黑體
            'WenQuanYi Micro Hei',   # 文泉驛微米黑
            'WenQuanYi Zen Hei',     # 文泉驛正黑
            'Droid Sans Fallback',    # Droid字體
            'DejaVu Sans'            # 備用英文字體
        ]
    
    return fonts

def setup_matplotlib_chinese():
    """設置matplotlib中文字體配置"""
    try:
        # 獲取系統字體
        chinese_fonts = get_system_chinese_fonts()
        
        # 設置字體優先級列表
        plt.rcParams['font.sans-serif'] = chinese_fonts
        
        # 解決負號顯示問題
        plt.rcParams['axes.unicode_minus'] = False
        
        # 設置默認編碼
        plt.rcParams['font.family'] = 'sans-serif'
        
        # 設置字體大小
        plt.rcParams['font.size'] = 10
        plt.rcParams['axes.titlesize'] = 12
        plt.rcParams['axes.labelsize'] = 10
        plt.rcParams['xtick.labelsize'] = 9
        plt.rcParams['ytick.labelsize'] = 9
        plt.rcParams['legend.fontsize'] = 9
        plt.rcParams['figure.titlesize'] = 14
        
        # 設置圖表樣式
        plt.rcParams['axes.grid'] = True
        plt.rcParams['grid.alpha'] = 0.3
        plt.rcParams['axes.spines.top'] = False
        plt.rcParams['axes.spines.right'] = False
        
        print(f"✅ 中文字體配置完成 - {platform.system()}")
        print(f"📝 字體優先級: {chinese_fonts[:3]}")
        return True
        
    except Exception as e:
        print(f"⚠️  字體配置警告: {e}")
        # 基本備用設置
        plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
        return False

def check_font_support():
    """檢查當前系統的中文字體支持情況"""
    import matplotlib.font_manager as fm
    
    print("🔍 檢查系統中文字體支持:")
    
    # 獲取所有字體
    font_list = [f.name for f in fm.fontManager.ttflist]
    chinese_fonts = get_system_chinese_fonts()
    
    available_chinese = []
    for font in chinese_fonts:
        if font in font_list:
            available_chinese.append(font)
            print(f"  ✅ {font}")
        else:
            print(f"  ❌ {font}")
    
    if available_chinese:
        print(f"📊 可用中文字體數量: {len(available_chinese)}")
        return available_chinese[0]  # 返回第一個可用字體
    else:
        print("⚠️  未找到中文字體，將使用英文字體")
        return 'DejaVu Sans'

def test_chinese_display():
    """測試中文字體顯示效果"""
    try:
        import matplotlib.pyplot as plt
        
        # 創建測試圖表
        fig, ax = plt.subplots(figsize=(8, 6))
        
        # 測試中文文字
        test_texts = [
            "主要污染物24小時趨勢",
            "AQI空氣品質指數",
            "PM2.5細顆粒物濃度",
            "空氣品質等級分佈"
        ]
        
        for i, text in enumerate(test_texts):
            ax.text(0.1, 0.8 - i*0.15, text, fontsize=12, 
                   transform=ax.transAxes)
        
        ax.set_title("中文字體顯示測試", fontsize=14, fontweight='bold')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        
        # 保存測試圖片
        test_dir = Path("reports/font_test")
        test_dir.mkdir(parents=True, exist_ok=True)
        test_path = test_dir / "chinese_font_test.png"
        
        plt.savefig(test_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"✅ 中文字體測試完成: {test_path}")
        return True
        
    except Exception as e:
        print(f"❌ 中文字體測試失敗: {e}")
        return False

def apply_chinese_style():
    """應用中文圖表樣式配置"""
    # 設置matplotlib樣式
    plt.style.use('default')
    
    # 應用中文字體
    setup_matplotlib_chinese()
    
    # 設置圖表美化參數
    plt.rcParams.update({
        'figure.facecolor': 'white',
        'axes.facecolor': 'white',
        'savefig.facecolor': 'white',
        'figure.edgecolor': 'none',
        'axes.edgecolor': 'gray',
        'axes.linewidth': 0.8,
        'xtick.direction': 'out',
        'ytick.direction': 'out',
        'xtick.major.size': 4,
        'ytick.major.size': 4,
        'legend.framealpha': 0.8,
        'legend.fancybox': True,
        'legend.shadow': True
    })

# 自動配置
if __name__ == "__main__":
    print("🚀 字體配置模塊測試")
    print("="*40)
    
    # 檢查字體支持
    available_font = check_font_support()
    
    # 設置字體
    setup_matplotlib_chinese()
    
    # 測試顯示
    test_chinese_display()
    
    print("📋 字體配置測試完成")
else:
    # 被導入時自動設置
    setup_matplotlib_chinese() 