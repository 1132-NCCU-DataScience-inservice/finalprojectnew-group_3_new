[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/ZXf3Hbkv)
# [Group3] 1132-DS-final_air-quality <!-- omit in toc -->

整合 **AQX\_P\_488** 空氣品質資料與中央氣象署 (CWA) 氣象觀測，
建立一條 **可重複、可擴充、易維護** 的資料科學流水線，涵蓋：

* **資料獲取 → 清理 / 特徵工程 → 時間序列與機器學習預測 →**  **分群 / 異常偵測 → 評估解釋 → Shiny 互動展示**

> **專案規劃文件**：[https://docs.google.com/document/d/1fWCmSwpUNJA2OCpSXNO9Z6GWopuk0UtO65z6cOMXtyc/edit](https://docs.google.com/document/d/1fWCmSwpUNJA2OCpSXNO9Z6GWopuk0UtO65z6cOMXtyc/edit)

> **最終簡報**：`docs/Air Pollution Analysis – Final Project.pptx`

---

* [Quick Start](#quick-start)
* [Project Motivation](#project-motivation)
* [Overall Workflow](#overall-workflow)
* [Contributors](#contributors)
* [Project Structure Details](#project-structure-details)
* [Folder Organization](#folder-organization)
* [End-to-End Pipeline Details](#end-to-end-pipeline-details)
* [Evaluation & Explainability](#evaluation--explainability)
* [Shiny Dashboard](#shiny-dashboard)
* [Installation & Environment](#installation--environment)
* [Citation](#citation)
* [License](#license)

---

## Quick Start

以下最小指令可自動完成 **原始資料 → 模型訓練 → 評估解釋** 全流程。

```bash
# 1. (可選) 由逐時觀測產生滑動視窗特徵
Rscript generate_sliding_windows/generate_sliding_windows_production.R \
       --input  data/Raw \
       --output data/Combine

# 2. 訓練 LightGBM 與/或 LSTM
Rscript run_aqi_training.R                  # 完整訓練管線
#  └── 常用旗標：
#      --models lgbm,lstm      # 指定演算法
#      --max-files 10          # 每種資料型態最多取 N 個檔案

# 3. 事後評估與可解釋性分析
Rscript run_analysis.R                      # 標準 Top-N 報告
Rscript run_analysis.R --full               # 跨測站完整比較
```

所有輸出（模型、指標、圖表、報告）將自動寫入：

```
model_outputs/      # 模型與中介檔
analysis_outputs/   # 評估報表、SHAP 圖
```

---

## Project Motivation

1. **環境影響複雜** – AQI 單一指標易忽略氣象對光化學反應、濕沉降的影響。
2. **決策需求多元** – 預警（短期 1-24 h）、趨勢（季節～多年）、異常偵測。
3. **溝通互動性** – 非技術利害關係人需要即時、直觀的視覺化儀表板。

因此，本專案在期末報告架構上 **加入氣象變數、建構全流程自動化、並提供 Shiny Dashboard**。

---

## Overall Workflow

```text
     ┌─────────────┐
     │   Acquire   │  CWA / AQX API
     └─────┬───────┘
           ▼
┌────────────────────┐
│   Raw CSV / Parquet│
└─────┬──────────────┘
      ▼
┌─────────────┐  清理、補值
│    Clean    │─────────────────────┐
└─────┬───────┘                     │
      ▼                             │
┌─────────────┐  製作滯後 / 滑動視窗  │
│   Feature   │► features.parquet   │
└─────┬───────┘                     │
      ▼                             │
┌─────────────┐  時序交叉驗證        │
│   Modeling  │► models/*.rds       │
└─────┬───────┘                     │
      ▼                             │
┌─────────────┐  SHAP / PermImp     │
│  Evaluation │► reports/*.html     │
└─────┬───────┘                     │
      ▼                             │
┌─────────────┐  R shiny + leaflet  │
│   Shiny UI  │► 互動視覺化          │
└─────────────┘
```

---

## Contributors
|組員|系級|學號|工作分配|
|-|-|-|-|
|李翔仁|資科碩一|113971021|資料獲取 → 清理 / 特徵工程/ Shiny 展示| 
|張敦皓|資科碩一|113971007|時間序列 & XGBoost 預測 → 分群 / 異常偵測|
|林遠哲|資科碩一|113971001|資料獲取 → 清理 / 特徵工程|
|王秀暐|資科碩三|111971025|Shiny 展示|

---

## Project Structure Details

### docs
專案文件與簡報資料：
* `Air Pollution Analysis – Final Project.pptx` - 最終專案簡報（預交 2025-06-10）
* `Air Pollution Analysis.pptx` - 專案簡報草案
* `空氣品質監測與預測 – 期末專案規劃.pdf` - 專案規劃文件
* `資料科學專題-模型訓練規劃` - 模型訓練規劃文件
* `error_log/` - 錯誤記錄與除錯資訊

### code
核心程式碼與分析腳本：

#### 主要處理腳本
* `combine_to_onecsv.R` - 合併資料為單一 CSV 檔案
* `Finished_to_ClearFeature.R` - 特徵清理與處理
* `Finished_to_FinalDataset.R` - 最終資料集生成

#### Train_R/ (R 語言訓練與分析)
* `run_aqi_training.R` - 主要 AQI 預測模型訓練腳本
* `run_analysis.R` - 模型評估與分析腳本
* `demo_fast_evaluation.R` - 快速評估演示
* `demo_full_evaluation_enhanced.R` - 完整評估演示（增強版）
* `demo_lstm_evaluation.R` - LSTM 模型評估演示
* `generate_sliding_windows/` - 滑動視窗特徵生成
* `model_src/` - 模型相關輔助函式
* `analysis_outputs/` - 分析結果輸出
* `model_outputs/` - 模型訓練輸出
* `LAG_Analysis/` - 滯後分析相關檔案
* `SHAP_加速指南.md` - SHAP 分析加速使用指南

#### Train_py/ (Python 訓練與分析)
* `run_training.py` - Python 主要訓練腳本
* `run_unified_training.py` - 統一訓練流程腳本
* `create_report_analyzer.py` - 報告分析器
* `setup.py` - Python 環境設定
* `requirements.txt` - Python 套件需求
* `configs/` - 設定檔案
* `src/` - Python 原始碼模組
* `models/` - Python 生成的模型
* `reports/` - Python 分析報告
* `docs/` - Python 相關文件
* `報告分析使用指南.md` - 報告分析使用說明

### Shiny Dashboard
雖然專案中沒有本地 shiny-app 資料夾，但已部署互動式視覺化應用：

**部署連結**：[https://w2wpgv-0-0.shinyapps.io/Visualization/](https://w2wpgv-0-0.shinyapps.io/Visualization/)

**功能特色**：
* **即時地圖顯示** - 基於 Leaflet 的互動式地圖
* **空氣品質指標** - AQI, PM₂.₅, O₃ 等監測數據
* **預測結果展示** - LightGBM 與 LSTM 模型預測結果

**技術架構**：
* 前端：R Shiny + Leaflet + plotly
* 後端：整合 CWA 氣象 API 與 AQX_P_488 空品資料
* 部署：shinyapps.io

---

---

## Folder Organization

```text
<project_root>/
├── README.md
├── .git/                         # Git version control files
├── code/                         # Source code for data processing, training, and analysis
│   ├── combine_to_onecsv.R
│   ├── Finished_to_ClearFeature.R
│   ├── Finished_to_FinalDataset.R
│   ├── Train_py/                 # Python scripts and associated files
│   │   ├── run_training.py       # Main Python training script
│   │   ├── configs/              # Configuration files
│   │   ├── src/                  # Python source modules
│   │   ├── models/               # Models generated by Python scripts
│   │   └── reports/              # Reports from Python analysis
│   └── Train_R/                  # R scripts and associated files
│       ├── run_aqi_training.R    # Main R training script
│       ├── run_analysis.R        # R analysis script
│       ├── generate_sliding_windows/ # R scripts for feature generation
│       ├── model_src/            # R source/helper scripts for models
│       └── analysis_outputs/     # Outputs from R analysis
├── data/                         # Raw and intermediate data files
│   ├── Data_Sendlink.txt
│   └── Tracker Issue.txt
├── docs/                         # Project documentation, presentations, and planning
│   ├── Air Pollution Analysis – Final Project.pptx
│   └── 空氣品質監測與預測 – 期末專案規劃.pdf
└── results/                      # Final outputs, model registry, and deployed models
    ├── model_registry.csv
    └── models/                   # Trained models, organized by type/station
        └── lgbm_separate_norm_Nomorlization_三義_C0F9Q0_combined_windows/
        └── ... (other model folders)
```

---

## End-to-End Pipeline Details

| 階段      | Script / Notebook                                 | 內容摘要                              | 主要輸出                                   |
| ------- | ------------------------------------------------- | --------------------------------- | -------------------------------------- |
| Acquire | `src/R/acquire.R`, `acquire.py`                   | 呼叫 CWA & AQX API、補缺值              | `data/raw/*.csv`                       |
| Clean   | `src/R/clean.R`                                   | 型別統一、異常剔除、地理對齊                    | `data/processed/*.parquet`             |
| Feature | `src/R/features.R` + `generate_sliding_windows/*` | Lag、rolling、diff、STL              | `data/features/*.parquet`              |
| Model   | `src/R/modeling.R`, `run_aqi_training.R`          | 時序 CV、LightGBM／LSTM               | `models/*.rds`, `model_outputs/*`      |
| Report  | `quarto render` 或 `run_analysis.R`                | SHAP、Permutation Importance、跨站排行榜 | `reports/*.html`, `analysis_outputs/*` |
| Shiny   | `shiny-app/`                                      | Leaflet 地圖、指標查詢、異常追蹤              | Web App                                |

---

## Evaluation & Explainability

* **SHAP** (`shapviz`) – 全域 / 區域重要度，支援分群比較
* **Permutation Importance** – 校驗穩健度
* **Top-N 排行** – 同站多模型 & 同模型跨站
* **Error Analysis** – 階段性 (季節 / 風向) 熱力矩陣
* **Null Model Benchmark** – 相對改善百分比 Δ% 顯示於報告封面

---

## Shiny Dashboard

* **即時地圖**（Leaflet） – AQI, PM₂.₅, O₃ 等指標顯示
* **模型解釋** – 點擊測站 → 顯示 SHAP waterfall

部署方式：

1. **本機**：`R -e "shiny::runApp('shiny-app')"`
2. **雲端**：CI 自動推送至 [https://shinyapps.io](https://shinyapps.io) 或內部伺服器 (`rsconnect::deployApp`)

---

## Installation & Environment

### Prerequisites

| 軟體                 | 推薦版本   | 用途                  |
| ------------------ | ------ | ------------------- |
| **R / RStudio**    | ≥ 4.3  | 資料清理、特徵、Shiny       |
| **Python / Conda** | ≥ 3.10 | API 抓取、XGBoost、輔助腳本 |
| **Git LFS**        | 最新     | 版控大檔                |
| **DVC** *(可選)*     | ≥ 3.0  | 資料 / 模型流追蹤          |
| **Quarto**         | ≥ 1.4  | 報告 / Notebook       |

### Setup Steps

```bash
# 1. 取得程式碼
git clone https://github.com/<your-id>/air-quality-tw.git
cd air-quality-tw

# 2. 還原 R & Python 環境
R -e "install.packages('renv'); renv::restore()"
conda env create -f environment.yml
conda activate airq

# 3. 下載資料 / 模型
dvc pull          # 或 git lfs pull

# 4. 一鍵重跑全流程
make all          # (Makefile / targets / snakemake 任選)

# 5. 啟動 Shiny Dashboard
R -e "shiny::runApp('shiny-app', launch.browser = TRUE)"
```

> **API 金鑰**：請至 `.env` 或 `config.yml` 填入 **CWA opendata 授權碼**；範例模板見 `config/_example.env`.

---

## 4. 資料來源與授權

| 資料集                | 提供單位     | 授權            | 備註                     |
| ------------------ | -------- | ------------- | ---------------------- |
| AQX\_P\_488 空氣品質指標 | 行政院環境部   | 政府資料開放授權第 1 版 | 逐時 AQI / PM / O₃ / 風速向 |
| O-A0001-001 自動氣象站  | 交通部中央氣象署 | 同上            | 溫度 / 濕度 / 氣壓 / 風       |
| O-A0002-001 自動雨量站  | 交通部中央氣象署 | 同上            | 降水量                    |
| O-A0091-001 日射量    | 交通部中央氣象署 | 同上            | 太陽輻射 (MJ m⁻²)          |
| CODiS 日報表          | 交通部中央氣象署 | 需註冊           | 歷史 1995–               |

*使用及引用時請遵守各單位開放資料授權規範，並標註出處。*

---

## Citation

```
Chan, J. (2025). Air-Quality-TW: Integrating CWA Meteorology with AQX_P_488 for Forecasting, Clustering and Anomaly Detection (Version v1.0) [Computer software]. https://github.com/<your-id>/air-quality-tw
```

---
MIT License © 2025




