
# separate_norm 模式模型訓練報告

## 基本信息
- **模式**: separate_norm
- **測站**: 新營
- **時間戳**: 20250608_183944
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 10.38 秒
- **驗證集指標**:
  - MAE: 0.0675
  - RMSE: 0.0974
  - MAPE: 8707480.70%
  - R²: 0.9759

### LSTM 結果

- **訓練時間**: 9.01 秒
- **最終輪數**: 12
- **驗證集指標**:
  - MAE: 0.2946
  - RMSE: 0.4474
  - MAPE: 506324150.00%
  - R²: 0.5931

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.2271)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate_norm\separate_norm_新營_20250608_183944_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate_norm\separate_norm_新營_20250608_183944_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_norm_新營_20250608_183944_evaluation.json
