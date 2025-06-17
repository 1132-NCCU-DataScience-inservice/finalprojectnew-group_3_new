
# separate_norm 模式模型訓練報告

## 基本信息
- **模式**: separate_norm
- **測站**: 斗六
- **時間戳**: 20250608_183829
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 9.45 秒
- **驗證集指標**:
  - MAE: 0.0582
  - RMSE: 0.0885
  - MAPE: 5734688.26%
  - R²: 0.9747

### LSTM 結果

- **訓練時間**: 9.11 秒
- **最終輪數**: 12
- **驗證集指標**:
  - MAE: 0.2598
  - RMSE: 0.4024
  - MAPE: 426295900.00%
  - R²: 0.6127

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.2015)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate_norm\separate_norm_斗六_20250608_183829_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate_norm\separate_norm_斗六_20250608_183829_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_norm_斗六_20250608_183829_evaluation.json
