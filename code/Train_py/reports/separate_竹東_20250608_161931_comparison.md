
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 竹東
- **時間戳**: 20250608_161931
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 10.88 秒
- **驗證集指標**:
  - MAE: 2.5148
  - RMSE: 3.8074
  - MAPE: 5.21%
  - R²: 0.9674

### LSTM 結果

- **訓練時間**: 14.24 秒
- **最終輪數**: 18
- **驗證集指標**:
  - MAE: 2.8361
  - RMSE: 5.9352
  - MAPE: 526530750.00%
  - R²: 0.8770

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.3213)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_竹東_20250608_161931_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_竹東_20250608_161931_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_竹東_20250608_161931_evaluation.json
