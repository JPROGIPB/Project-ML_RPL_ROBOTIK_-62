"""
Data loader utilities for SEALEN ML system
"""

import os
import json
import numpy as np
from pathlib import Path
from typing import List, Tuple, Dict
import cv2
from PIL import Image

def load_taco_annotations(anno_path: str) -> Dict:
    """
    Load TACO dataset annotations (COCO format)
    
    Args:
        anno_path: Path to annotations JSON file
        
    Returns:
        Dictionary with images, annotations, and categories
    """
    with open(anno_path, 'r') as f:
        annotations = json.load(f)
    
    return annotations

def get_class_mapping(annotations: Dict) -> Dict[int, str]:
    """
    Get class ID to name mapping from TACO annotations
    
    Args:
        annotations: TACO annotations dictionary
        
    Returns:
        Dictionary mapping class IDs to names
    """
    class_mapping = {}
    for category in annotations['categories']:
        class_mapping[category['id']] = category['name']
    
    return class_mapping

def load_image(image_path: str, target_size: Tuple[int, int] = None) -> np.ndarray:
    """
    Load and preprocess image
    
    Args:
        image_path: Path to image file
        target_size: Optional (width, height) to resize image
        
    Returns:
        Numpy array of image
    """
    image = Image.open(image_path)
    
    if target_size:
        image = image.resize(target_size)
    
    return np.array(image)

def normalize_image(image: np.ndarray) -> np.ndarray:
    """
    Normalize image to [0, 1] range
    
    Args:
        image: Input image array
        
    Returns:
        Normalized image array
    """
    return image.astype(np.float32) / 255.0

def augment_image(image: np.ndarray, 
                  rotation: float = 0,
                  flip_h: bool = False,
                  flip_v: bool = False) -> np.ndarray:
    """
    Apply augmentation to image
    
    Args:
        image: Input image
        rotation: Rotation angle in degrees
        flip_h: Horizontal flip
        flip_v: Vertical flip
        
    Returns:
        Augmented image
    """
    # Rotation
    if rotation != 0:
        h, w = image.shape[:2]
        center = (w // 2, h // 2)
        matrix = cv2.getRotationMatrix2D(center, rotation, 1.0)
        image = cv2.warpAffine(image, matrix, (w, h))
    
    # Horizontal flip
    if flip_h:
        image = cv2.flip(image, 1)
    
    # Vertical flip
    if flip_v:
        image = cv2.flip(image, 0)
    
    return image

def split_dataset(data_dir: str, 
                  train_ratio: float = 0.7,
                  val_ratio: float = 0.15,
                  test_ratio: float = 0.15) -> Tuple[List, List, List]:
    """
    Split dataset into train/val/test sets
    
    Args:
        data_dir: Directory containing images
        train_ratio: Ratio for training set
        val_ratio: Ratio for validation set
        test_ratio: Ratio for test set
        
    Returns:
        Tuple of (train_files, val_files, test_files)
    """
    assert abs(train_ratio + val_ratio + test_ratio - 1.0) < 1e-6, \
        "Ratios must sum to 1.0"
    
    # Get all image files
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    image_files = []
    
    for ext in image_extensions:
        image_files.extend(Path(data_dir).glob(f'*{ext}'))
    
    # Shuffle
    np.random.shuffle(image_files)
    
    # Split
    n_total = len(image_files)
    n_train = int(n_total * train_ratio)
    n_val = int(n_total * val_ratio)
    
    train_files = image_files[:n_train]
    val_files = image_files[n_train:n_train + n_val]
    test_files = image_files[n_train + n_val:]
    
    return train_files, val_files, test_files

def batch_generator(file_list: List[str],
                   batch_size: int = 32,
                   target_size: Tuple[int, int] = (224, 224),
                   shuffle: bool = True):
    """
    Generate batches of images
    
    Args:
        file_list: List of image file paths
        batch_size: Batch size
        target_size: Target image size
        shuffle: Whether to shuffle data
        
    Yields:
        Batch of images
    """
    n_samples = len(file_list)
    indices = np.arange(n_samples)
    
    while True:
        if shuffle:
            np.random.shuffle(indices)
        
        for start_idx in range(0, n_samples, batch_size):
            end_idx = min(start_idx + batch_size, n_samples)
            batch_indices = indices[start_idx:end_idx]
            
            batch_images = []
            for idx in batch_indices:
                img = load_image(file_list[idx], target_size)
                img = normalize_image(img)
                batch_images.append(img)
            
            yield np.array(batch_images)

def save_predictions(predictions: List[Dict], output_path: str):
    """
    Save predictions to JSON file
    
    Args:
        predictions: List of prediction dictionaries
        output_path: Path to save JSON file
    """
    with open(output_path, 'w') as f:
        json.dump(predictions, f, indent=2)
    
    print(f"Predictions saved to: {output_path}")

def load_model_config(config_path: str) -> Dict:
    """
    Load model configuration from JSON
    
    Args:
        config_path: Path to config JSON file
        
    Returns:
        Configuration dictionary
    """
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    return config
