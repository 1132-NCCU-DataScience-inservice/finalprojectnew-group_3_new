
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 大園
- **時間戳**: 20250608_155857
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 6.11 秒
- **驗證集指標**:
  - MAE: 2.7522
  - RMSE: 4.1364
  - MAPE: 5.66%
  - R²: 0.9628

### LSTM 結果

- **訓練時間**: 13.79 秒
- **最終輪數**: 17
- **驗證集指標**:
  - MAE: 3.2268
  - RMSE: 6.3973
  - MAPE: 458810550.00%
  - R²: 0.8701

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.4746)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_大園_20250608_155857_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_大園_20250608_155857_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_大園_20250608_155857_evaluation.json
