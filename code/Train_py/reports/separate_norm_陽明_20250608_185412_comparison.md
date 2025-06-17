
# separate_norm 模式模型訓練報告

## 基本信息
- **模式**: separate_norm
- **測站**: 陽明
- **時間戳**: 20250608_185412
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 4.09 秒
- **驗證集指標**:
  - MAE: 0.0919
  - RMSE: 0.1893
  - MAPE: 11720663.08%
  - R²: 0.9617

### LSTM 結果

- **訓練時間**: 9.09 秒
- **最終輪數**: 12
- **驗證集指標**:
  - MAE: 0.3347
  - RMSE: 0.5347
  - MAPE: 500005600.00%
  - R²: 0.6051

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.2429)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate_norm\separate_norm_陽明_20250608_185412_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate_norm\separate_norm_陽明_20250608_185412_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_norm_陽明_20250608_185412_evaluation.json
