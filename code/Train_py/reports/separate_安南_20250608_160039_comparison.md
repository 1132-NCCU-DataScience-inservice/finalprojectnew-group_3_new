
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 安南
- **時間戳**: 20250608_160039
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 12.83 秒
- **驗證集指標**:
  - MAE: 3.0311
  - RMSE: 4.5724
  - MAPE: 4.88%
  - R²: 0.9725

### LSTM 結果

- **訓練時間**: 21.62 秒
- **最終輪數**: 28
- **驗證集指標**:
  - MAE: 3.4868
  - RMSE: 7.0814
  - MAPE: 505197800.00%
  - R²: 0.9009

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.4557)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_安南_20250608_160039_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_安南_20250608_160039_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_安南_20250608_160039_evaluation.json
