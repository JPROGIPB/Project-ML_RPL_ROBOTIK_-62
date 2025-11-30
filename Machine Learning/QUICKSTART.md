# 🚀 SEALEN - Quick Start Guide

Panduan cepat untuk memulai training model AI SEALEN.

## 📋 Prerequisites

- Python 3.9+
- CUDA-capable GPU (recommended)
- 50GB free disk space
- 16GB RAM minimum

## ⚡ Quick Setup (Windows PowerShell)

### 1. Setup Environment

```powershell
# Navigate to Machine Learning directory
cd "Machine Learning"

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Run setup script
python setup.py
```

### 2. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 3. Download Dataset

```powershell
# Download TACO dataset
cd datasets
git clone https://github.com/pedropro/TACO.git
cd TACO
python download.py
```

## 🎯 Training Models

### Model 1: Waste Detection (YOLOv8)

```powershell
python training/train_detector.py --epochs 100 --batch 16
```

**Expected Output:**
- Training time: ~3-4 hours
- Target mAP@0.5: >75%
- Model size: ~50MB

### Model 2: Waste Classification (ResNet50)

```powershell
python training/train_classifier.py --epochs 50 --batch 32
```

**Expected Output:**
- Training time: ~2-3 hours
- Target accuracy: >85%
- Model size: ~100MB

### Model 3: RL Agent (DQN)

```powershell
python training/train_rl_agent.py --timesteps 500000
```

**Expected Output:**
- Training time: ~2-4 hours
- Target success rate: >80%
- Model size: ~5MB

## 🔍 Running Inference

### Detect Waste in Image

```powershell
python inference/detect_waste.py `
  --model models/detection/waste_detector_v1_final.pt `
  --source test_image.jpg `
  --save
```

### Classify Waste Type

```powershell
python inference/classify_waste.py `
  --model models/classification/waste_classifier_v1_final.h5 `
  --image test_image.jpg
```

## 🌐 Start API Server

```powershell
cd api
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```

**Test API:**
- Open browser: `http://localhost:8000/docs`
- Interactive API documentation

## 📊 Monitor Training

### TensorBoard

```powershell
tensorboard --logdir=logs
```

Open: `http://localhost:6006`

### Weights & Biases (Optional)

```powershell
# Login
wandb login

# Training will automatically log to W&B
```

## 🧪 Testing

```powershell
# Run all tests
pytest tests/

# Run specific test
pytest tests/test_detector.py
```

## 📈 Evaluation

### Evaluate Detection Model

```powershell
python utils/evaluate_detector.py `
  --model models/detection/waste_detector_v1_final.pt `
  --data configs/taco.yaml
```

### Evaluate Classification Model

```powershell
python utils/evaluate_classifier.py `
  --model models/classification/waste_classifier_v1_final.h5 `
  --data datasets/TACO/data/val
```

## 🐛 Troubleshooting

### GPU Not Detected

```powershell
# Check CUDA installation
python -c "import torch; print(torch.cuda.is_available())"

# If False, reinstall PyTorch with CUDA
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

### Out of Memory Error

Reduce batch size:
```powershell
python training/train_detector.py --batch 8  # Instead of 16
```

### Module Not Found

```powershell
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

## 📦 Export Models

### ONNX Format (for deployment)

```powershell
# YOLOv8 to ONNX
python -c "from ultralytics import YOLO; YOLO('models/detection/waste_detector_v1_final.pt').export(format='onnx')"

# TensorFlow to TFLite
python utils/convert_to_tflite.py
```

## 🔗 Useful Commands

```powershell
# Check model info
python -c "from ultralytics import YOLO; model = YOLO('model.pt'); print(model.info())"

# Monitor GPU usage
nvidia-smi -l 1

# Clean up old checkpoints
Remove-Item -Recurse -Force models/*/checkpoints/*.pt -Exclude best.pt

# Zip results for sharing
Compress-Archive -Path models/detection -DestinationPath detection_models.zip
```

## 📚 Additional Resources

- [YOLOv8 Documentation](https://docs.ultralytics.com/)
- [TensorFlow/Keras Guide](https://www.tensorflow.org/guide)
- [Stable-Baselines3 Docs](https://stable-baselines3.readthedocs.io/)
- [TACO Dataset Paper](http://tacodataset.org/)

## 🆘 Getting Help

1. Check README.md for detailed documentation
2. Review DEVELOP.md for architecture details
3. Check GitHub Issues
4. Contact: [your-email@example.com]

---

**Happy Training! 🤖🌊**
