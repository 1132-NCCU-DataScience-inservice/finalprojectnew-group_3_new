
# separate_norm 模式模型訓練報告

## 基本信息
- **模式**: separate_norm
- **測站**: 仁武
- **時間戳**: 20250608_182624
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 10.91 秒
- **驗證集指標**:
  - MAE: 0.0594
  - RMSE: 0.0896
  - MAPE: 5979232.23%
  - R²: 0.9752

### LSTM 結果

- **訓練時間**: 8.99 秒
- **最終輪數**: 12
- **驗證集指標**:
  - MAE: 0.2503
  - RMSE: 0.4230
  - MAPE: 432728500.00%
  - R²: 0.5787

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.1909)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate_norm\separate_norm_仁武_20250608_182624_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate_norm\separate_norm_仁武_20250608_182624_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_norm_仁武_20250608_182624_evaluation.json
