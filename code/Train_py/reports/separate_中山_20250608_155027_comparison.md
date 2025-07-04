
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 中山
- **時間戳**: 20250608_155027
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 8.28 秒
- **驗證集指標**:
  - MAE: 3.1431
  - RMSE: 4.6770
  - MAPE: 6.96%
  - R²: 0.9431

### LSTM 結果

- **訓練時間**: 17.81 秒
- **最終輪數**: 23
- **驗證集指標**:
  - MAE: 3.5041
  - RMSE: 6.7011
  - MAPE: 554016150.00%
  - R²: 0.8518

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.3610)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_中山_20250608_155027_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_中山_20250608_155027_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_中山_20250608_155027_evaluation.json
