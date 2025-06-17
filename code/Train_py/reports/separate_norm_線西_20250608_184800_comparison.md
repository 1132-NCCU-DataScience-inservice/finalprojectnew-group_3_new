
# separate_norm 模式模型訓練報告

## 基本信息
- **模式**: separate_norm
- **測站**: 線西
- **時間戳**: 20250608_184800
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 9.47 秒
- **驗證集指標**:
  - MAE: 0.0800
  - RMSE: 0.1212
  - MAPE: 12033953.24%
  - R²: 0.9636

### LSTM 結果

- **訓練時間**: 9.04 秒
- **最終輪數**: 12
- **驗證集指標**:
  - MAE: 0.3155
  - RMSE: 0.4902
  - MAPE: 458317150.00%
  - R²: 0.5485

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.2354)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate_norm\separate_norm_線西_20250608_184800_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate_norm\separate_norm_線西_20250608_184800_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_norm_線西_20250608_184800_evaluation.json
