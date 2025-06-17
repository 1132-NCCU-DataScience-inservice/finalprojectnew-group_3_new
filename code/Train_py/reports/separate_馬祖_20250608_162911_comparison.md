
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 馬祖
- **時間戳**: 20250608_162911
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 7.29 秒
- **驗證集指標**:
  - MAE: 3.2123
  - RMSE: 5.6991
  - MAPE: 5.14%
  - R²: 0.9709

### LSTM 結果

- **訓練時間**: 18.07 秒
- **最終輪數**: 25
- **驗證集指標**:
  - MAE: 3.0886
  - RMSE: 6.7131
  - MAPE: 663291600.00%
  - R²: 0.9177

## 總結

- **較佳模型**: LSTM (MAE差異: 0.1238)
- **建議使用**: LSTM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_馬祖_20250608_162911_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_馬祖_20250608_162911_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_馬祖_20250608_162911_evaluation.json
