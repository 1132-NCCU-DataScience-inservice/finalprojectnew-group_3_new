
# separate_norm 模式模型訓練報告

## 基本信息
- **模式**: separate_norm
- **測站**: 南投
- **時間戳**: 20250608_182809
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 9.29 秒
- **驗證集指標**:
  - MAE: 0.0630
  - RMSE: 0.0888
  - MAPE: 5905564.91%
  - R²: 0.9751

### LSTM 結果

- **訓練時間**: 9.69 秒
- **最終輪數**: 13
- **驗證集指標**:
  - MAE: 0.2473
  - RMSE: 0.4141
  - MAPE: 351018975.00%
  - R²: 0.5808

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.1843)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate_norm\separate_norm_南投_20250608_182809_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate_norm\separate_norm_南投_20250608_182809_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_norm_南投_20250608_182809_evaluation.json
