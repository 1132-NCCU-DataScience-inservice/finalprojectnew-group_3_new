
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 竹山
- **時間戳**: 20250608_161858
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 9.96 秒
- **驗證集指標**:
  - MAE: 2.8921
  - RMSE: 4.0131
  - MAPE: 4.45%
  - R²: 0.9761

### LSTM 結果

- **訓練時間**: 14.46 秒
- **最終輪數**: 18
- **驗證集指標**:
  - MAE: 3.1117
  - RMSE: 6.3302
  - MAPE: 467174200.00%
  - R²: 0.9158

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.2197)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_竹山_20250608_161858_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_竹山_20250608_161858_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_竹山_20250608_161858_evaluation.json
