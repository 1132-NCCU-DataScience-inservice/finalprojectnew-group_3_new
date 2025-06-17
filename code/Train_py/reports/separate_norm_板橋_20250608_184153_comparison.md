
# separate_norm 模式模型訓練報告

## 基本信息
- **模式**: separate_norm
- **測站**: 板橋
- **時間戳**: 20250608_184153
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 7.60 秒
- **驗證集指標**:
  - MAE: 0.1242
  - RMSE: 0.1892
  - MAPE: 33992872.56%
  - R²: 0.9364

### LSTM 結果

- **訓練時間**: 9.69 秒
- **最終輪數**: 13
- **驗證集指標**:
  - MAE: 0.2648
  - RMSE: 0.4345
  - MAPE: 185259962.50%
  - R²: 0.6115

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.1406)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate_norm\separate_norm_板橋_20250608_184153_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate_norm\separate_norm_板橋_20250608_184153_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_norm_板橋_20250608_184153_evaluation.json
