
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 湖口
- **時間戳**: 20250608_161753
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 7.21 秒
- **驗證集指標**:
  - MAE: 2.7425
  - RMSE: 4.0493
  - MAPE: 5.26%
  - R²: 0.9666

### LSTM 結果

- **訓練時間**: 13.62 秒
- **最終輪數**: 17
- **驗證集指標**:
  - MAE: 3.4240
  - RMSE: 6.8506
  - MAPE: 683156100.00%
  - R²: 0.8681

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.6815)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_湖口_20250608_161753_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_湖口_20250608_161753_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_湖口_20250608_161753_evaluation.json
