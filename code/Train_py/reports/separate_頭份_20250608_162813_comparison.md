
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 頭份
- **時間戳**: 20250608_162813
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 8.28 秒
- **驗證集指標**:
  - MAE: 2.5667
  - RMSE: 3.7809
  - MAPE: 4.95%
  - R²: 0.9691

### LSTM 結果

- **訓練時間**: 13.94 秒
- **最終輪數**: 19
- **驗證集指標**:
  - MAE: 2.9379
  - RMSE: 6.0568
  - MAPE: 166617525.00%
  - R²: 0.8860

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.3712)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_頭份_20250608_162813_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_頭份_20250608_162813_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_頭份_20250608_162813_evaluation.json
