
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 仁武
- **時間戳**: 20250608_155141
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 7.94 秒
- **驗證集指標**:
  - MAE: 3.2445
  - RMSE: 5.0413
  - MAPE: 5.12%
  - R²: 0.9722

### LSTM 結果

- **訓練時間**: 19.01 秒
- **最終輪數**: 24
- **驗證集指標**:
  - MAE: 3.2986
  - RMSE: 6.7228
  - MAPE: 318866875.00%
  - R²: 0.9080

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.0540)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_仁武_20250608_155141_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_仁武_20250608_155141_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_仁武_20250608_155141_evaluation.json
