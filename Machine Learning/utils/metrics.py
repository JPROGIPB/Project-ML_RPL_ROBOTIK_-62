"""
Metrics and evaluation utilities for SEALEN ML system
"""

import numpy as np
from sklearn.metrics import (
    confusion_matrix, 
    classification_report,
    precision_recall_curve,
    average_precision_score
)
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Tuple

def calculate_map(y_true: np.ndarray, 
                  y_pred: np.ndarray, 
                  y_scores: np.ndarray,
                  iou_threshold: float = 0.5) -> float:
    """
    Calculate mean Average Precision (mAP)
    
    Args:
        y_true: True labels
        y_pred: Predicted labels
        y_scores: Prediction scores
        iou_threshold: IoU threshold
        
    Returns:
        mAP score
    """
    # Simplified mAP calculation
    # For full mAP, use YOLO's built-in metrics
    ap_scores = []
    
    for class_id in np.unique(y_true):
        mask = (y_true == class_id)
        if mask.sum() == 0:
            continue
        
        ap = average_precision_score(
            (y_true == class_id).astype(int),
            y_scores[:, class_id]
        )
        ap_scores.append(ap)
    
    return np.mean(ap_scores)

def plot_confusion_matrix(y_true: np.ndarray,
                         y_pred: np.ndarray,
                         class_names: List[str],
                         save_path: str = None):
    """
    Plot confusion matrix
    
    Args:
        y_true: True labels
        y_pred: Predicted labels
        class_names: List of class names
        save_path: Path to save plot
    """
    cm = confusion_matrix(y_true, y_pred)
    
    plt.figure(figsize=(12, 10))
    sns.heatmap(
        cm, 
        annot=True, 
        fmt='d',
        cmap='Blues',
        xticklabels=class_names,
        yticklabels=class_names
    )
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Confusion matrix saved to: {save_path}")
    
    plt.show()

def plot_precision_recall_curve(y_true: np.ndarray,
                                y_scores: np.ndarray,
                                class_names: List[str],
                                save_path: str = None):
    """
    Plot precision-recall curves for each class
    
    Args:
        y_true: True labels (one-hot encoded)
        y_scores: Prediction scores
        class_names: List of class names
        save_path: Path to save plot
    """
    plt.figure(figsize=(12, 8))
    
    for i, class_name in enumerate(class_names):
        precision, recall, _ = precision_recall_curve(
            y_true[:, i], 
            y_scores[:, i]
        )
        ap = average_precision_score(y_true[:, i], y_scores[:, i])
        
        plt.plot(
            recall, 
            precision, 
            label=f'{class_name} (AP={ap:.2f})'
        )
    
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Precision-Recall Curves')
    plt.legend(loc='best')
    plt.grid(True)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"PR curve saved to: {save_path}")
    
    plt.show()

def calculate_detection_metrics(predictions: List[Dict],
                               ground_truths: List[Dict],
                               iou_threshold: float = 0.5) -> Dict:
    """
    Calculate detection metrics (precision, recall, F1)
    
    Args:
        predictions: List of prediction dictionaries
        ground_truths: List of ground truth dictionaries
        iou_threshold: IoU threshold for matching
        
    Returns:
        Dictionary of metrics
    """
    tp = 0  # True positives
    fp = 0  # False positives
    fn = 0  # False negatives
    
    for pred, gt in zip(predictions, ground_truths):
        pred_boxes = pred.get('boxes', [])
        gt_boxes = gt.get('boxes', [])
        
        matched_gt = set()
        
        for pred_box in pred_boxes:
            best_iou = 0
            best_gt_idx = -1
            
            for gt_idx, gt_box in enumerate(gt_boxes):
                if gt_idx in matched_gt:
                    continue
                
                iou = calculate_iou(pred_box, gt_box)
                if iou > best_iou:
                    best_iou = iou
                    best_gt_idx = gt_idx
            
            if best_iou >= iou_threshold:
                tp += 1
                matched_gt.add(best_gt_idx)
            else:
                fp += 1
        
        fn += len(gt_boxes) - len(matched_gt)
    
    # Calculate metrics
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    
    return {
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'true_positives': tp,
        'false_positives': fp,
        'false_negatives': fn
    }

def calculate_iou(box1: List[float], box2: List[float]) -> float:
    """
    Calculate Intersection over Union (IoU) between two boxes
    
    Args:
        box1: [x1, y1, x2, y2]
        box2: [x1, y1, x2, y2]
        
    Returns:
        IoU score
    """
    x1_min, y1_min, x1_max, y1_max = box1
    x2_min, y2_min, x2_max, y2_max = box2
    
    # Intersection area
    inter_x_min = max(x1_min, x2_min)
    inter_y_min = max(y1_min, y2_min)
    inter_x_max = min(x1_max, x2_max)
    inter_y_max = min(y1_max, y2_max)
    
    if inter_x_max < inter_x_min or inter_y_max < inter_y_min:
        return 0.0
    
    inter_area = (inter_x_max - inter_x_min) * (inter_y_max - inter_y_min)
    
    # Union area
    box1_area = (x1_max - x1_min) * (y1_max - y1_min)
    box2_area = (x2_max - x2_min) * (y2_max - y2_min)
    union_area = box1_area + box2_area - inter_area
    
    return inter_area / union_area if union_area > 0 else 0.0

def print_classification_report(y_true: np.ndarray,
                               y_pred: np.ndarray,
                               class_names: List[str]):
    """
    Print detailed classification report
    
    Args:
        y_true: True labels
        y_pred: Predicted labels
        class_names: List of class names
    """
    report = classification_report(
        y_true, 
        y_pred, 
        target_names=class_names,
        digits=4
    )
    
    print("=" * 60)
    print("CLASSIFICATION REPORT")
    print("=" * 60)
    print(report)
    print("=" * 60)

def calculate_rl_metrics(episode_rewards: List[float],
                        episode_lengths: List[int],
                        success_flags: List[bool]) -> Dict:
    """
    Calculate RL agent performance metrics
    
    Args:
        episode_rewards: List of episode rewards
        episode_lengths: List of episode lengths
        success_flags: List of success flags
        
    Returns:
        Dictionary of metrics
    """
    return {
        'mean_reward': np.mean(episode_rewards),
        'std_reward': np.std(episode_rewards),
        'min_reward': np.min(episode_rewards),
        'max_reward': np.max(episode_rewards),
        'mean_length': np.mean(episode_lengths),
        'success_rate': np.mean(success_flags),
        'num_episodes': len(episode_rewards)
    }

def plot_training_history(history: Dict, save_path: str = None):
    """
    Plot training history (loss and accuracy curves)
    
    Args:
        history: Training history dictionary
        save_path: Path to save plot
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    
    # Loss plot
    ax1.plot(history['loss'], label='Training Loss')
    ax1.plot(history['val_loss'], label='Validation Loss')
    ax1.set_title('Model Loss')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Loss')
    ax1.legend()
    ax1.grid(True)
    
    # Accuracy plot
    ax2.plot(history['accuracy'], label='Training Accuracy')
    ax2.plot(history['val_accuracy'], label='Validation Accuracy')
    ax2.set_title('Model Accuracy')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Accuracy')
    ax2.legend()
    ax2.grid(True)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Training history plot saved to: {save_path}")
    
    plt.show()
