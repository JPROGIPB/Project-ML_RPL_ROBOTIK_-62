"""
SEALEN - YOLOv8 Waste Detection Training Script
Train YOLOv8 model for detecting trash in marine environments
"""

import os
import argparse
from pathlib import Path
from ultralytics import YOLO
import yaml

def parse_args():
    parser = argparse.ArgumentParser(description='Train YOLOv8 Waste Detection Model')
    parser.add_argument('--data', type=str, default='../configs/taco.yaml', 
                        help='Path to dataset YAML config')
    parser.add_argument('--model', type=str, default='yolov8n.pt', 
                        help='Pretrained model size (yolov8n/s/m/l/x)')
    parser.add_argument('--epochs', type=int, default=100, 
                        help='Number of training epochs')
    parser.add_argument('--batch', type=int, default=16, 
                        help='Batch size')
    parser.add_argument('--imgsz', type=int, default=640, 
                        help='Image size')
    parser.add_argument('--device', type=str, default='0', 
                        help='Device to train on (0 for GPU, cpu for CPU)')
    parser.add_argument('--project', type=str, default='../models/detection', 
                        help='Project folder to save results')
    parser.add_argument('--name', type=str, default='waste_detector_v1', 
                        help='Experiment name')
    parser.add_argument('--resume', action='store_true', 
                        help='Resume training from last checkpoint')
    return parser.parse_args()

def main():
    args = parse_args()
    
    # Create output directory
    os.makedirs(args.project, exist_ok=True)
    
    print("=" * 60)
    print("SEALEN - Waste Detection Training")
    print("=" * 60)
    print(f"Model: {args.model}")
    print(f"Dataset: {args.data}")
    print(f"Epochs: {args.epochs}")
    print(f"Batch Size: {args.batch}")
    print(f"Image Size: {args.imgsz}")
    print(f"Device: {args.device}")
    print("=" * 60)
    
    # Load pretrained YOLOv8 model
    print("\n[1/4] Loading pretrained YOLOv8 model...")
    model = YOLO(args.model)
    
    # Train model
    print("\n[2/4] Starting training...")
    results = model.train(
        data=args.data,
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
        device=args.device,
        project=args.project,
        name=args.name,
        resume=args.resume,
        # Training hyperparameters
        patience=50,           # Early stopping patience
        save=True,             # Save checkpoints
        save_period=10,        # Save every N epochs
        cache=True,            # Cache images for faster training
        workers=8,             # DataLoader workers
        # Augmentation
        hsv_h=0.015,           # HSV-Hue augmentation
        hsv_s=0.7,             # HSV-Saturation
        hsv_v=0.4,             # HSV-Value
        degrees=0.0,           # Rotation
        translate=0.1,         # Translation
        scale=0.5,             # Scaling
        shear=0.0,             # Shear
        perspective=0.0,       # Perspective
        flipud=0.0,            # Flip up-down
        fliplr=0.5,            # Flip left-right
        mosaic=1.0,            # Mosaic augmentation
        mixup=0.0,             # Mixup augmentation
    )
    
    # Validate model
    print("\n[3/4] Validating model on test set...")
    metrics = model.val()
    
    print("\n" + "=" * 60)
    print("VALIDATION RESULTS")
    print("=" * 60)
    print(f"mAP@0.5: {metrics.box.map50:.4f}")
    print(f"mAP@0.5:0.95: {metrics.box.map:.4f}")
    print(f"Precision: {metrics.box.mp:.4f}")
    print(f"Recall: {metrics.box.mr:.4f}")
    print("=" * 60)
    
    # Save final model
    print("\n[4/4] Saving final model...")
    model_path = Path(args.project) / args.name / 'weights' / 'best.pt'
    final_path = Path(args.project) / f'{args.name}_final.pt'
    
    if model_path.exists():
        import shutil
        shutil.copy(model_path, final_path)
        print(f"Model saved to: {final_path}")
    
    # Export to ONNX for deployment
    print("\n[Optional] Exporting to ONNX format...")
    try:
        model.export(format='onnx')
        print("ONNX export successful!")
    except Exception as e:
        print(f"ONNX export failed: {e}")
    
    print("\n✅ Training completed successfully!")
    print(f"📁 Results saved in: {Path(args.project) / args.name}")
    
    # Performance check
    if metrics.box.map50 >= 0.75:
        print("🎉 Target mAP@0.5 (>75%) achieved!")
    else:
        print(f"⚠️ mAP@0.5 is {metrics.box.map50:.2%}, target is 75%")
        print("   Consider training for more epochs or tuning hyperparameters")

if __name__ == '__main__':
    main()
