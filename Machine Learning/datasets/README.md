# Datasets

This directory contains datasets for training SEALEN ML models.

## Required Datasets

### 1. TACO Dataset (Trash Annotations in Context)
- **Purpose**: Waste detection and classification
- **Size**: ~1500 images, 60 classes
- **Format**: COCO JSON
- **License**: CC BY 4.0
- **Download**: http://tacodataset.org/

```powershell
git clone https://github.com/pedropro/TACO.git
cd TACO
python download.py
```

### 2. SeaClear Marine Debris (Optional)
- **Purpose**: Underwater waste detection
- **Size**: 8,610 images, 40 categories
- **Format**: COCO + segmentation masks
- **Paper**: https://www.nature.com/articles/s41597-024-03759-2

## Structure

```
datasets/
├── TACO/
│   ├── data/
│   │   ├── images/
│   │   │   ├── train/
│   │   │   ├── val/
│   │   │   └── test/
│   │   └── annotations/
│   │       ├── train.json
│   │       ├── val.json
│   │       └── test.json
│   └── download.py
├── SeaClear/
│   └── data/
└── processed/              # Preprocessed data
    ├── augmented/
    └── normalized/
```

## Data Preprocessing

Run preprocessing scripts:

```powershell
python utils/preprocess_data.py --input datasets/TACO/data --output datasets/processed
```

## Notes

- Datasets are gitignored (too large)
- Download datasets manually or use provided scripts
- Keep raw data separate from processed data
- Document any custom preprocessing steps

## Citation

If using TACO dataset:
```
@article{proenca2020taco,
  title={TACO: Trash Annotations in Context for Litter Detection},
  author={Proença, Pedro F and Simões, Pedro},
  journal={arXiv preprint arXiv:2003.06975},
  year={2020}
}
```
