
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 平鎮
- **時間戳**: 20250608_160453
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 7.36 秒
- **驗證集指標**:
  - MAE: 2.7290
  - RMSE: 4.0183
  - MAPE: 5.87%
  - R²: 0.9657

### LSTM 結果

- **訓練時間**: 12.87 秒
- **最終輪數**: 16
- **驗證集指標**:
  - MAE: 3.3016
  - RMSE: 6.5180
  - MAPE: 689272500.00%
  - R²: 0.8605

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.5726)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_平鎮_20250608_160453_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_平鎮_20250608_160453_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_平鎮_20250608_160453_evaluation.json
