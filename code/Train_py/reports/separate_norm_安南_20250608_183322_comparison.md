
# separate_norm 模式模型訓練報告

## 基本信息
- **模式**: separate_norm
- **測站**: 安南
- **時間戳**: 20250608_183322
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 8.63 秒
- **驗證集指標**:
  - MAE: 0.0620
  - RMSE: 0.0906
  - MAPE: 8333216.83%
  - R²: 0.9748

### LSTM 結果

- **訓練時間**: 9.04 秒
- **最終輪數**: 12
- **驗證集指標**:
  - MAE: 0.2594
  - RMSE: 0.3944
  - MAPE: 365162675.00%
  - R²: 0.6236

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.1974)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate_norm\separate_norm_安南_20250608_183322_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate_norm\separate_norm_安南_20250608_183322_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_norm_安南_20250608_183322_evaluation.json
