
# separate_norm 模式模型訓練報告

## 基本信息
- **模式**: separate_norm
- **測站**: 三義
- **時間戳**: 20250608_182418
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 8.94 秒
- **驗證集指標**:
  - MAE: 0.0811
  - RMSE: 0.1243
  - MAPE: 16472544.43%
  - R²: 0.9633

### LSTM 結果

- **訓練時間**: 10.14 秒
- **最終輪數**: 12
- **驗證集指標**:
  - MAE: 0.3072
  - RMSE: 0.4698
  - MAPE: 455943150.00%
  - R²: 0.4916

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.2261)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate_norm\separate_norm_三義_20250608_182418_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate_norm\separate_norm_三義_20250608_182418_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_norm_三義_20250608_182418_evaluation.json
