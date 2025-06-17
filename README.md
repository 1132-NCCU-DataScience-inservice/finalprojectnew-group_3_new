[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/ZXf3Hbkv)
# [Group3] 1132-DS-final_air-quality
The goals of this project.
空氣品質受到氣象條件強烈影響；單用 AQI 資料易低估光化學作用、降雨清洗等效果。
本專案在期末報告框架基礎上，新增氣象輔助變數，同時確保：

長期趨勢：STL / Prophet
短期預報：XGBoost → PM₂.₅、AQI 下一 1‒24 小時
污染源分類：K-Means / 階層式分群
異常事件偵測：IsolationForest / LOF
互動溝通：Shiny Dashboard + Leaflet 地圖

## Contributors
|組員|系級|學號|工作分配|
|-|-|-|-|
|李翔仁|資科碩一|113971021|團隊中的吉祥物🦒，負責增進團隊氣氛| 
|張敦皓|資科碩一|113971007|團隊的中流砥柱，一個人打十個|
|林遠哲|資科碩一|113971001|團隊的中流砥柱，一個人打十個|
|王秀暐|資科碩三|111971025|團隊的中流砥柱，一個人打十個|

## Folder organization and its related description
idea by Noble WS (2009) [A Quick Guide to Organizing Computational Biology Projects.](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1000424) PLoS Comput Biol 5(7): e1000424.

### docs
* 簡報檔, 1132_DS-FP_group3.ppt , by **06.10**

* 系統使用手冊與討論紀錄
### data
data/

原始空氣品質與氣象資料（如 CSV）

處理後資料（如 parquet / feather）

### code
acquire.R: 抓取與整理 AQI 與氣象資料

features.R: 特徵工程與合併

modeling.R: 預測與分群模型訓練
### shiny-app/

global.R, ui.R, server.R

地圖顯示、指標查詢與異常分析

# 臺灣空氣品質監測與預測專案（Air-Quality-TW）

> 整合 **AQX_P_488** 空氣品質資料與中央氣象署 (CWA) 氣象觀測，  
> 從 **資料獲取 → 清理 / 特徵工程 → 時間序列 & XGBoost 預測 →  
> 分群 / 異常偵測 → Shiny 展示**  
> 建立一條可重複、可擴充的資料科學流程。

---
規劃連結: https://docs.google.com/document/d/1fWCmSwpUNJA2OCpSXNO9Z6GWopuk0UtO65z6cOMXtyc/edit?usp=sharing

---

## 1. 專案動機

空氣品質受到氣象條件強烈影響；單用 AQI 資料易低估光化學作用、降雨清洗等效果。  
本專案在期末報告框架基礎上，**新增氣象輔助變數**，同時確保：

- **長期趨勢**：STL / Prophet  
- **短期預報**：XGBoost → PM₂.₅、AQI 下一 1‒24 小時  
- **污染源分類**：K-Means / 階層式分群  
- **異常事件偵測**：IsolationForest / LOF  
- **互動溝通**：Shiny Dashboard + Leaflet 地圖

---

## 2. 目錄結構

```text
air-quality-tw/
├── data/               # raw / processed / features（Parquet）
├── notebooks/          # EDA & 實驗 Quarto / Jupyter
├── src/
│   ├── R/              # acquire.R, clean.R, features.R, modeling.R
│   └── py/             # 對應 Python 版本
├── models/             # 已訓練模型（Git-LFS 或 DVC 管理）
├── reports/            # Quarto 報告與圖表
├── shiny-app/          # global.R, ui.R, server.R, www/
├── tests/              # testthat / pytest
├── .github/workflows/  # CI：R CMD check、render docs、deploy Shiny
└── README.md
````

> **Tips**：大型逐時資料、模型檔皆使用 **Git LFS / DVC**，避免 clog repo。

---

## 3. 快速開始

### 3.1 先備條件

| 軟體             | 版本建議   | 角色             |
| -------------- | ------ | -------------- |
| R / RStudio    | ≥ 4.3  | 清理、特徵、Shiny    |
| Python / Conda | ≥ 3.10 | API 抓取、XGBoost |
| Git LFS        | 最新     | 管理大檔           |
| DVC *(可選)*     | 3.x    | 追蹤資料流程         |
| Quarto         | ≥ 1.4  | 報告 / notebook  |

### 3.2 安裝步驟

```bash
# 1. 取得程式碼
git clone https://github.com/<your-id>/air-quality-tw.git && cd air-quality-tw

# 2. 還原 R / Python 環境
R -e "install.packages('renv'); renv::restore()"
conda env create -f environment.yml && conda activate airq

# 3. 下載完整資料與模型
dvc pull        # 或 git lfs pull

# 4. 一鍵重跑 pipeline（Make / targets / snakemake 其一）
make all

# 5. 啟動 Shiny（本機）
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

## 5. 再現完整流程

| 階段          | Script / Notebook                | 主要輸出                       |
| ----------- | -------------------------------- | -------------------------- |
| 1️⃣ Acquire | `src/R/acquire.R` / `acquire.py` | `data/raw/*.csv`           |
| 2️⃣ Clean   | `src/R/clean.R`                  | `data/processed/*.parquet` |
| 3️⃣ Feature | `src/R/features.R`               | `data/features/*.parquet`  |
| 4️⃣ Model   | `src/R/modeling.R`               | `models/*.pkl` / `.rds`    |
| 5️⃣ Report  | `quarto render`                  | `reports/*.html`           |
| 6️⃣ Shiny   | `shiny-app/`                     | Web App (local / cloud)    |

CI（`.github/workflows/render-docs.yml`）在每次 push：

1. 還原環境 → 下載小型示例資料
2. 執行單元測試
3. 重建 Quarto 報告
4. 部署 Shiny 至 `shinyapps.io` 或伺服器

---

## 6. 貢獻指南

1. **Fork & Branch**：功能開發請在 `feature/<topic>` 分支。
2. **測試覆蓋**：新增 / 修改函式須附對應 `tests/`。
3. **開 PR**：說明背景、變更範圍、驗證方式。CI 通過後合併。
4. **Code Style**：R 使用 `styler`，Python 遵循 `black` + `isort`。

歡迎 issue / PR，一起讓臺灣空污預測更精準！

---

## 7. 引用

若本專案協助您的研究或開發，請引用：

```
Chan, J. (2025). Air-Quality-TW: Integrating CWA Meteorology with AQX_P_488 for Forecasting, Clustering and Anomaly Detection (Version v1.0) [Computer software]. https://github.com/<your-id>/air-quality-tw
```
---
MIT License © 2025




