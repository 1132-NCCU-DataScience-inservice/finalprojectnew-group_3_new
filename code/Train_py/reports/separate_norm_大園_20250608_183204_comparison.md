
# separate_norm 模式模型訓練報告

## 基本信息
- **模式**: separate_norm
- **測站**: 大園
- **時間戳**: 20250608_183204
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 4.98 秒
- **驗證集指標**:
  - MAE: 0.1055
  - RMSE: 0.1590
  - MAPE: 13946209.15%
  - R²: 0.9595

### LSTM 結果

- **訓練時間**: 9.75 秒
- **最終輪數**: 13
- **驗證集指標**:
  - MAE: 0.3034
  - RMSE: 0.4856
  - MAPE: 292485500.00%
  - R²: 0.5103

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.1980)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate_norm\separate_norm_大園_20250608_183204_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate_norm\separate_norm_大園_20250608_183204_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_norm_大園_20250608_183204_evaluation.json
