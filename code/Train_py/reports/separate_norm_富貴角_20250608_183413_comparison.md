
# separate_norm 模式模型訓練報告

## 基本信息
- **模式**: separate_norm
- **測站**: 富貴角
- **時間戳**: 20250608_183413
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 6.08 秒
- **驗證集指標**:
  - MAE: 0.0806
  - RMSE: 0.1357
  - MAPE: 19193513.77%
  - R²: 0.9676

### LSTM 結果

- **訓練時間**: 9.59 秒
- **最終輪數**: 12
- **驗證集指標**:
  - MAE: 0.2634
  - RMSE: 0.4279
  - MAPE: 342778675.00%
  - R²: 0.5658

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.1828)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate_norm\separate_norm_富貴角_20250608_183413_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate_norm\separate_norm_富貴角_20250608_183413_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_norm_富貴角_20250608_183413_evaluation.json
