
# separate_norm 模式模型訓練報告

## 基本信息
- **模式**: separate_norm
- **測站**: 林口
- **時間戳**: 20250608_184219
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 4.73 秒
- **驗證集指標**:
  - MAE: 0.1175
  - RMSE: 0.1939
  - MAPE: 26208159.09%
  - R²: 0.9421

### LSTM 結果

- **訓練時間**: 9.12 秒
- **最終輪數**: 12
- **驗證集指標**:
  - MAE: 0.2777
  - RMSE: 0.4560
  - MAPE: 211187150.00%
  - R²: 0.5418

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.1602)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate_norm\separate_norm_林口_20250608_184219_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate_norm\separate_norm_林口_20250608_184219_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_norm_林口_20250608_184219_evaluation.json
