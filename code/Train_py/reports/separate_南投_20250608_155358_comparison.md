
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 南投
- **時間戳**: 20250608_155358
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 13.51 秒
- **驗證集指標**:
  - MAE: 2.5760
  - RMSE: 3.6408
  - MAPE: 4.96%
  - R²: 0.9763

### LSTM 結果

- **訓練時間**: 15.87 秒
- **最終輪數**: 19
- **驗證集指標**:
  - MAE: 2.8623
  - RMSE: 5.8013
  - MAPE: 663248200.00%
  - R²: 0.9056

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.2863)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_南投_20250608_155358_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_南投_20250608_155358_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_南投_20250608_155358_evaluation.json
