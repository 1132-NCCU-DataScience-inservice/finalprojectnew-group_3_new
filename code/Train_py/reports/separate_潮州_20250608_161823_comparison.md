
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 潮州
- **時間戳**: 20250608_161823
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 10.22 秒
- **驗證集指標**:
  - MAE: 3.2388
  - RMSE: 5.0351
  - MAPE: 6.20%
  - R²: 0.9745

### LSTM 結果

- **訓練時間**: 16.73 秒
- **最終輪數**: 21
- **驗證集指標**:
  - MAE: 3.1013
  - RMSE: 6.8151
  - MAPE: 485891200.00%
  - R²: 0.9006

## 總結

- **較佳模型**: LSTM (MAE差異: 0.1375)
- **建議使用**: LSTM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_潮州_20250608_161823_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_潮州_20250608_161823_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_潮州_20250608_161823_evaluation.json
