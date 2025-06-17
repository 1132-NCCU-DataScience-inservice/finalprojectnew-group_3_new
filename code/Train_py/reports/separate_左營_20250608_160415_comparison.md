
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 左營
- **時間戳**: 20250608_160415
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 10.55 秒
- **驗證集指標**:
  - MAE: 3.2293
  - RMSE: 4.9741
  - MAPE: 4.90%
  - R²: 0.9729

### LSTM 結果

- **訓練時間**: 18.70 秒
- **最終輪數**: 24
- **驗證集指標**:
  - MAE: 3.2821
  - RMSE: 6.7562
  - MAPE: 307466125.00%
  - R²: 0.9151

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.0528)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_左營_20250608_160415_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_左營_20250608_160415_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_左營_20250608_160415_evaluation.json
