
# separate_norm 模式模型訓練報告

## 基本信息
- **模式**: separate_norm
- **測站**: 大同
- **時間戳**: 20250608_183137
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 8.98 秒
- **驗證集指標**:
  - MAE: 0.1195
  - RMSE: 0.1699
  - MAPE: 16400811.44%
  - R²: 0.9449

### LSTM 結果

- **訓練時間**: 10.79 秒
- **最終輪數**: 14
- **驗證集指標**:
  - MAE: 0.2914
  - RMSE: 0.4306
  - MAPE: 251649525.00%
  - R²: 0.5735

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.1719)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate_norm\separate_norm_大同_20250608_183137_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate_norm\separate_norm_大同_20250608_183137_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_norm_大同_20250608_183137_evaluation.json
