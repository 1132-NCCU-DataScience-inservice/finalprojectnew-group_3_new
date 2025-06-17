
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 楠梓
- **時間戳**: 20250608_161430
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 11.00 秒
- **驗證集指標**:
  - MAE: 3.1812
  - RMSE: 4.8607
  - MAPE: 5.56%
  - R²: 0.9687

### LSTM 結果

- **訓練時間**: 15.75 秒
- **最終輪數**: 20
- **驗證集指標**:
  - MAE: 3.4802
  - RMSE: 6.9782
  - MAPE: 442054950.00%
  - R²: 0.9012

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.2990)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_楠梓_20250608_161430_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_楠梓_20250608_161430_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_楠梓_20250608_161430_evaluation.json
