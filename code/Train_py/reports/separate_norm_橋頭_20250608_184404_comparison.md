
# separate_norm 模式模型訓練報告

## 基本信息
- **模式**: separate_norm
- **測站**: 橋頭
- **時間戳**: 20250608_184404
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 9.16 秒
- **驗證集指標**:
  - MAE: 0.0575
  - RMSE: 0.0855
  - MAPE: 7737689.21%
  - R²: 0.9762

### LSTM 結果

- **訓練時間**: 10.44 秒
- **最終輪數**: 14
- **驗證集指標**:
  - MAE: 0.2632
  - RMSE: 0.4269
  - MAPE: 436968700.00%
  - R²: 0.5589

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.2057)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate_norm\separate_norm_橋頭_20250608_184404_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate_norm\separate_norm_橋頭_20250608_184404_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_norm_橋頭_20250608_184404_evaluation.json
