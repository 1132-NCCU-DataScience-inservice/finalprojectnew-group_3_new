
# separate_norm 模式模型訓練報告

## 基本信息
- **模式**: separate_norm
- **測站**: 馬公
- **時間戳**: 20250608_185500
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 4.89 秒
- **驗證集指標**:
  - MAE: 0.0718
  - RMSE: 0.1433
  - MAPE: 13853689.86%
  - R²: 0.9647

### LSTM 結果

- **訓練時間**: 9.66 秒
- **最終輪數**: 13
- **驗證集指標**:
  - MAE: 0.2616
  - RMSE: 0.4200
  - MAPE: 415419875.00%
  - R²: 0.5989

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.1898)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate_norm\separate_norm_馬公_20250608_185500_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate_norm\separate_norm_馬公_20250608_185500_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_norm_馬公_20250608_185500_evaluation.json
