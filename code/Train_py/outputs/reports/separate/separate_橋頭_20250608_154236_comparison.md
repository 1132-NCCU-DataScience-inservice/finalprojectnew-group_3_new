
# separate 模式模型訓練報告

## 基本信息
- **模式**: separate
- **測站**: 橋頭
- **時間戳**: 20250608_154236
- **設備**: cuda

## 配置參數
- **時間窗口**: 24 小時
- **預測範圍**: 6 小時
- **訓練比例**: 80.0%

## 模型比較

### LightGBM 結果

- **錯誤**: 'ConfigManager' object has no attribute 'lgbm_config'

### LSTM 結果

- **錯誤**: 'ConfigManager' object has no attribute 'lstm_config'


## 輸出檔案
- **LightGBM模型**: D:\pythonWork\R_datascience\final\Train\models\lightgbm\separate\separate_橋頭_20250608_154236_lgbm.pkl
- **LSTM模型**: D:\pythonWork\R_datascience\final\Train\models\lstm\separate\separate_橋頭_20250608_154236_lstm.pt
- **評估報告**: D:\pythonWork\R_datascience\final\Train\outputs\reports\separate\separate_橋頭_20250608_154236_evaluation.json
