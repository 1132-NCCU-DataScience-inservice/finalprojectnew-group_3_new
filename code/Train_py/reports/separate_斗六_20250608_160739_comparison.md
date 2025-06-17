
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 斗六
- **時間戳**: 20250608_160739
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 13.04 秒
- **驗證集指標**:
  - MAE: 3.0896
  - RMSE: 4.7164
  - MAPE: 5.04%
  - R²: 0.9727

### LSTM 結果

- **訓練時間**: 14.37 秒
- **最終輪數**: 18
- **驗證集指標**:
  - MAE: 3.5527
  - RMSE: 7.1393
  - MAPE: 260944125.00%
  - R²: 0.9023

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.4631)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_斗六_20250608_160739_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_斗六_20250608_160739_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_斗六_20250608_160739_evaluation.json
