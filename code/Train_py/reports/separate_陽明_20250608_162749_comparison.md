
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 陽明
- **時間戳**: 20250608_162749
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 4.82 秒
- **驗證集指標**:
  - MAE: 1.7452
  - RMSE: 3.3763
  - MAPE: 4.47%
  - R²: 0.9595

### LSTM 結果

- **訓練時間**: 11.11 秒
- **最終輪數**: 15
- **驗證集指標**:
  - MAE: 2.1328
  - RMSE: 4.6998
  - MAPE: 950248300.00%
  - R²: 0.9271

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.3876)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_陽明_20250608_162749_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_陽明_20250608_162749_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_陽明_20250608_162749_evaluation.json
