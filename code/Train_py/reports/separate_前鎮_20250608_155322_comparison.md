
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 前鎮
- **時間戳**: 20250608_155322
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 8.92 秒
- **驗證集指標**:
  - MAE: 3.3105
  - RMSE: 4.9566
  - MAPE: 5.84%
  - R²: 0.9700

### LSTM 結果

- **訓練時間**: 18.96 秒
- **最終輪數**: 24
- **驗證集指標**:
  - MAE: 3.5625
  - RMSE: 7.2930
  - MAPE: 213379400.00%
  - R²: 0.8903

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.2520)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_前鎮_20250608_155322_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_前鎮_20250608_155322_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_前鎮_20250608_155322_evaluation.json
