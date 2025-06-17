
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 恆春
- **時間戳**: 20250608_160713
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 3.73 秒
- **驗證集指標**:
  - MAE: 1.3143
  - RMSE: 2.8102
  - MAPE: 4.63%
  - R²: 0.9716

### LSTM 結果

- **訓練時間**: 14.33 秒
- **最終輪數**: 17
- **驗證集指標**:
  - MAE: 1.4882
  - RMSE: 3.3344
  - MAPE: 597121900.00%
  - R²: 0.9584

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.1739)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_恆春_20250608_160713_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_恆春_20250608_160713_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_恆春_20250608_160713_evaluation.json
