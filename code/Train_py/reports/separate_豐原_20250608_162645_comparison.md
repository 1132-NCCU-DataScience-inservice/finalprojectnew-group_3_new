
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 豐原
- **時間戳**: 20250608_162645
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 7.77 秒
- **驗證集指標**:
  - MAE: 2.5142
  - RMSE: 3.5662
  - MAPE: 5.25%
  - R²: 0.9712

### LSTM 結果

- **訓練時間**: 12.60 秒
- **最終輪數**: 17
- **驗證集指標**:
  - MAE: 3.1031
  - RMSE: 6.1471
  - MAPE: 418601750.00%
  - R²: 0.8778

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.5889)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_豐原_20250608_162645_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_豐原_20250608_162645_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_豐原_20250608_162645_evaluation.json
