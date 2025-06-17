
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 崙背
- **時間戳**: 20250608_160340
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 10.70 秒
- **驗證集指標**:
  - MAE: 3.3315
  - RMSE: 5.7484
  - MAPE: 5.73%
  - R²: 0.9581

### LSTM 結果

- **訓練時間**: 15.88 秒
- **最終輪數**: 20
- **驗證集指標**:
  - MAE: 3.6856
  - RMSE: 7.5688
  - MAPE: 460389000.00%
  - R²: 0.8916

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.3541)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_崙背_20250608_160340_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_崙背_20250608_160340_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_崙背_20250608_160340_evaluation.json
