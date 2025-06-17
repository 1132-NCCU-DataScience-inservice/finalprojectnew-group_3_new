
# separate_norm 模式模型訓練報告

## 基本信息
- **模式**: separate_norm
- **測站**: 淡水
- **時間戳**: 20250608_184551
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 6.32 秒
- **驗證集指標**:
  - MAE: 0.1132
  - RMSE: 0.1924
  - MAPE: 22992270.59%
  - R²: 0.9448

### LSTM 結果

- **訓練時間**: 9.04 秒
- **最終輪數**: 12
- **驗證集指標**:
  - MAE: 0.3237
  - RMSE: 0.5433
  - MAPE: 389515125.00%
  - R²: 0.4459

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.2105)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate_norm\separate_norm_淡水_20250608_184551_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate_norm\separate_norm_淡水_20250608_184551_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_norm_淡水_20250608_184551_evaluation.json
