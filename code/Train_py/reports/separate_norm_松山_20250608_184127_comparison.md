
# separate_norm 模式模型訓練報告

## 基本信息
- **模式**: separate_norm
- **測站**: 松山
- **時間戳**: 20250608_184127
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 8.37 秒
- **驗證集指標**:
  - MAE: 0.0965
  - RMSE: 0.1430
  - MAPE: 19617411.10%
  - R²: 0.9540

### LSTM 結果

- **訓練時間**: 9.64 秒
- **最終輪數**: 13
- **驗證集指標**:
  - MAE: 0.2595
  - RMSE: 0.4281
  - MAPE: 245069150.00%
  - R²: 0.5357

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.1630)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate_norm\separate_norm_松山_20250608_184127_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate_norm\separate_norm_松山_20250608_184127_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_norm_松山_20250608_184127_evaluation.json
