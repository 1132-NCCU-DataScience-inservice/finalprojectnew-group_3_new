
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 花蓮
- **時間戳**: 20250608_162310
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 5.92 秒
- **驗證集指標**:
  - MAE: 2.0246
  - RMSE: 3.1815
  - MAPE: 5.67%
  - R²: 0.9585

### LSTM 結果

- **訓練時間**: 17.45 秒
- **最終輪數**: 22
- **驗證集指標**:
  - MAE: 2.0967
  - RMSE: 4.2283
  - MAPE: 514919050.00%
  - R²: 0.9140

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.0720)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_花蓮_20250608_162310_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_花蓮_20250608_162310_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_花蓮_20250608_162310_evaluation.json
