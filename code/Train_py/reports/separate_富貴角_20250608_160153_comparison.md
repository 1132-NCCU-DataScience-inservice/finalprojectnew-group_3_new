
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 富貴角
- **時間戳**: 20250608_160153
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 5.03 秒
- **驗證集指標**:
  - MAE: 2.1143
  - RMSE: 3.6904
  - MAPE: 4.66%
  - R²: 0.9702

### LSTM 結果

- **訓練時間**: 18.30 秒
- **最終輪數**: 23
- **驗證集指標**:
  - MAE: 2.6461
  - RMSE: 5.8562
  - MAPE: 257417350.00%
  - R²: 0.9243

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.5317)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_富貴角_20250608_160153_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_富貴角_20250608_160153_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_富貴角_20250608_160153_evaluation.json
