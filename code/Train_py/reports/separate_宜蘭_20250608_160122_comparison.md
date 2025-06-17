
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 宜蘭
- **時間戳**: 20250608_160122
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 8.15 秒
- **驗證集指標**:
  - MAE: 2.0252
  - RMSE: 3.3578
  - MAPE: 5.41%
  - R²: 0.9530

### LSTM 結果

- **訓練時間**: 14.38 秒
- **最終輪數**: 18
- **驗證集指標**:
  - MAE: 2.0360
  - RMSE: 4.1933
  - MAPE: 577923550.00%
  - R²: 0.9164

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.0108)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_宜蘭_20250608_160122_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_宜蘭_20250608_160122_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_宜蘭_20250608_160122_evaluation.json
