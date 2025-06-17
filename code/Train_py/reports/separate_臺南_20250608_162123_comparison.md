
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 臺南
- **時間戳**: 20250608_162123
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 10.07 秒
- **驗證集指標**:
  - MAE: 3.0179
  - RMSE: 4.5614
  - MAPE: 5.01%
  - R²: 0.9765

### LSTM 結果

- **訓練時間**: 19.80 秒
- **最終輪數**: 25
- **驗證集指標**:
  - MAE: 3.2728
  - RMSE: 6.7645
  - MAPE: 400236325.00%
  - R²: 0.9085

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.2549)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_臺南_20250608_162123_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_臺南_20250608_162123_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_臺南_20250608_162123_evaluation.json
