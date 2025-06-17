
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 基隆
- **時間戳**: 20250608_155721
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 6.67 秒
- **驗證集指標**:
  - MAE: 2.6249
  - RMSE: 4.2517
  - MAPE: 6.56%
  - R²: 0.9474

### LSTM 結果

- **訓練時間**: 12.83 秒
- **最終輪數**: 16
- **驗證集指標**:
  - MAE: 2.9884
  - RMSE: 6.0050
  - MAPE: 527611400.00%
  - R²: 0.8668

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.3635)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_基隆_20250608_155721_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_基隆_20250608_155721_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_基隆_20250608_155721_evaluation.json
