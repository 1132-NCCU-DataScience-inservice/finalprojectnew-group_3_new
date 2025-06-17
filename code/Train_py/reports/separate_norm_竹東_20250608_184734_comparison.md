
# separate_norm 模式模型訓練報告

## 基本信息
- **模式**: separate_norm
- **測站**: 竹東
- **時間戳**: 20250608_184734
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 8.39 秒
- **驗證集指標**:
  - MAE: 0.0881
  - RMSE: 0.1378
  - MAPE: 12826774.92%
  - R²: 0.9648

### LSTM 結果

- **訓練時間**: 9.11 秒
- **最終輪數**: 12
- **驗證集指標**:
  - MAE: 0.2809
  - RMSE: 0.4522
  - MAPE: 464575800.00%
  - R²: 0.5353

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.1928)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate_norm\separate_norm_竹東_20250608_184734_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate_norm\separate_norm_竹東_20250608_184734_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_norm_竹東_20250608_184734_evaluation.json
