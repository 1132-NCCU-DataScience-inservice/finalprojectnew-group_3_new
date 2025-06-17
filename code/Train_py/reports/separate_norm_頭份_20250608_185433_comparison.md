
# separate_norm 模式模型訓練報告

## 基本信息
- **模式**: separate_norm
- **測站**: 頭份
- **時間戳**: 20250608_185433
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 9.44 秒
- **驗證集指標**:
  - MAE: 0.0738
  - RMSE: 0.1103
  - MAPE: 11922797.08%
  - R²: 0.9683

### LSTM 結果

- **訓練時間**: 9.67 秒
- **最終輪數**: 13
- **驗證集指標**:
  - MAE: 0.2912
  - RMSE: 0.4507
  - MAPE: 432033550.00%
  - R²: 0.5361

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.2174)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate_norm\separate_norm_頭份_20250608_185433_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate_norm\separate_norm_頭份_20250608_185433_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_norm_頭份_20250608_185433_evaluation.json
