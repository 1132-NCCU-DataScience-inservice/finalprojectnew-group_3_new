
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 彰化
- **時間戳**: 20250608_160522
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 13.34 秒
- **驗證集指標**:
  - MAE: 2.6916
  - RMSE: 3.8081
  - MAPE: 5.61%
  - R²: 0.9697

### LSTM 結果

- **訓練時間**: 15.35 秒
- **最終輪數**: 19
- **驗證集指標**:
  - MAE: 3.2654
  - RMSE: 6.3499
  - MAPE: 633111100.00%
  - R²: 0.8795

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.5737)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_彰化_20250608_160522_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_彰化_20250608_160522_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_彰化_20250608_160522_evaluation.json
