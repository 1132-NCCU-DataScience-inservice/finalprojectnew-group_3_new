
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 淡水
- **時間戳**: 20250608_161724
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 7.10 秒
- **驗證集指標**:
  - MAE: 2.5017
  - RMSE: 3.9697
  - MAPE: 5.74%
  - R²: 0.9567

### LSTM 結果

- **訓練時間**: 13.00 秒
- **最終輪數**: 16
- **驗證集指標**:
  - MAE: 3.0783
  - RMSE: 6.0745
  - MAPE: 319658675.00%
  - R²: 0.8739

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.5765)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_淡水_20250608_161724_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_淡水_20250608_161724_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_淡水_20250608_161724_evaluation.json
