
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 新店
- **時間戳**: 20250608_160815
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 6.89 秒
- **驗證集指標**:
  - MAE: 2.6917
  - RMSE: 4.1326
  - MAPE: 5.56%
  - R²: 0.9565

### LSTM 結果

- **訓練時間**: 16.08 秒
- **最終輪數**: 20
- **驗證集指標**:
  - MAE: 2.6319
  - RMSE: 5.5040
  - MAPE: 428012450.00%
  - R²: 0.8947

## 總結

- **較佳模型**: LSTM (MAE差異: 0.0598)
- **建議使用**: LSTM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_新店_20250608_160815_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_新店_20250608_160815_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_新店_20250608_160815_evaluation.json
