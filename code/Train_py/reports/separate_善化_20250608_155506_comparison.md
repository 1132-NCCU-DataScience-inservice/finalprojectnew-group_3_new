
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 善化
- **時間戳**: 20250608_155506
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 12.82 秒
- **驗證集指標**:
  - MAE: 2.9575
  - RMSE: 4.6574
  - MAPE: 5.14%
  - R²: 0.9666

### LSTM 結果

- **訓練時間**: 16.80 秒
- **最終輪數**: 21
- **驗證集指標**:
  - MAE: 3.0576
  - RMSE: 6.4709
  - MAPE: 289177175.00%
  - R²: 0.9079

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.1000)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_善化_20250608_155506_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_善化_20250608_155506_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_善化_20250608_155506_evaluation.json
