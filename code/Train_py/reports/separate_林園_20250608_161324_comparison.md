
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 林園
- **時間戳**: 20250608_161324
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 12.24 秒
- **驗證集指標**:
  - MAE: 3.3513
  - RMSE: 5.0695
  - MAPE: 5.47%
  - R²: 0.9740

### LSTM 結果

- **訓練時間**: 16.63 秒
- **最終輪數**: 21
- **驗證集指標**:
  - MAE: 3.3976
  - RMSE: 7.3517
  - MAPE: 335298625.00%
  - R²: 0.9027

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.0462)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_林園_20250608_161324_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_林園_20250608_161324_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_林園_20250608_161324_evaluation.json
