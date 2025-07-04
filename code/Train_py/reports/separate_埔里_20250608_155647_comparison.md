
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 埔里
- **時間戳**: 20250608_155647
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 8.85 秒
- **驗證集指標**:
  - MAE: 2.3718
  - RMSE: 3.3315
  - MAPE: 4.66%
  - R²: 0.9768

### LSTM 結果

- **訓練時間**: 15.97 秒
- **最終輪數**: 20
- **驗證集指標**:
  - MAE: 2.3613
  - RMSE: 4.9538
  - MAPE: 234625075.00%
  - R²: 0.9248

## 總結

- **較佳模型**: LSTM (MAE差異: 0.0105)
- **建議使用**: LSTM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_埔里_20250608_155647_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_埔里_20250608_155647_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_埔里_20250608_155647_evaluation.json
