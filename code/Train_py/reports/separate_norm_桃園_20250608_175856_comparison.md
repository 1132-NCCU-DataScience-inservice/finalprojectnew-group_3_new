
# separate_norm 模式模型訓練報告

## 基本信息
- **模式**: separate_norm
- **測站**: 桃園
- **時間戳**: 20250608_175856
- **設備**: cpu

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **訓練時間**: 9.04 秒
- **驗證集指標**:
  - MAE: 0.1042
  - RMSE: 0.1569
  - MAPE: 14342028.73%
  - R²: 0.9610

### LSTM 結果

- **錯誤**: ReduceLROnPlateau.__init__() got an unexpected keyword argument 'verbose'


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate_norm\separate_norm_桃園_20250608_175856_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate_norm\separate_norm_桃園_20250608_175856_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\reports\separate_norm_桃園_20250608_175856_evaluation.json
