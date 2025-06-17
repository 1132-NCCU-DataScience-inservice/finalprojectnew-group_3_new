
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 大同
- **時間戳**: 20250608_155818
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 9.28 秒
- **驗證集指標**:
  - MAE: 2.9180
  - RMSE: 3.9312
  - MAPE: 5.07%
  - R²: 0.9593

### LSTM 結果

- **訓練時間**: 20.68 秒
- **最終輪數**: 26
- **驗證集指標**:
  - MAE: 4.7571
  - RMSE: 9.5605
  - MAPE: 423225650.00%
  - R²: 0.8067

## 總結

- **較佳模型**: LightGBM (MAE差異: 1.8391)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_大同_20250608_155818_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_大同_20250608_155818_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_大同_20250608_155818_evaluation.json
