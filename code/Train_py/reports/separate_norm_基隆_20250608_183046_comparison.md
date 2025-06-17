
# separate_norm 模式模型訓練報告

## 基本信息
- **模式**: separate_norm
- **測站**: 基隆
- **時間戳**: 20250608_183046
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 4.96 秒
- **驗證集指標**:
  - MAE: 0.1310
  - RMSE: 0.2186
  - MAPE: 18602339.74%
  - R²: 0.9376

### LSTM 結果

- **訓練時間**: 10.35 秒
- **最終輪數**: 14
- **驗證集指標**:
  - MAE: 0.3218
  - RMSE: 0.5376
  - MAPE: 428308400.00%
  - R²: 0.5514

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.1908)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate_norm\separate_norm_基隆_20250608_183046_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate_norm\separate_norm_基隆_20250608_183046_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_norm_基隆_20250608_183046_evaluation.json
