
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 復興
- **時間戳**: 20250608_160600
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 10.14 秒
- **驗證集指標**:
  - MAE: 3.4306
  - RMSE: 5.1167
  - MAPE: 6.15%
  - R²: 0.9724

### LSTM 結果

- **訓練時間**: 18.92 秒
- **最終輪數**: 23
- **驗證集指標**:
  - MAE: 3.4594
  - RMSE: 7.0867
  - MAPE: 350483650.00%
  - R²: 0.8930

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.0287)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_復興_20250608_160600_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_復興_20250608_160600_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_復興_20250608_160600_evaluation.json
