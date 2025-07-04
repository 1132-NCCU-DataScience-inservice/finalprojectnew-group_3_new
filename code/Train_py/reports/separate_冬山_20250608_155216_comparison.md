
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 冬山
- **時間戳**: 20250608_155216
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 6.15 秒
- **驗證集指標**:
  - MAE: 2.0414
  - RMSE: 3.1248
  - MAPE: 5.24%
  - R²: 0.9567

### LSTM 結果

- **訓練時間**: 13.38 秒
- **最終輪數**: 17
- **驗證集指標**:
  - MAE: 2.3868
  - RMSE: 4.8436
  - MAPE: 505496100.00%
  - R²: 0.8940

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.3454)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_冬山_20250608_155216_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_冬山_20250608_155216_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_冬山_20250608_155216_evaluation.json
