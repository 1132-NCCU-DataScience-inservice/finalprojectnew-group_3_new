
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 新港
- **時間戳**: 20250608_160846
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 10.03 秒
- **驗證集指標**:
  - MAE: 3.2795
  - RMSE: 5.1276
  - MAPE: 5.32%
  - R²: 0.9653

### LSTM 結果

- **訓練時間**: 19.61 秒
- **最終輪數**: 25
- **驗證集指標**:
  - MAE: 3.2814
  - RMSE: 7.1946
  - MAPE: 205823950.00%
  - R²: 0.8998

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.0018)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_新港_20250608_160846_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_新港_20250608_160846_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_新港_20250608_160846_evaluation.json
