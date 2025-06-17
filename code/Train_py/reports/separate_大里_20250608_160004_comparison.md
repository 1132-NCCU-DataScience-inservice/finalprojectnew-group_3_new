
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 大里
- **時間戳**: 20250608_160004
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 11.52 秒
- **驗證集指標**:
  - MAE: 2.8943
  - RMSE: 4.1696
  - MAPE: 5.37%
  - R²: 0.9679

### LSTM 結果

- **訓練時間**: 14.77 秒
- **最終輪數**: 18
- **驗證集指標**:
  - MAE: 2.9048
  - RMSE: 6.0067
  - MAPE: 487773300.00%
  - R²: 0.8912

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.0105)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_大里_20250608_160004_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_大里_20250608_160004_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_大里_20250608_160004_evaluation.json
