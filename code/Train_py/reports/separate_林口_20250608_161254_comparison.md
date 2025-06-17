
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 林口
- **時間戳**: 20250608_161254
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 7.01 秒
- **驗證集指標**:
  - MAE: 2.5345
  - RMSE: 3.8650
  - MAPE: 5.76%
  - R²: 0.9585

### LSTM 結果

- **訓練時間**: 14.41 秒
- **最終輪數**: 18
- **驗證集指標**:
  - MAE: 3.0453
  - RMSE: 6.1067
  - MAPE: 522791100.00%
  - R²: 0.8651

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.5108)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_林口_20250608_161254_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_林口_20250608_161254_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_林口_20250608_161254_evaluation.json
