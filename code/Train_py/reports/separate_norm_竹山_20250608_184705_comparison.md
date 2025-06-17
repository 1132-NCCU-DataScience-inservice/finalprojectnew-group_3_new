
# separate_norm 模式模型訓練報告

## 基本信息
- **模式**: separate_norm
- **測站**: 竹山
- **時間戳**: 20250608_184705
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 11.56 秒
- **驗證集指標**:
  - MAE: 0.0538
  - RMSE: 0.0747
  - MAPE: 6290502.22%
  - R²: 0.9765

### LSTM 結果

- **訓練時間**: 10.36 秒
- **最終輪數**: 14
- **驗證集指標**:
  - MAE: 0.2451
  - RMSE: 0.3964
  - MAPE: 397628500.00%
  - R²: 0.5932

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.1913)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate_norm\separate_norm_竹山_20250608_184705_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate_norm\separate_norm_竹山_20250608_184705_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_norm_竹山_20250608_184705_evaluation.json
