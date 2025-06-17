
# separate_norm 模式模型訓練報告

## 基本信息
- **模式**: separate_norm
- **測站**: 金門
- **時間戳**: 20250608_185344
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 10.46 秒
- **驗證集指標**:
  - MAE: 0.0729
  - RMSE: 0.1289
  - MAPE: 14480901.51%
  - R²: 0.9690

### LSTM 結果

- **訓練時間**: 8.89 秒
- **最終輪數**: 12
- **驗證集指標**:
  - MAE: 0.2466
  - RMSE: 0.3974
  - MAPE: 344195275.00%
  - R²: 0.6656

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.1736)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate_norm\separate_norm_金門_20250608_185344_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate_norm\separate_norm_金門_20250608_185344_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_norm_金門_20250608_185344_evaluation.json
