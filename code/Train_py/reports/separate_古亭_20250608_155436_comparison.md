
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 古亭
- **時間戳**: 20250608_155436
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 7.60 秒
- **驗證集指標**:
  - MAE: 2.8477
  - RMSE: 4.1913
  - MAPE: 6.41%
  - R²: 0.9556

### LSTM 結果

- **訓練時間**: 14.29 秒
- **最終輪數**: 18
- **驗證集指標**:
  - MAE: 3.0884
  - RMSE: 6.2058
  - MAPE: 339061050.00%
  - R²: 0.8606

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.2407)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_古亭_20250608_155436_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_古亭_20250608_155436_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_古亭_20250608_155436_evaluation.json
