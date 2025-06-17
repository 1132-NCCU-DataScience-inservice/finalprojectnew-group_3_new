
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 永和
- **時間戳**: 20250608_161541
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 9.56 秒
- **驗證集指標**:
  - MAE: 2.7577
  - RMSE: 3.9871
  - MAPE: 6.18%
  - R²: 0.9527

### LSTM 結果

- **訓練時間**: 17.30 秒
- **最終輪數**: 22
- **驗證集指標**:
  - MAE: 3.3634
  - RMSE: 6.5162
  - MAPE: 209735775.00%
  - R²: 0.8493

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.6058)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_永和_20250608_161541_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_永和_20250608_161541_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_永和_20250608_161541_evaluation.json
