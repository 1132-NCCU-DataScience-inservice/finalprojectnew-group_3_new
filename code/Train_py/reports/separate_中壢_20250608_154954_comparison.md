
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 中壢
- **時間戳**: 20250608_154954
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 7.73 秒
- **驗證集指標**:
  - MAE: 3.2648
  - RMSE: 4.4861
  - MAPE: 6.34%
  - R²: 0.9579

### LSTM 結果

- **訓練時間**: 17.71 秒
- **最終輪數**: 22
- **驗證集指標**:
  - MAE: 4.2490
  - RMSE: 8.1212
  - MAPE: 287970000.00%
  - R²: 0.8318

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.9842)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_中壢_20250608_154954_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_中壢_20250608_154954_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_中壢_20250608_154954_evaluation.json
