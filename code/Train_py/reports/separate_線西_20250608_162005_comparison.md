
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 線西
- **時間戳**: 20250608_162005
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 12.01 秒
- **驗證集指標**:
  - MAE: 2.8948
  - RMSE: 4.2084
  - MAPE: 51304472.69%
  - R²: 0.9653

### LSTM 結果

- **訓練時間**: 20.15 秒
- **最終輪數**: 25
- **驗證集指標**:
  - MAE: 3.4023
  - RMSE: 6.8798
  - MAPE: 487242800.00%
  - R²: 0.8740

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.5075)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_線西_20250608_162005_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_線西_20250608_162005_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_線西_20250608_162005_evaluation.json
