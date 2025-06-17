
# separate_norm 模式模型訓練報告

## 基本信息
- **模式**: separate_norm
- **測站**: 林園
- **時間戳**: 20250608_184241
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 11.49 秒
- **驗證集指標**:
  - MAE: 0.0629
  - RMSE: 0.0937
  - MAPE: 11121933.19%
  - R²: 0.9732

### LSTM 結果

- **訓練時間**: 8.95 秒
- **最終輪數**: 12
- **驗證集指標**:
  - MAE: 0.2460
  - RMSE: 0.4218
  - MAPE: 357399675.00%
  - R²: 0.6164

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.1831)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate_norm\separate_norm_林園_20250608_184241_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate_norm\separate_norm_林園_20250608_184241_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_norm_林園_20250608_184241_evaluation.json
