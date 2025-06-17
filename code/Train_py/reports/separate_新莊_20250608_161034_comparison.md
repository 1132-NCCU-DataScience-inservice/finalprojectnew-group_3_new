
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 新莊
- **時間戳**: 20250608_161034
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 7.17 秒
- **驗證集指標**:
  - MAE: 2.7210
  - RMSE: 3.9142
  - MAPE: 5.65%
  - R²: 0.9640

### LSTM 結果

- **訓練時間**: 14.42 秒
- **最終輪數**: 17
- **驗證集指標**:
  - MAE: 3.1850
  - RMSE: 6.4625
  - MAPE: 996435400.00%
  - R²: 0.8582

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.4639)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_新莊_20250608_161034_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_新莊_20250608_161034_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_新莊_20250608_161034_evaluation.json
