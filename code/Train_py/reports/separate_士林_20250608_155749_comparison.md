
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 士林
- **時間戳**: 20250608_155749
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 7.59 秒
- **驗證集指標**:
  - MAE: 2.7562
  - RMSE: 4.1831
  - MAPE: 5.92%
  - R²: 0.9462

### LSTM 結果

- **訓練時間**: 13.63 秒
- **最終輪數**: 17
- **驗證集指標**:
  - MAE: 3.0208
  - RMSE: 6.1175
  - MAPE: 590308300.00%
  - R²: 0.8668

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.2646)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_士林_20250608_155749_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_士林_20250608_155749_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_士林_20250608_155749_evaluation.json
