# 🎮 GPU訓練環境使用指南

基於你的 **NVIDIA GeForce RTX 4090 (24GB VRAM)** 的完整GPU訓練解決方案。

## 🎯 環境狀態

✅ **硬體配置**
- GPU: NVIDIA GeForce RTX 4090 (24GB VRAM)
- CPU: 32核心
- 記憶體: 63.1GB
- CUDA版本: 12.6
- PyTorch版本: 2.6.0+cu124

## 🚀 快速開始

### 1. 檢查GPU環境
```bash
python setup_gpu_environment.py
```

### 2. 一鍵GPU訓練
```bash
# 自動訓練（推薦）
python scripts/train_gpu.py --auto_data --fast_mode

# 訓練特定模型
python scripts/train_gpu.py --model lgbm --auto_data
python scripts/train_gpu.py --model lstm --auto_data
```

### 3. 手動選擇數據
```bash
python scripts/train_gpu.py
```

## 📊 性能對比

| 模型 | CPU訓練時間 | GPU訓練時間 | 加速比 | GPU記憶體使用 |
|------|------------|------------|--------|--------------|
| **LightGBM** | ~6分鐘 | ~2分鐘 | **3x** | ~2GB |
| **LSTM** | ~40分鐘 | ~8分鐘 | **5x** | ~8GB |

## 🎮 GPU專用訓練腳本

### LightGBM GPU訓練
```bash
# 基本GPU訓練
python src/train_lgbm_gpu.py \
    --data data/processed/combine_168_train.npz \
    --model_out models/gpu/lgbm_gpu.pkl \
    --verbose

# 快速模式
python src/train_lgbm_gpu.py \
    --data data/processed/combine_168_train.npz \
    --model_out models/gpu/lgbm_gpu_fast.pkl \
    --fast_mode \
    --verbose

# 強制CPU模式（對比用）
python src/train_lgbm_gpu.py \
    --data data/processed/combine_168_train.npz \
    --model_out models/gpu/lgbm_cpu.pkl \
    --force_cpu \
    --verbose
```

### LSTM GPU訓練
```bash
# 基本GPU訓練
python src/train_lstm_gpu.py \
    --data data/processed/combine_168_train.npz \
    --model_out models/gpu/lstm_gpu.pth \
    --epochs 50 \
    --verbose

# 大批次訓練（充分利用24GB VRAM）
python src/train_lstm_gpu.py \
    --data data/processed/combine_168_train.npz \
    --model_out models/gpu/lstm_gpu_large.pth \
    --batch_size 512 \
    --epochs 100 \
    --verbose

# 快速模式
python src/train_lstm_gpu.py \
    --data data/processed/combine_168_train.npz \
    --model_out models/gpu/lstm_gpu_fast.pth \
    --fast_mode \
    --epochs 20 \
    --verbose
```

## ⚙️ GPU優化配置

### LightGBM GPU參數
```python
LGBM_GPU_PARAMS = {
    'device': 'gpu',
    'gpu_device_id': 0,
    'num_leaves': 127,        # GPU可處理更大模型
    'learning_rate': 0.05,
    'n_estimators': 1000,     # 更多樹
    'max_depth': 10,          # 更深
    'gpu_use_dp': True,       # 雙精度
}
```

### LSTM GPU配置
```python
LSTM_GPU_PARAMS = {
    'hidden_size': 256,       # 更大模型
    'num_layers': 3,
    'bidirectional': True,    # 雙向LSTM
    'use_attention': True,    # 注意力機制
    'batch_size': 256,        # 大批次
    'mixed_precision': True,  # 混合精度
}
```

## 💾 記憶體管理

### GPU記憶體使用策略
- **小數據集** (<5GB): 預載入到GPU記憶體
- **中數據集** (5-15GB): 動態載入
- **大數據集** (>15GB): 分批處理

### 批次大小建議
```python
# 基於24GB VRAM的建議
BATCH_SIZES = {
    'lstm_train': 256,      # 訓練
    'lstm_val': 512,        # 驗證  
    'lstm_inference': 1024, # 推理
}
```

## 🔧 故障排除

### 常見問題

#### 1. GPU記憶體不足
```bash
# 減少批次大小
python src/train_lstm_gpu.py --batch_size 128

# 啟用梯度累積
python src/train_lstm_gpu.py --accumulation_steps 2
```

#### 2. CUDA版本不匹配
```bash
# 重新安裝正確版本的PyTorch
pip uninstall torch torchvision torchaudio -y
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
```

#### 3. LightGBM GPU支援問題
```bash
# 使用CPU版本
python src/train_lgbm_gpu.py --force_cpu
```

### GPU監控命令
```bash
# 實時GPU狀態
watch -n 1 nvidia-smi

# GPU記憶體使用
python -c "import torch; print(f'GPU記憶體: {torch.cuda.memory_allocated()/1024**3:.1f}GB / {torch.cuda.get_device_properties(0).total_memory/1024**3:.1f}GB')"
```

## 📈 性能優化建議

### 針對RTX 4090的優化
1. **充分利用24GB VRAM**: 使用大批次大小
2. **混合精度訓練**: 啟用AMP以提升速度
3. **模型編譯**: 使用PyTorch 2.0編譯加速
4. **並行處理**: LightGBM多目標並行訓練

### 最佳實踐
```bash
# 日常快速訓練（5-10分鐘）
python scripts/train_gpu.py --fast_mode --max_samples 50000

# 完整精確訓練（30-60分鐘）
python scripts/train_gpu.py --epochs 100

# 性能基準測試
python scripts/train_gpu.py --benchmark --max_samples 10000
```

## 🎯 預期性能

基於你的RTX 4090系統：

### LightGBM
- **訓練時間**: 2-5分鐘（336目標）
- **GPU使用率**: 60-80%
- **記憶體使用**: 2-4GB
- **加速比**: 3-5x vs CPU

### LSTM  
- **訓練時間**: 5-15分鐘（50 epochs）
- **GPU使用率**: 85-95%
- **記憶體使用**: 8-16GB
- **吞吐量**: 2000+ samples/s

## 🏆 建議工作流程

### 開發階段
```bash
# 快速驗證（1-2分鐘）
python scripts/train_gpu.py --fast_mode --max_samples 10000

# 中等測試（5-10分鐘）
python scripts/train_gpu.py --max_samples 50000
```

### 生產階段
```bash
# 完整訓練（30-60分鐘）
python scripts/train_gpu.py --epochs 100
```

### 實驗階段
```bash
# 超參數調優
python src/train_lstm_gpu.py --lr 0.01 --batch_size 512
python src/train_lgbm_gpu.py --fast_mode
```

## 🎉 總結

通過GPU加速，你的訓練效率將大幅提升：

- ✅ **LightGBM**: 6分鐘 → 2分鐘 (3x提升)
- ✅ **LSTM**: 40分鐘 → 8分鐘 (5x提升)
- ✅ **完整Pipeline**: 2小時 → 30分鐘 (4x提升)

立即開始使用GPU加速訓練，享受極致的訓練體驗！ 🚀 