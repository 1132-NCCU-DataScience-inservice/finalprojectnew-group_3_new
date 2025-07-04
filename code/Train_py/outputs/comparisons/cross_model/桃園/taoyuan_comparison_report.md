# 桃園站 LSTM vs LightGBM 模型比較報告

**生成時間**: 2025-06-07T17:30:38.622770

## 📊 訓練結果

| 模型 | 狀態 | 訓練時間(秒) | 模型大小(MB) |
|------|------|-------------|-------------|
| LGBM | success | 702.2 | 298.9 |
| LSTM | success | 300.0 | 0.1 |

## 📈 性能評估

### LGBM 模型指標

**AQI_pm2.5_h+1**:
- MAE: 0.476
- RMSE: 0.642
- MAPE: 230763893.678%

## 🎯 目標達成狀況

| 指標 | 目標 | LightGBM | LSTM |
|------|------|----------|------|
| PM2.5 MAE | ≤ 6.0 | ✅ 0.476 | N/A |

## 💡 建議

1. 💡 推薦使用LSTM：在預測準確度方面表現更佳
2. ✅ 有一個模型達到目標，可進一步優化另一個模型

## 📁 相關檔案

- 比較圖表: `taoyuan_model_comparison.png`
- 詳細數據: `taoyuan_comparison_report.json`
