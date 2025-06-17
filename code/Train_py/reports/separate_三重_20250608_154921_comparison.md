
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 三重
- **時間戳**: 20250608_154921
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 5.85 秒
- **驗證集指標**:
  - MAE: 3.4593
  - RMSE: 4.6699
  - MAPE: 6.69%
  - R²: 0.9405

### LSTM 結果

- **訓練時間**: 19.49 秒
- **最終輪數**: 26
- **驗證集指標**:
  - MAE: 4.3090
  - RMSE: 9.1743
  - MAPE: 424985700.00%
  - R²: 0.8432

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.8497)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_三重_20250608_154921_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_三重_20250608_154921_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_三重_20250608_154921_evaluation.json
