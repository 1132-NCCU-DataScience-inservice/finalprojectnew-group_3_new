
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 馬公
- **時間戳**: 20250608_162843
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 4.71 秒
- **驗證集指標**:
  - MAE: 1.9367
  - RMSE: 3.2858
  - MAPE: 4.49%
  - R²: 0.9763

### LSTM 結果

- **訓練時間**: 15.17 秒
- **最終輪數**: 21
- **驗證集指標**:
  - MAE: 2.1235
  - RMSE: 4.4924
  - MAPE: 543908850.00%
  - R²: 0.9422

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.1868)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_馬公_20250608_162843_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_馬公_20250608_162843_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_馬公_20250608_162843_evaluation.json
