
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 橋頭
- **時間戳**: 20250608_161505
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 11.18 秒
- **驗證集指標**:
  - MAE: 3.2029
  - RMSE: 4.9723
  - MAPE: 5.29%
  - R²: 0.9723

### LSTM 結果

- **訓練時間**: 16.37 秒
- **最終輪數**: 20
- **驗證集指標**:
  - MAE: 3.4714
  - RMSE: 7.0523
  - MAPE: 305798450.00%
  - R²: 0.9019

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.2685)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_橋頭_20250608_161505_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_橋頭_20250608_161505_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_橋頭_20250608_161505_evaluation.json
