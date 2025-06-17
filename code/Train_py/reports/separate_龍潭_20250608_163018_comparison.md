
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 龍潭
- **時間戳**: 20250608_163018
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 8.43 秒
- **驗證集指標**:
  - MAE: 2.8385
  - RMSE: 4.5498
  - MAPE: 5.97%
  - R²: 0.9558

### LSTM 結果

- **訓練時間**: 14.28 秒
- **最終輪數**: 19
- **驗證集指標**:
  - MAE: 2.9959
  - RMSE: 6.1705
  - MAPE: 435960650.00%
  - R²: 0.8734

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.1573)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_龍潭_20250608_163018_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_龍潭_20250608_163018_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_龍潭_20250608_163018_evaluation.json
