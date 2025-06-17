
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 美濃
- **時間戳**: 20250608_162046
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 12.85 秒
- **驗證集指標**:
  - MAE: 2.7783
  - RMSE: 4.3185
  - MAPE: 5.69%
  - R²: 0.9712

### LSTM 結果

- **訓練時間**: 15.91 秒
- **最終輪數**: 20
- **驗證集指標**:
  - MAE: 2.7818
  - RMSE: 5.8539
  - MAPE: 628708450.00%
  - R²: 0.9152

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.0035)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_美濃_20250608_162046_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_美濃_20250608_162046_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_美濃_20250608_162046_evaluation.json
