
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 汐止
- **時間戳**: 20250608_161617
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 9.20 秒
- **驗證集指標**:
  - MAE: 2.6707
  - RMSE: 3.9445
  - MAPE: 5.86%
  - R²: 0.9555

### LSTM 結果

- **訓練時間**: 14.57 秒
- **最終輪數**: 18
- **驗證集指標**:
  - MAE: 3.1834
  - RMSE: 6.3182
  - MAPE: 666110600.00%
  - R²: 0.8539

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.5127)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_汐止_20250608_161617_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_汐止_20250608_161617_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_汐止_20250608_161617_evaluation.json
