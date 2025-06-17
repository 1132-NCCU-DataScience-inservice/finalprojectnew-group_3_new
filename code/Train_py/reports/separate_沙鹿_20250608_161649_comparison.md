
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 沙鹿
- **時間戳**: 20250608_161649
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 11.03 秒
- **驗證集指標**:
  - MAE: 2.6795
  - RMSE: 4.0433
  - MAPE: 5.11%
  - R²: 0.9656

### LSTM 結果

- **訓練時間**: 15.36 秒
- **最終輪數**: 19
- **驗證集指標**:
  - MAE: 3.1584
  - RMSE: 6.4322
  - MAPE: 352050250.00%
  - R²: 0.8882

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.4789)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_沙鹿_20250608_161649_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_沙鹿_20250608_161649_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_沙鹿_20250608_161649_evaluation.json
