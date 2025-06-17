
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 三義
- **時間戳**: 20250608_154851
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 8.60 秒
- **驗證集指標**:
  - MAE: 2.5150
  - RMSE: 3.7053
  - MAPE: 5.86%
  - R²: 0.9671

### LSTM 結果

- **訓練時間**: 12.85 秒
- **最終輪數**: 16
- **驗證集指標**:
  - MAE: 3.0185
  - RMSE: 6.0480
  - MAPE: 302864175.00%
  - R²: 0.8752

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.5035)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_三義_20250608_154851_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_三義_20250608_154851_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_三義_20250608_154851_evaluation.json
