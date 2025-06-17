
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 金門
- **時間戳**: 20250608_162714
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 7.36 秒
- **驗證集指標**:
  - MAE: 3.5048
  - RMSE: 5.8285
  - MAPE: 5.87%
  - R²: 0.9733

### LSTM 結果

- **訓練時間**: 19.41 秒
- **最終輪數**: 27
- **驗證集指標**:
  - MAE: 3.5284
  - RMSE: 7.6587
  - MAPE: 522335800.00%
  - R²: 0.8902

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.0236)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_金門_20250608_162714_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_金門_20250608_162714_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_金門_20250608_162714_evaluation.json
