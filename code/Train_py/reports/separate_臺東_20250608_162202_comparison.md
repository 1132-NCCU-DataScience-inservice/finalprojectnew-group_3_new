
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 臺東
- **時間戳**: 20250608_162202
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 5.82 秒
- **驗證集指標**:
  - MAE: 1.4743
  - RMSE: 2.5734
  - MAPE: 4.55%
  - R²: 0.9623

### LSTM 結果

- **訓練時間**: 15.53 秒
- **最終輪數**: 19
- **驗證集指標**:
  - MAE: 1.8425
  - RMSE: 3.7980
  - MAPE: 488293700.00%
  - R²: 0.9243

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.3682)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_臺東_20250608_162202_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_臺東_20250608_162202_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_臺東_20250608_162202_evaluation.json
