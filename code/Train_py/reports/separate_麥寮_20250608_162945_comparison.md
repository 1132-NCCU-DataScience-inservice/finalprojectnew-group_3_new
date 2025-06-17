
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 麥寮
- **時間戳**: 20250608_162945
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 6.40 秒
- **驗證集指標**:
  - MAE: 3.3195
  - RMSE: 5.1250
  - MAPE: 5.73%
  - R²: 0.9628

### LSTM 結果

- **訓練時間**: 17.65 秒
- **最終輪數**: 24
- **驗證集指標**:
  - MAE: 3.2781
  - RMSE: 6.8697
  - MAPE: 376471950.00%
  - R²: 0.8979

## 總結

- **較佳模型**: LSTM (MAE差異: 0.0414)
- **建議使用**: LSTM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_麥寮_20250608_162945_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_麥寮_20250608_162945_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_麥寮_20250608_162945_evaluation.json
