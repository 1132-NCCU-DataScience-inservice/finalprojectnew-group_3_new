
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 菜寮
- **時間戳**: 20250608_162414
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 8.27 秒
- **驗證集指標**:
  - MAE: 2.7801
  - RMSE: 4.1465
  - MAPE: 5.87%
  - R²: 0.9578

### LSTM 結果

- **訓練時間**: 13.89 秒
- **最終輪數**: 17
- **驗證集指標**:
  - MAE: 3.0703
  - RMSE: 6.1256
  - MAPE: 558172550.00%
  - R²: 0.8744

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.2903)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_菜寮_20250608_162414_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_菜寮_20250608_162414_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_菜寮_20250608_162414_evaluation.json
