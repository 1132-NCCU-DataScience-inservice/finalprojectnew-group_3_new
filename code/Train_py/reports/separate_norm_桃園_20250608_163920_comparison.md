
# separate_norm 模式模型訓練報告

## 基本信息
- **模式**: separate_norm
- **測站**: 桃園
- **時間戳**: 20250608_163920
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 10.47 秒
- **驗證集指標**:
  - MAE: 0.1034
  - RMSE: 0.1567
  - MAPE: 14432295.09%
  - R²: 0.9611

### LSTM 結果

- **訓練時間**: 13.29 秒
- **最終輪數**: 16
- **驗證集指標**:
  - MAE: 0.2869
  - RMSE: 0.4465
  - MAPE: 292228425.00%
  - R²: 0.6020

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.1835)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate_norm\separate_norm_桃園_20250608_163920_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate_norm\separate_norm_桃園_20250608_163920_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_norm_桃園_20250608_163920_evaluation.json
