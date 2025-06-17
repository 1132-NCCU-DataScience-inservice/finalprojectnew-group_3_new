
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 二林
- **時間戳**: 20250608_155102
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 9.15 秒
- **驗證集指標**:
  - MAE: 3.4649
  - RMSE: 5.1177
  - MAPE: 5.14%
  - R²: 0.9665

### LSTM 結果

- **訓練時間**: 21.89 秒
- **最終輪數**: 28
- **驗證集指標**:
  - MAE: 4.1508
  - RMSE: 8.4393
  - MAPE: 356830550.00%
  - R²: 0.8813

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.6859)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_二林_20250608_155102_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_二林_20250608_155102_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_二林_20250608_155102_evaluation.json
