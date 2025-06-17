
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 萬華
- **時間戳**: 20250608_162444
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 10.85 秒
- **驗證集指標**:
  - MAE: 2.9529
  - RMSE: 4.2043
  - MAPE: 6.21%
  - R²: 0.9590

### LSTM 結果

- **訓練時間**: 14.31 秒
- **最終輪數**: 18
- **驗證集指標**:
  - MAE: 3.3715
  - RMSE: 6.5456
  - MAPE: 432730450.00%
  - R²: 0.8648

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.4185)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_萬華_20250608_162444_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_萬華_20250608_162444_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_萬華_20250608_162444_evaluation.json
