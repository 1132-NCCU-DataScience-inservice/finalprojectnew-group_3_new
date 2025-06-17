
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 前金
- **時間戳**: 20250608_155244
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 13.45 秒
- **驗證集指標**:
  - MAE: 3.2716
  - RMSE: 4.9972
  - MAPE: 6.10%
  - R²: 0.9724

### LSTM 結果

- **訓練時間**: 16.55 秒
- **最終輪數**: 21
- **驗證集指標**:
  - MAE: 3.6574
  - RMSE: 7.4265
  - MAPE: 613109700.00%
  - R²: 0.8876

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.3858)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_前金_20250608_155244_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_前金_20250608_155244_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_前金_20250608_155244_evaluation.json
