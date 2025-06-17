
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 桃園
- **時間戳**: 20250608_154641
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 6.18 秒
- **驗證集指標**:
  - MAE: 2.7769
  - RMSE: 4.0766
  - MAPE: 5.82%
  - R²: 0.9673

### LSTM 結果

- **訓練時間**: 15.66 秒
- **最終輪數**: 17
- **驗證集指標**:
  - MAE: 3.1298
  - RMSE: 6.2326
  - MAPE: 684641800.00%
  - R²: 0.8749

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.3528)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_桃園_20250608_154641_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_桃園_20250608_154641_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_桃園_20250608_154641_evaluation.json
