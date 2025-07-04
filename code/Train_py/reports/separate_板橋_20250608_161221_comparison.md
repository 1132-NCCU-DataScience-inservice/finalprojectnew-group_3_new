
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 板橋
- **時間戳**: 20250608_161221
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 8.47 秒
- **驗證集指標**:
  - MAE: 2.9675
  - RMSE: 4.4308
  - MAPE: 6.72%
  - R²: 0.9519

### LSTM 結果

- **訓練時間**: 15.49 秒
- **最終輪數**: 19
- **驗證集指標**:
  - MAE: 3.1354
  - RMSE: 6.2763
  - MAPE: 637957400.00%
  - R²: 0.8618

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.1679)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_板橋_20250608_161221_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_板橋_20250608_161221_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_板橋_20250608_161221_evaluation.json
