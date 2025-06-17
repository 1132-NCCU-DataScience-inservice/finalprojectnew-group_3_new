# AQI預測系統 - 深度學習與機器學習混合模型

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.6%2B-red)](https://pytorch.org/)
[![LightGBM](https://img.shields.io/badge/LightGBM-Latest-green)](https://lightgbm.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

一個基於深度學習（LSTM）和梯度提升機器學習（LightGBM）的空氣品質指數（AQI）預測系統，支援多種訓練管道和測站配置。

## 📈 專案成果

### 🎯 訓練完成狀態
- ✅ **Separate Pipeline**: 75個測站全部訓練完成（100%成功率）
- ✅ **雙模型訓練**: LightGBM + LSTM 同時訓練
- ✅ **配置統一**: 新舊配置系統完全兼容
- ✅ **路徑修復**: 時間戳一致性問題已解決

### 📊 模型表現（桃園測站範例）
| 模型 | 訓練時間 | 驗證集MAE | 模型大小 |
|------|----------|-----------|----------|
| LightGBM | 6.18秒 | 2.78 | 544KB |
| LSTM | 15.66秒 | 3.13 | 1.5MB |

## 🚀 快速開始

### 環境需求
```bash
# 創建環境
conda create -n aqi python=3.8
conda activate aqi

# 安裝依賴
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install lightgbm scikit-learn numpy pandas matplotlib seaborn
pip install pyyaml tqdm pathlib
```

### 基本使用

#### 1. 訓練單個測站
```bash
# 訓練指定測站（原始數據）
python run_training.py --mode separate --stations 桃園

# 訓練指定測站（標準化數據）
python run_training.py --mode separate_norm --stations 桃園

# 驗證配置
python run_training.py --mode separate --stations 桃園 --validate
```

#### 2. 批量訓練
```bash
# 訓練所有separate測站（75個）
python run_training.py --mode separate

# 訓練所有separate_norm測站（75個）
python run_training.py --mode separate_norm

# 訓練全域模式
python run_training.py --mode combine
python run_training.py --mode combine_norm
```

#### 3. 多管道訓練
```bash
# 同時訓練多個管道
python run_training.py --modes separate combine --stations 桃園

# 訓練所有管道模式
python run_training.py --modes all
```

## 🗂️ 專案結構

```
Train/
├── src/                          # 核心代碼
│   ├── unified_config.py         # 統一配置系統
│   ├── unified_preprocessor.py   # 統一數據預處理
│   ├── unified_window_generator.py # 時間窗口生成
│   ├── unified_trainer.py        # 統一模型訓練
│   └── config_manager.py         # 舊配置系統（兼容）
│
├── configs/                      # 配置文件
│   ├── pipelines/               # 管道配置
│   │   ├── combine.yaml         # 全域合併模式
│   │   ├── combine_norm.yaml    # 全域標準化模式
│   │   ├── separate.yaml        # 分別訓練模式
│   │   ├── separate_norm.yaml   # 分別標準化模式
│   │   └── station_specific.yaml # 指定測站模式
│   ├── base.yaml               # 基礎配置
│   ├── models.yaml             # 模型配置
│   └── stations.yaml           # 測站配置
│
├── data/                        # 數據目錄
│   ├── raw/                    # 原始數據
│   │   ├── Separate/           # 各測站原始數據（75個）
│   │   ├── Separate_Nomorlization/ # 各測站標準化數據（75個）
│   │   └── Combine/            # 合併數據
│   ├── processed/              # 預處理數據
│   └── sliding_windows/        # 時間窗口數據
│
├── models/                      # 訓練模型
│   ├── lightgbm/              # LightGBM模型
│   │   └── separate/          # 75個測站模型
│   └── lstm/                  # LSTM模型
│       └── separate/          # 75個測站模型
│
├── outputs/                     # 輸出結果
│   └── reports/               # 訓練報告
│
└── run_training.py              # 主執行腳本
```

## 🎛️ 訓練管道模式

| 模式 | 描述 | 數據源 | 測站數 | 狀態 |
|------|------|--------|--------|------|
| `combine` | 全域合併模式（原始） | Combine/ | 1個全域模型 | ✅ 可用 |
| `combine_norm` | 全域合併模式（標準化） | Combine_Nomolization/ | 1個全域模型 | ✅ 可用 |
| `separate` | 各測站分別模式（原始） | Separate/ | 75個測站模型 | ✅ 已完成 |
| `separate_norm` | 各測站分別模式（標準化） | Separate_Nomorlization/ | 75個測站模型 | ✅ 可用 |
| `station_specific` | 指定測站靈活模式 | 動態選擇 | 按需訓練 | ✅ 可用 |

## 📋 指令參考

### 訓練選項
```bash
# 管道模式選擇
--mode {combine,separate,combine_norm,separate_norm,station_specific,all}
--modes {多個模式} [{多個模式} ...]

# 測站選擇
--stations {測站名稱} [{測站名稱} ...]

# 其他選項
--validate          # 僅驗證配置
--output-dir DIR    # 指定輸出目錄
--verbose           # 詳細輸出
```

### 範例指令集
```bash
# 基礎訓練
python run_training.py --mode separate --stations 桃園
python run_training.py --mode separate_norm --stations 桃園 台北

# 批量訓練
python run_training.py --mode separate  # 75個測站
python run_training.py --modes separate separate_norm --stations 桃園

# 全域訓練
python run_training.py --mode combine
python run_training.py --mode combine_norm

# 配置驗證
python run_training.py --validate --mode separate_norm --stations 桃園
```

## 📈 訓練成果

### 已完成訓練
- ✅ **Separate模式**: 75個測站，100%成功率
- ✅ **雙模型**: 每個測站都有LightGBM和LSTM模型
- ✅ **完整管道**: 預處理 → 時間窗口 → 模型訓練

### 模型文件
```
models/
├── lightgbm/separate/
│   ├── separate_桃園_20250608_154641_lgbm.pkl
│   ├── separate_台北_*_lgbm.pkl
│   └── ... (75個測站模型)
└── lstm/separate/
    ├── separate_桃園_20250608_154641_lstm.pt
    ├── separate_台北_*_lstm.pt
    └── ... (75個測站模型)
```

### 訓練報告
完整的訓練結果保存在 `outputs/reports/` 目錄，包含：
- 模型性能指標（MAE, RMSE, MAPE, R²）
- 訓練時間和收斂情況
- 特徵重要性分析
- 配置摘要

## 🔧 技術特色

### 統一配置系統
- **5種訓練管道**: 支援全域和測站特定訓練
- **自動路徑管理**: 根據模式自動配置輸入輸出路徑
- **時間戳一致性**: 解決管道步驟間文件查找問題

### 雙模型架構
- **LightGBM**: 快速梯度提升，適合特徵工程
- **LSTM**: 深度序列學習，捕捉時間依賴
- **統一評估**: 標準化的評估指標和比較

### 企業級功能
- **PyTorch 2.6兼容**: 解決安全更新導致的載入問題
- **GPU加速**: 自動檢測和使用CUDA
- **批量處理**: 支援多測站並行訓練
- **錯誤恢復**: 健壯的異常處理機制

## 🛠️ 故障排除

### 常見問題

1. **配置驗證失敗**
   ```bash
   # 檢查管道配置
   python run_training.py --validate --mode separate
   ```

2. **找不到測站數據**
   ```bash
   # 檢查數據文件
   ls data/raw/Separate/ | grep 桃園
   ```

3. **GPU記憶體不足**
   ```bash
   # 使用CPU訓練
   export CUDA_VISIBLE_DEVICES=""
   python run_training.py --mode separate --stations 桃園
   ```

4. **模型載入錯誤**
   - 確保PyTorch版本 >= 2.6
   - 檢查文件權限和路徑

## 📊 效能基準

### 硬體需求
- **最低配置**: CPU 4核心, 8GB RAM
- **推薦配置**: CPU 8核心, 16GB RAM, GPU 8GB
- **大規模訓練**: CPU 16核心, 32GB RAM, GPU 16GB

### 訓練時間估算
| 模式 | 測站數 | 預估時間 | 硬體需求 |
|------|--------|----------|----------|
| separate | 75個 | 60-90分鐘 | GPU推薦 |
| combine | 1個 | 15-30分鐘 | GPU/CPU |
| separate_norm | 75個 | 60-90分鐘 | GPU推薦 |

## 🤝 貢獻指南

1. Fork 本專案
2. 創建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交變更 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 開啟 Pull Request

## 📝 更新日誌

### v1.2.0 (2025-06-08)
- ✅ 修復配置系統兼容性問題
- ✅ 完成75個測站separate pipeline訓練
- ✅ 添加5種訓練管道配置文件
- ✅ 解決時間戳一致性問題
- ✅ 支援PyTorch 2.6安全更新

### v1.1.0 (2025-06-07)
- ✅ 統一配置系統實現
- ✅ 雙模型訓練管道
- ✅ 路徑管理優化

## 📄 授權

本專案採用 MIT 授權條款 - 詳見 [LICENSE](LICENSE) 文件

## 🙋‍♂️ 支援

如有問題或建議，請：
1. 查看本README的故障排除章節
2. 檢查已有的 [Issues](../../issues)
3. 創建新的 Issue 描述問題

---

*最後更新: 2025-06-08*
*專案狀態: 穩定運行，75個測站訓練完成* 