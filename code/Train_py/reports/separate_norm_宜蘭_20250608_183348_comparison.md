
# separate_norm 模式模型訓練報告

## 基本信息
- **模式**: separate_norm
- **測站**: 宜蘭
- **時間戳**: 20250608_183348
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 7.39 秒
- **驗證集指標**:
  - MAE: 0.1142
  - RMSE: 0.1870
  - MAPE: 27744449.30%
  - R²: 0.9533

### LSTM 結果

- **訓練時間**: 9.70 秒
- **最終輪數**: 13
- **驗證集指標**:
  - MAE: 0.2893
  - RMSE: 0.4619
  - MAPE: 436715450.00%
  - R²: 0.6032

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.1751)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate_norm\separate_norm_宜蘭_20250608_183348_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate_norm\separate_norm_宜蘭_20250608_183348_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_norm_宜蘭_20250608_183348_evaluation.json
