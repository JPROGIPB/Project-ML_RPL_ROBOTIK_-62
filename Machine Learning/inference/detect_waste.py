"""
SEALEN - Waste Detection Inference Script
Run waste detection on images or video using trained YOLOv8 model
"""

import argparse
from pathlib import Path
from ultralytics import YOLO
import cv2
import numpy as np

def parse_args():
    parser = argparse.ArgumentParser(description='Run waste detection inference')
    parser.add_argument('--model', type=str, required=True,
                        help='Path to trained YOLOv8 model (.pt file)')
    parser.add_argument('--source', type=str, required=True,
                        help='Path to image, video, or folder')
    parser.add_argument('--conf', type=float, default=0.5,
                        help='Confidence threshold (0-1)')
    parser.add_argument('--save', action='store_true',
                        help='Save detection results')
    parser.add_argument('--show', action='store_true',
                        help='Display results')
    parser.add_argument('--output', type=str, default='../outputs/detections',
                        help='Output directory for results')
    return parser.parse_args()

def main():
    args = parse_args()
    
    # Create output directory
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print("SEALEN - Waste Detection Inference")
    print("=" * 60)
    print(f"Model: {args.model}")
    print(f"Source: {args.source}")
    print(f"Confidence: {args.conf}")
    print("=" * 60)
    
    # Load model
    print("\nLoading model...")
    model = YOLO(args.model)
    
    # Run inference
    print("Running inference...")
    results = model.predict(
        source=args.source,
        conf=args.conf,
        save=args.save,
        show=args.show,
        project=str(output_dir),
        name='run',
        stream=True  # Use streaming for large videos
    )
    
    # Process results
    total_detections = 0
    class_counts = {}
    
    for i, result in enumerate(results):
        num_detections = len(result.boxes)
        total_detections += num_detections
        
        print(f"\nImage {i+1}: {num_detections} objects detected")
        
        for box in result.boxes:
            cls = int(box.cls)
            cls_name = result.names[cls]
            conf = float(box.conf)
            
            class_counts[cls_name] = class_counts.get(cls_name, 0) + 1
            print(f"  - {cls_name}: {conf:.2f}")
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total detections: {total_detections}")
    print("\nClass distribution:")
    for cls_name, count in sorted(class_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {cls_name}: {count}")
    print("=" * 60)
    
    if args.save:
        print(f"\n✅ Results saved to: {output_dir / 'run'}")

if __name__ == '__main__':
    main()
