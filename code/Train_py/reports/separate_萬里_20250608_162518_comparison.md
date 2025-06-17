
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 萬里
- **時間戳**: 20250608_162518
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 6.82 秒
- **驗證集指標**:
  - MAE: 2.4840
  - RMSE: 4.0069
  - MAPE: 5.85%
  - R²: 0.9638

### LSTM 結果

- **訓練時間**: 15.66 秒
- **最終輪數**: 21
- **驗證集指標**:
  - MAE: 2.9746
  - RMSE: 6.6120
  - MAPE: 280714350.00%
  - R²: 0.8844

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.4905)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_萬里_20250608_162518_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_萬里_20250608_162518_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_萬里_20250608_162518_evaluation.json
