
# separate_norm 模式模型訓練報告

## 基本信息
- **模式**: separate_norm
- **測站**: 豐原
- **時間戳**: 20250608_185314
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 11.73 秒
- **驗證集指標**:
  - MAE: 0.0669
  - RMSE: 0.1072
  - MAPE: 13702783.00%
  - R²: 0.9679

### LSTM 結果

- **訓練時間**: 10.44 秒
- **最終輪數**: 14
- **驗證集指標**:
  - MAE: 0.3149
  - RMSE: 0.4841
  - MAPE: 531289250.00%
  - R²: 0.5201

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.2480)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate_norm\separate_norm_豐原_20250608_185314_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate_norm\separate_norm_豐原_20250608_185314_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_norm_豐原_20250608_185314_evaluation.json
