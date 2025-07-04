
# separate_norm 模式模型訓練報告

## 基本信息
- **模式**: separate_norm
- **測站**: 湖口
- **時間戳**: 20250608_184615
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 7.35 秒
- **驗證集指標**:
  - MAE: 0.0869
  - RMSE: 0.1364
  - MAPE: 13626414.19%
  - R²: 0.9563

### LSTM 結果

- **訓練時間**: 8.41 秒
- **最終輪數**: 11
- **驗證集指標**:
  - MAE: 0.3398
  - RMSE: 0.5368
  - MAPE: 555942550.00%
  - R²: 0.4701

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.2529)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate_norm\separate_norm_湖口_20250608_184615_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate_norm\separate_norm_湖口_20250608_184615_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_norm_湖口_20250608_184615_evaluation.json
