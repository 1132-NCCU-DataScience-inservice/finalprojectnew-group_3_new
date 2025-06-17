
# separate_norm 模式模型訓練報告

## 基本信息
- **模式**: separate_norm
- **測站**: 臺東
- **時間戳**: 20250608_184921
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 4.65 秒
- **驗證集指標**:
  - MAE: 0.0763
  - RMSE: 0.1415
  - MAPE: 16646709.91%
  - R²: 0.9489

### LSTM 結果

- **訓練時間**: 9.74 秒
- **最終輪數**: 13
- **驗證集指標**:
  - MAE: 0.2400
  - RMSE: 0.3840
  - MAPE: 299925400.00%
  - R²: 0.6688

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.1637)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate_norm\separate_norm_臺東_20250608_184921_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate_norm\separate_norm_臺東_20250608_184921_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_norm_臺東_20250608_184921_evaluation.json
