
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 嘉義
- **時間戳**: 20250608_155544
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 10.41 秒
- **驗證集指標**:
  - MAE: 3.0546
  - RMSE: 4.6708
  - MAPE: 5.10%
  - R²: 0.9730

### LSTM 結果

- **訓練時間**: 16.00 秒
- **最終輪數**: 20
- **驗證集指標**:
  - MAE: 3.3815
  - RMSE: 6.9837
  - MAPE: 305750300.00%
  - R²: 0.8973

## 總結

- **較佳模型**: LightGBM (MAE差異: 0.3269)
- **建議使用**: LightGBM 模型用於此配置


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_嘉義_20250608_155544_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_嘉義_20250608_155544_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_嘉義_20250608_155544_evaluation.json
