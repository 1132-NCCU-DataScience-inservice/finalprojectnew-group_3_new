
# separate_norm 模式模型訓練報告

## 基本信息
- **模式**: separate_norm
- **測站**: 花蓮
- **時間戳**: 20250608_185013
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 5.71 秒
- **驗證集指標**:
  - MAE: 0.0869
  - RMSE: 0.1556
  - MAPE: 18654128.36%
  - R²: 0.9409

### LSTM 結果

- **訓練時間**: 9.69 秒
- **最終輪數**: 13
- **驗證集指標**:
  - MAE: 0.2885
  - RMSE: 0.4676
  - MAPE: 441527900.00%
  - R²: 0.5907

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.2016)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate_norm\separate_norm_花蓮_20250608_185013_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate_norm\separate_norm_花蓮_20250608_185013_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_norm_花蓮_20250608_185013_evaluation.json
