
# separate_norm 模式模型訓練報告

## 基本信息
- **模式**: separate_norm
- **測站**: 朴子
- **時間戳**: 20250608_184102
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 8.43 秒
- **驗證集指標**:
  - MAE: 0.0666
  - RMSE: 0.1001
  - MAPE: 7410419.12%
  - R²: 0.9717

### LSTM 結果

- **訓練時間**: 8.33 秒
- **最終輪數**: 11
- **驗證集指標**:
  - MAE: 0.2922
  - RMSE: 0.4559
  - MAPE: 476272750.00%
  - R²: 0.5716

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.2256)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate_norm\separate_norm_朴子_20250608_184102_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate_norm\separate_norm_朴子_20250608_184102_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_norm_朴子_20250608_184102_evaluation.json
