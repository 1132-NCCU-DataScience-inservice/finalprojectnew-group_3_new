
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 臺西
- **時間戳**: 20250608_162232
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 10.53 秒
- **驗證集指標**:
  - MAE: 2.8910
  - RMSE: 4.6963
  - MAPE: 6.23%
  - R²: 0.9624

### LSTM 結果

- **訓練時間**: 19.35 秒
- **最終輪數**: 25
- **驗證集指標**:
  - MAE: 3.2975
  - RMSE: 6.6418
  - MAPE: 435218850.00%
  - R²: 0.8947

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.4065)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_臺西_20250608_162232_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_臺西_20250608_162232_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_臺西_20250608_162232_evaluation.json
