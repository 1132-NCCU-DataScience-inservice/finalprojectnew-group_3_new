
# separate_norm 模式模型訓練報告

## 基本信息
- **模式**: separate_norm
- **測站**: 嘉義
- **時間戳**: 20250608_182930
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 8.17 秒
- **驗證集指標**:
  - MAE: 0.0550
  - RMSE: 0.0821
  - MAPE: 6268676.24%
  - R²: 0.9773

### LSTM 結果

- **訓練時間**: 8.93 秒
- **最終輪數**: 12
- **驗證集指標**:
  - MAE: 0.2480
  - RMSE: 0.4029
  - MAPE: 398071800.00%
  - R²: 0.6217

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.1931)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate_norm\separate_norm_嘉義_20250608_182930_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate_norm\separate_norm_嘉義_20250608_182930_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_norm_嘉義_20250608_182930_evaluation.json
