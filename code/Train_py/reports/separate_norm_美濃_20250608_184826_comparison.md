
# separate_norm 模式模型訓練報告

## 基本信息
- **模式**: separate_norm
- **測站**: 美濃
- **時間戳**: 20250608_184826
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 8.19 秒
- **驗證集指標**:
  - MAE: 0.0668
  - RMSE: 0.1011
  - MAPE: 8132898.67%
  - R²: 0.9710

### LSTM 結果

- **訓練時間**: 11.13 秒
- **最終輪數**: 15
- **驗證集指標**:
  - MAE: 0.2202
  - RMSE: 0.3382
  - MAPE: 344086525.00%
  - R²: 0.6766

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.1534)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate_norm\separate_norm_美濃_20250608_184826_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate_norm\separate_norm_美濃_20250608_184826_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_norm_美濃_20250608_184826_evaluation.json
