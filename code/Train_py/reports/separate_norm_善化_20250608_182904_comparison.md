
# separate_norm 模式模型訓練報告

## 基本信息
- **模式**: separate_norm
- **測站**: 善化
- **時間戳**: 20250608_182904
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 9.05 秒
- **驗證集指標**:
  - MAE: 0.0594
  - RMSE: 0.0954
  - MAPE: 8758204.11%
  - R²: 0.9680

### LSTM 結果

- **訓練時間**: 9.00 秒
- **最終輪數**: 12
- **驗證集指標**:
  - MAE: 0.2313
  - RMSE: 0.3718
  - MAPE: 395310275.00%
  - R²: 0.6022

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.1719)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate_norm\separate_norm_善化_20250608_182904_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate_norm\separate_norm_善化_20250608_182904_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_norm_善化_20250608_182904_evaluation.json
