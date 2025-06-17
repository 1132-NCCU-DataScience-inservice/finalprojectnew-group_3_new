
# separate_norm 模式模型訓練報告

## 基本信息
- **模式**: separate_norm
- **測站**: 三重
- **時間戳**: 20250608_182445
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 6.97 秒
- **驗證集指標**:
  - MAE: 0.1540
  - RMSE: 0.2194
  - MAPE: 42376545.33%
  - R²: 0.9160

### LSTM 結果

- **訓練時間**: 8.96 秒
- **最終輪數**: 12
- **驗證集指標**:
  - MAE: 0.2785
  - RMSE: 0.4331
  - MAPE: 233769125.00%
  - R²: 0.5657

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.1245)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate_norm\separate_norm_三重_20250608_182445_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate_norm\separate_norm_三重_20250608_182445_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_norm_三重_20250608_182445_evaluation.json
