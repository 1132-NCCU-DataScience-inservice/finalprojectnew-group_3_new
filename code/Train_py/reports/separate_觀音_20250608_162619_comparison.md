
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 觀音
- **時間戳**: 20250608_162619
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 6.30 秒
- **驗證集指標**:
  - MAE: 2.9217
  - RMSE: 5.0204
  - MAPE: 6.85%
  - R²: 0.9496

### LSTM 結果

- **訓練時間**: 11.98 秒
- **最終輪數**: 16
- **驗證集指標**:
  - MAE: 3.2273
  - RMSE: 6.6821
  - MAPE: 819707300.00%
  - R²: 0.8730

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.3056)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_觀音_20250608_162619_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_觀音_20250608_162619_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_觀音_20250608_162619_evaluation.json
