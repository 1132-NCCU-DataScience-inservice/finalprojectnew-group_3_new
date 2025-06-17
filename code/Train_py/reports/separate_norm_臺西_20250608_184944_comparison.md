
# separate_norm 模式模型訓練報告

## 基本信息
- **模式**: separate_norm
- **測站**: 臺西
- **時間戳**: 20250608_184944
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 11.12 秒
- **驗證集指標**:
  - MAE: 0.0873
  - RMSE: 0.1519
  - MAPE: 29059164.92%
  - R²: 0.9516

### LSTM 結果

- **訓練時間**: 9.68 秒
- **最終輪數**: 13
- **驗證集指標**:
  - MAE: 0.3359
  - RMSE: 0.4977
  - MAPE: 564269750.00%
  - R²: 0.5083

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.2485)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate_norm\separate_norm_臺西_20250608_184944_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate_norm\separate_norm_臺西_20250608_184944_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_norm_臺西_20250608_184944_evaluation.json
