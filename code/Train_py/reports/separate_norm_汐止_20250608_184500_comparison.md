
# separate_norm 模式模型訓練報告

## 基本信息
- **模式**: separate_norm
- **測站**: 汐止
- **時間戳**: 20250608_184500
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 8.46 秒
- **驗證集指標**:
  - MAE: 0.1118
  - RMSE: 0.1747
  - MAPE: 30879085.27%
  - R²: 0.9373

### LSTM 結果

- **訓練時間**: 10.27 秒
- **最終輪數**: 14
- **驗證集指標**:
  - MAE: 0.2840
  - RMSE: 0.4557
  - MAPE: 273643050.00%
  - R²: 0.5747

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.1722)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate_norm\separate_norm_汐止_20250608_184500_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate_norm\separate_norm_汐止_20250608_184500_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_norm_汐止_20250608_184500_evaluation.json
