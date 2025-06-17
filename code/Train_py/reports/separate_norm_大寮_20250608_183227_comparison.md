
# separate_norm 模式模型訓練報告

## 基本信息
- **模式**: separate_norm
- **測站**: 大寮
- **時間戳**: 20250608_183227
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 13.25 秒
- **驗證集指標**:
  - MAE: 0.0663
  - RMSE: 0.1000
  - MAPE: 9662604.06%
  - R²: 0.9709

### LSTM 結果

- **訓練時間**: 9.05 秒
- **最終輪數**: 12
- **驗證集指標**:
  - MAE: 0.2747
  - RMSE: 0.4564
  - MAPE: 383887350.00%
  - R²: 0.5361

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.2084)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate_norm\separate_norm_大寮_20250608_183227_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate_norm\separate_norm_大寮_20250608_183227_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_norm_大寮_20250608_183227_evaluation.json
