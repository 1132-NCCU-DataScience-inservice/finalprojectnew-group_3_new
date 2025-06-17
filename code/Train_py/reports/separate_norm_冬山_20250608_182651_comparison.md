
# separate_norm 模式模型訓練報告

## 基本信息
- **模式**: separate_norm
- **測站**: 冬山
- **時間戳**: 20250608_182651
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 8.07 秒
- **驗證集指標**:
  - MAE: 0.1084
  - RMSE: 0.1665
  - MAPE: 40183241.68%
  - R²: 0.9521

### LSTM 結果

- **訓練時間**: 9.71 秒
- **最終輪數**: 13
- **驗證集指標**:
  - MAE: 0.2614
  - RMSE: 0.4303
  - MAPE: 263228675.00%
  - R²: 0.5553

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.1530)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate_norm\separate_norm_冬山_20250608_182651_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate_norm\separate_norm_冬山_20250608_182651_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_norm_冬山_20250608_182651_evaluation.json
