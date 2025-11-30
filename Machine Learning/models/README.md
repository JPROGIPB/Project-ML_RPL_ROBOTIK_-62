# Machine Learning Models

This directory contains trained ML models for the SEALEN project.

## Structure

```
models/
├── detection/              # YOLOv8 waste detection models
│   ├── waste_detector_v1_final.pt
│   └── checkpoints/
├── classification/         # ResNet50 classification models
│   ├── waste_classifier_v1/
│   │   ├── waste_classifier_v1_final.h5
│   │   ├── class_mapping.json
│   │   └── config.json
│   └── checkpoints/
└── reinforcement/          # DQN RL agents
    ├── dqn_ocean_cleaning/
    │   ├── dqn_ocean_cleaning_final.zip
    │   └── results.json
    └── checkpoints/
```

## Model Files

### Detection Models (.pt)
- YOLOv8 PyTorch format
- Can be loaded with: `YOLO('model.pt')`
- Size: ~50MB

### Classification Models (.h5)
- Keras/TensorFlow format
- Can be loaded with: `tf.keras.models.load_model('model.h5')`
- Size: ~100MB

### RL Models (.zip)
- Stable-Baselines3 format
- Can be loaded with: `DQN.load('model.zip')`
- Size: ~5MB

## Usage

See parent README.md for training and inference instructions.

## Notes

- Models are gitignored by default (too large)
- Use model versioning (v1, v2, etc.)
- Keep best checkpoints only
- Document model performance in config.json
