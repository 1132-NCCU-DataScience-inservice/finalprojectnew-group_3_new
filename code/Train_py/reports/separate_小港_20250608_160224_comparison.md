
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 小港
- **時間戳**: 20250608_160224
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 9.02 秒
- **驗證集指標**:
  - MAE: 3.2931
  - RMSE: 4.7826
  - MAPE: 5.99%
  - R²: 0.9688

### LSTM 結果

- **訓練時間**: 17.29 秒
- **最終輪數**: 22
- **驗證集指標**:
  - MAE: 3.6403
  - RMSE: 7.2071
  - MAPE: 345282700.00%
  - R²: 0.8839

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.3472)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_小港_20250608_160224_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_小港_20250608_160224_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_小港_20250608_160224_evaluation.json
