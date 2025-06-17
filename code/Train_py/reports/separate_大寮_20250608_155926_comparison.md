
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 大寮
- **時間戳**: 20250608_155926
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 12.12 秒
- **驗證集指標**:
  - MAE: 3.3898
  - RMSE: 5.1095
  - MAPE: 5.57%
  - R²: 0.9698

### LSTM 結果

- **訓練時間**: 16.68 秒
- **最終輪數**: 21
- **驗證集指標**:
  - MAE: 3.6164
  - RMSE: 7.4011
  - MAPE: 330729975.00%
  - R²: 0.8917

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.2266)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_大寮_20250608_155926_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_大寮_20250608_155926_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_大寮_20250608_155926_evaluation.json
