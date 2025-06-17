
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 屏東
- **時間戳**: 20250608_160259
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 13.37 秒
- **驗證集指標**:
  - MAE: 3.0326
  - RMSE: 4.5785
  - MAPE: 5.26%
  - R²: 0.9766

### LSTM 結果

- **訓練時間**: 19.17 秒
- **最終輪數**: 24
- **驗證集指標**:
  - MAE: 3.1427
  - RMSE: 6.7463
  - MAPE: 365789725.00%
  - R²: 0.9072

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.1100)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_屏東_20250608_160259_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_屏東_20250608_160259_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_屏東_20250608_160259_evaluation.json
