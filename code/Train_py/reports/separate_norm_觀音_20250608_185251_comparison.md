
# separate_norm 模式模型訓練報告

## 基本信息
- **模式**: separate_norm
- **測站**: 觀音
- **時間戳**: 20250608_185251
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 6.20 秒
- **驗證集指標**:
  - MAE: 0.1079
  - RMSE: 0.2050
  - MAPE: 18367432.95%
  - R²: 0.9316

### LSTM 結果

- **訓練時間**: 9.01 秒
- **最終輪數**: 12
- **驗證集指標**:
  - MAE: 0.2925
  - RMSE: 0.4471
  - MAPE: 377437625.00%
  - R²: 0.5546

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.1845)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate_norm\separate_norm_觀音_20250608_185251_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate_norm\separate_norm_觀音_20250608_185251_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_norm_觀音_20250608_185251_evaluation.json
