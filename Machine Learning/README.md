# 🤖 SEALEN - Machine Learning System

Sistem Machine Learning untuk deteksi, klasifikasi, dan navigasi robot pembersih laut.

## 📁 Struktur Direktori

```
Machine Learning/
├── datasets/              # Dataset dan preprocessing
│   ├── TACO/             # TACO trash dataset
│   ├── SeaClear/         # Marine debris dataset
│   └── processed/        # Data terproses
├── models/               # Trained models
│   ├── detection/        # YOLOv8 models
│   ├── classification/   # ResNet50 models
│   └── reinforcement/    # DQN agents
├── training/             # Training scripts
│   ├── train_detector.py
│   ├── train_classifier.py
│   └── train_rl_agent.py
├── inference/            # Inference scripts
│   ├── detect_waste.py
│   ├── classify_waste.py
│   └── rl_control.py
├── api/                  # API integration
│   ├── server.py
│   ├── endpoints/
│   └── schemas/
├── notebooks/            # Jupyter notebooks
│   ├── 01_data_exploration.ipynb
│   ├── 02_model_training.ipynb
│   └── 03_evaluation.ipynb
├── utils/                # Utilities
│   ├── data_loader.py
│   ├── metrics.py
│   └── visualization.py
├── configs/              # Configuration files
│   ├── taco.yaml
│   ├── model_config.py
│   └── training_config.py
├── tests/                # Unit tests
└── requirements.txt      # Dependencies
```

## 🚀 Quick Start

### 1. Setup Environment
```powershell
# Create conda environment
conda create -n sealen python=3.9
conda activate sealen

# Install dependencies
pip install -r requirements.txt
```

### 2. Download Datasets
```powershell
# TACO Dataset
cd datasets
git clone https://github.com/pedropro/TACO.git
cd TACO
python download.py
```

### 3. Train Models
```powershell
# Model 1: Waste Detection (YOLOv8)
python training/train_detector.py --epochs 100 --batch 16

# Model 2: Waste Classification (ResNet50)
python training/train_classifier.py --epochs 50 --batch 32

# Model 3: RL Agent (DQN)
python training/train_rl_agent.py --timesteps 500000
```

### 4. Run API Server
```powershell
cd api
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```

## 📊 Models Overview

### Model 1: Waste Detection
- **Architecture**: YOLOv8n
- **Input**: 640x640 RGB images
- **Output**: Bounding boxes + class labels
- **Target mAP@0.5**: >75%

### Model 2: Waste Classification
- **Architecture**: ResNet50 + Transfer Learning
- **Input**: 224x224 RGB images
- **Output**: 10-class probabilities
- **Target Accuracy**: >85%

### Model 3: Reinforcement Learning
- **Architecture**: Deep Q-Network (DQN)
- **State Space**: 5D (robot_pos, battery, waste_pos)
- **Action Space**: 5 actions (N, S, E, W, Collect)
- **Target Success Rate**: >80%

## 📈 Performance Metrics

| Model | Metric | Target | Current |
|-------|--------|--------|---------|
| Detection | mAP@0.5 | >75% | TBD |
| Classification | Accuracy | >85% | TBD |
| RL Agent | Success Rate | >80% | TBD |

## 🔗 API Endpoints

- `POST /detect` - Detect waste in image
- `POST /classify` - Classify waste type
- `POST /rl_action` - Get RL agent action
- `GET /models/info` - Get model information

## 📝 Development Phases

- [x] Phase 1: Directory structure setup
- [ ] Phase 2: Dataset preparation (Week 1-2)
- [ ] Phase 3: Waste detection training (Week 1-2)
- [ ] Phase 4: Classification training (Week 3-4)
- [ ] Phase 5: RL agent training (Week 5-8)
- [ ] Phase 6: API integration (Week 9-10)
- [ ] Phase 7: Testing & deployment

## 🛠️ Requirements

- **Hardware**: GPU (GTX 1060 or better)
- **Storage**: 50GB minimum
- **RAM**: 16GB minimum
- **OS**: Windows/Linux/MacOS

## 📚 References

- [TACO Dataset](http://tacodataset.org/)
- [YOLOv8 Documentation](https://docs.ultralytics.com/)
- [Stable-Baselines3](https://stable-baselines3.readthedocs.io/)
