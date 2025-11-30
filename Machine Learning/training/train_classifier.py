"""
SEALEN - Waste Classification Training Script
Train ResNet50 model for classifying waste types
"""

import os
import argparse
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau, TensorBoard
from pathlib import Path
import json
from datetime import datetime

def parse_args():
    parser = argparse.ArgumentParser(description='Train ResNet50 Waste Classification Model')
    parser.add_argument('--data_dir', type=str, default='../datasets/TACO/data',
                        help='Path to dataset directory')
    parser.add_argument('--epochs', type=int, default=50,
                        help='Number of training epochs')
    parser.add_argument('--batch', type=int, default=32,
                        help='Batch size')
    parser.add_argument('--img_size', type=int, default=224,
                        help='Image size (224 for ResNet50)')
    parser.add_argument('--output_dir', type=str, default='../models/classification',
                        help='Output directory for models')
    parser.add_argument('--name', type=str, default='waste_classifier_v1',
                        help='Model name')
    parser.add_argument('--lr', type=float, default=0.001,
                        help='Learning rate')
    parser.add_argument('--unfreeze', type=int, default=0,
                        help='Number of layers to unfreeze from base model (0=freeze all)')
    return parser.parse_args()

def create_model(num_classes, img_size=224, unfreeze_layers=0):
    """Create ResNet50 model with transfer learning"""
    
    # Load pretrained ResNet50
    base_model = ResNet50(
        weights='imagenet',
        include_top=False,
        input_shape=(img_size, img_size, 3)
    )
    
    # Freeze base layers
    base_model.trainable = False
    
    # Optionally unfreeze top layers
    if unfreeze_layers > 0:
        for layer in base_model.layers[-unfreeze_layers:]:
            layer.trainable = True
    
    # Add custom classification head
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(512, activation='relu')(x)
    x = Dropout(0.5)(x)
    x = Dense(256, activation='relu')(x)
    x = Dropout(0.3)(x)
    output = Dense(num_classes, activation='softmax')(x)
    
    # Create model
    model = Model(inputs=base_model.input, outputs=output)
    
    return model

def create_data_generators(data_dir, img_size, batch_size):
    """Create training and validation data generators"""
    
    # Training augmentation
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=30,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        vertical_flip=False,
        zoom_range=0.2,
        shear_range=0.1,
        fill_mode='nearest',
        validation_split=0.2  # 80-20 split
    )
    
    # Validation (no augmentation)
    val_datagen = ImageDataGenerator(
        rescale=1./255,
        validation_split=0.2
    )
    
    # Training data
    train_generator = train_datagen.flow_from_directory(
        data_dir,
        target_size=(img_size, img_size),
        batch_size=batch_size,
        class_mode='categorical',
        subset='training',
        shuffle=True
    )
    
    # Validation data
    val_generator = val_datagen.flow_from_directory(
        data_dir,
        target_size=(img_size, img_size),
        batch_size=batch_size,
        class_mode='categorical',
        subset='validation',
        shuffle=False
    )
    
    return train_generator, val_generator

def main():
    args = parse_args()
    
    # Create output directory
    output_path = Path(args.output_dir) / args.name
    output_path.mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print("SEALEN - Waste Classification Training")
    print("=" * 60)
    print(f"Data Directory: {args.data_dir}")
    print(f"Epochs: {args.epochs}")
    print(f"Batch Size: {args.batch}")
    print(f"Image Size: {args.img_size}")
    print(f"Learning Rate: {args.lr}")
    print(f"Output: {output_path}")
    print("=" * 60)
    
    # Create data generators
    print("\n[1/5] Loading dataset...")
    train_gen, val_gen = create_data_generators(
        args.data_dir, 
        args.img_size, 
        args.batch
    )
    
    num_classes = len(train_gen.class_indices)
    print(f"Found {num_classes} classes:")
    for class_name, class_idx in sorted(train_gen.class_indices.items(), key=lambda x: x[1]):
        print(f"  {class_idx}: {class_name}")
    
    # Save class mapping
    class_mapping = {v: k for k, v in train_gen.class_indices.items()}
    with open(output_path / 'class_mapping.json', 'w') as f:
        json.dump(class_mapping, f, indent=2)
    
    # Create model
    print("\n[2/5] Building model...")
    model = create_model(num_classes, args.img_size, args.unfreeze)
    
    # Compile model
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=args.lr),
        loss='categorical_crossentropy',
        metrics=['accuracy', 
                 keras.metrics.Precision(name='precision'),
                 keras.metrics.Recall(name='recall')]
    )
    
    # Model summary
    print(f"\nModel Parameters: {model.count_params():,}")
    trainable_params = sum([tf.size(w).numpy() for w in model.trainable_weights])
    print(f"Trainable Parameters: {trainable_params:,}")
    
    # Callbacks
    callbacks = [
        ModelCheckpoint(
            filepath=str(output_path / 'best_model.h5'),
            monitor='val_accuracy',
            save_best_only=True,
            mode='max',
            verbose=1
        ),
        EarlyStopping(
            monitor='val_loss',
            patience=15,
            restore_best_weights=True,
            verbose=1
        ),
        ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-7,
            verbose=1
        ),
        TensorBoard(
            log_dir=str(output_path / 'logs'),
            histogram_freq=1
        )
    ]
    
    # Train model
    print("\n[3/5] Starting training...")
    history = model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=args.epochs,
        callbacks=callbacks,
        verbose=1
    )
    
    # Evaluate model
    print("\n[4/5] Evaluating model...")
    results = model.evaluate(val_gen, verbose=1)
    
    print("\n" + "=" * 60)
    print("VALIDATION RESULTS")
    print("=" * 60)
    print(f"Loss: {results[0]:.4f}")
    print(f"Accuracy: {results[1]:.4f}")
    print(f"Precision: {results[2]:.4f}")
    print(f"Recall: {results[3]:.4f}")
    print("=" * 60)
    
    # Save final model
    print("\n[5/5] Saving model...")
    model.save(output_path / f'{args.name}_final.h5')
    
    # Save training history
    history_dict = {
        'accuracy': [float(x) for x in history.history['accuracy']],
        'val_accuracy': [float(x) for x in history.history['val_accuracy']],
        'loss': [float(x) for x in history.history['loss']],
        'val_loss': [float(x) for x in history.history['val_loss']],
    }
    
    with open(output_path / 'training_history.json', 'w') as f:
        json.dump(history_dict, f, indent=2)
    
    # Save training config
    config = {
        'model_name': args.name,
        'num_classes': num_classes,
        'img_size': args.img_size,
        'batch_size': args.batch,
        'epochs': args.epochs,
        'learning_rate': args.lr,
        'final_accuracy': float(results[1]),
        'final_precision': float(results[2]),
        'final_recall': float(results[3]),
        'trained_on': datetime.now().isoformat()
    }
    
    with open(output_path / 'config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"\n✅ Training completed successfully!")
    print(f"📁 Model saved to: {output_path}")
    
    # Performance check
    if results[1] >= 0.85:
        print("🎉 Target accuracy (>85%) achieved!")
    else:
        print(f"⚠️ Accuracy is {results[1]:.2%}, target is 85%")
        print("   Consider training for more epochs or unfreezing more layers")

if __name__ == '__main__':
    main()