
# separate_norm 模式模型訓練報告

## 基本信息
- **模式**: separate_norm
- **測站**: 永和
- **時間戳**: 20250608_184432
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 9.25 秒
- **驗證集指標**:
  - MAE: 0.1215
  - RMSE: 0.1851
  - MAPE: 15779234.72%
  - R²: 0.9362

### LSTM 結果

- **訓練時間**: 10.37 秒
- **最終輪數**: 14
- **驗證集指標**:
  - MAE: 0.2721
  - RMSE: 0.4206
  - MAPE: 250892175.00%
  - R²: 0.5922

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.1506)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate_norm\separate_norm_永和_20250608_184432_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate_norm\separate_norm_永和_20250608_184432_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_norm_永和_20250608_184432_evaluation.json
