
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 朴子
- **時間戳**: 20250608_161104
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 9.88 秒
- **驗證集指標**:
  - MAE: 3.0433
  - RMSE: 4.6319
  - MAPE: 5.15%
  - R²: 0.9704

### LSTM 結果

- **訓練時間**: 24.96 秒
- **最終輪數**: 31
- **驗證集指標**:
  - MAE: 3.2655
  - RMSE: 6.9008
  - MAPE: 454917600.00%
  - R²: 0.8986

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.2223)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_朴子_20250608_161104_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_朴子_20250608_161104_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_朴子_20250608_161104_evaluation.json
