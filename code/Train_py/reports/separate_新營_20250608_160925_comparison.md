
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 新營
- **時間戳**: 20250608_160925
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 14.07 秒
- **驗證集指標**:
  - MAE: 2.9292
  - RMSE: 4.2164
  - MAPE: 5.47%
  - R²: 0.9766

### LSTM 結果

- **訓練時間**: 14.82 秒
- **最終輪數**: 18
- **驗證集指標**:
  - MAE: 3.4996
  - RMSE: 6.9482
  - MAPE: 453877700.00%
  - R²: 0.8976

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.5703)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_新營_20250608_160925_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_新營_20250608_160925_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_新營_20250608_160925_evaluation.json
