
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 新竹
- **時間戳**: 20250608_161002
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 7.52 秒
- **驗證集指標**:
  - MAE: 2.7684
  - RMSE: 4.1270
  - MAPE: 5.48%
  - R²: 0.9681

### LSTM 結果

- **訓練時間**: 14.99 秒
- **最終輪數**: 18
- **驗證集指標**:
  - MAE: 2.8841
  - RMSE: 6.0339
  - MAPE: 570131450.00%
  - R²: 0.8819

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.1157)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_新竹_20250608_161002_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_新竹_20250608_161002_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_新竹_20250608_161002_evaluation.json
