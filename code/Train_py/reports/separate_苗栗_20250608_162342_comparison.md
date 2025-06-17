
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 苗栗
- **時間戳**: 20250608_162342
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 9.25 秒
- **驗證集指標**:
  - MAE: 2.7638
  - RMSE: 4.3676
  - MAPE: 5.64%
  - R²: 0.9548

### LSTM 結果

- **訓練時間**: 14.24 秒
- **最終輪數**: 18
- **驗證集指標**:
  - MAE: 3.0205
  - RMSE: 6.1824
  - MAPE: 320631350.00%
  - R²: 0.8765

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.2567)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_苗栗_20250608_162342_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_苗栗_20250608_162342_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_苗栗_20250608_162342_evaluation.json
