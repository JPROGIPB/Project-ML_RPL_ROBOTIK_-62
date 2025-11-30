"""
SEALEN ML System Setup Script
Automate environment setup and dataset download
"""

import os
import sys
import subprocess
from pathlib import Path
import argparse

def run_command(cmd, description):
    """Run shell command and handle errors"""
    print(f"\n{'='*60}")
    print(f"🔄 {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=True,
            text=True,
            capture_output=True
        )
        print(result.stdout)
        print(f"✅ {description} - SUCCESS")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - FAILED")
        print(f"Error: {e.stderr}")
        return False

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directory structure...")
    
    directories = [
        "datasets/TACO",
        "datasets/SeaClear",
        "datasets/processed",
        "models/detection",
        "models/classification",
        "models/reinforcement",
        "outputs/detections",
        "outputs/classifications",
        "outputs/rl_logs",
        "logs",
        "notebooks",
        "tests"
    ]
    
    for directory in directories:
        path = Path(directory)
        path.mkdir(parents=True, exist_ok=True)
        print(f"  ✓ Created: {directory}")
    
    print("✅ Directory structure created")

def install_dependencies(requirements_file="requirements.txt"):
    """Install Python dependencies"""
    if not Path(requirements_file).exists():
        print(f"⚠️ {requirements_file} not found, skipping dependency installation")
        return False
    
    return run_command(
        f"pip install -r {requirements_file}",
        "Installing Python dependencies"
    )

def download_taco_dataset():
    """Download TACO dataset"""
    taco_dir = Path("datasets/TACO")
    
    if (taco_dir / "data").exists():
        print("\n✓ TACO dataset already exists")
        return True
    
    print("\n📥 Downloading TACO dataset...")
    
    # Clone TACO repository
    if not run_command(
        f"git clone https://github.com/pedropro/TACO.git {taco_dir}",
        "Cloning TACO repository"
    ):
        return False
    
    # Download dataset
    print("\n⚠️ Manual step required:")
    print("1. Go to http://tacodataset.org/")
    print("2. Download the dataset")
    print(f"3. Extract to: {taco_dir / 'data'}")
    print("\nOr run the TACO download script:")
    print(f"  cd {taco_dir}")
    print("  python download.py")
    
    return True

def setup_tensorboard():
    """Setup TensorBoard logging"""
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    print("\n📊 TensorBoard setup complete")
    print(f"To view training logs, run:")
    print(f"  tensorboard --logdir={logs_dir}")
    
    return True

def verify_gpu():
    """Verify GPU availability"""
    print("\n🔍 Checking GPU availability...")
    
    try:
        import torch
        if torch.cuda.is_available():
            print(f"✅ GPU available: {torch.cuda.get_device_name(0)}")
            print(f"   CUDA version: {torch.version.cuda}")
            print(f"   GPU memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
            return True
        else:
            print("⚠️ No GPU detected - training will be slower on CPU")
            return False
    except ImportError:
        print("⚠️ PyTorch not installed yet - run setup with --install-deps")
        return False

def create_sample_config():
    """Create sample configuration files"""
    print("\n📝 Creating sample configuration...")
    
    # Create .env file
    env_content = """# SEALEN ML Environment Variables

# API Settings
API_HOST=0.0.0.0
API_PORT=8000

# Model Paths
DETECTOR_PATH=models/detection/waste_detector_v1_final.pt
CLASSIFIER_PATH=models/classification/waste_classifier_v1_final.h5
RL_AGENT_PATH=models/reinforcement/dqn_ocean_cleaning_final.zip

# Training Settings
BATCH_SIZE=32
LEARNING_RATE=0.001
EPOCHS=100

# Dataset Paths
TACO_PATH=datasets/TACO/data
SEACLEAR_PATH=datasets/SeaClear/data
"""
    
    with open(".env.example", "w") as f:
        f.write(env_content)
    
    print("  ✓ Created: .env.example")
    print("  Copy .env.example to .env and customize as needed")
    
    return True

def main():
    parser = argparse.ArgumentParser(description='Setup SEALEN ML System')
    parser.add_argument('--skip-deps', action='store_true',
                        help='Skip dependency installation')
    parser.add_argument('--skip-dataset', action='store_true',
                        help='Skip dataset download')
    parser.add_argument('--check-gpu', action='store_true',
                        help='Only check GPU availability')
    args = parser.parse_args()
    
    print("="*60)
    print("🚀 SEALEN ML SYSTEM SETUP")
    print("="*60)
    
    if args.check_gpu:
        verify_gpu()
        return
    
    # Step 1: Create directories
    create_directories()
    
    # Step 2: Install dependencies
    if not args.skip_deps:
        install_dependencies()
    else:
        print("\n⏭️ Skipping dependency installation")
    
    # Step 3: Download datasets
    if not args.skip_dataset:
        download_taco_dataset()
    else:
        print("\n⏭️ Skipping dataset download")
    
    # Step 4: Setup TensorBoard
    setup_tensorboard()
    
    # Step 5: Create sample configs
    create_sample_config()
    
    # Step 6: Verify GPU
    verify_gpu()
    
    # Final summary
    print("\n" + "="*60)
    print("✅ SETUP COMPLETE!")
    print("="*60)
    print("\n📋 Next steps:")
    print("1. Review and customize .env file")
    print("2. Download TACO dataset if not already done")
    print("3. Start training:")
    print("   python training/train_detector.py")
    print("   python training/train_classifier.py")
    print("   python training/train_rl_agent.py")
    print("\n4. Start API server:")
    print("   cd api")
    print("   uvicorn server:app --reload")
    print("\n📚 Read README.md for detailed documentation")
    print("="*60)

if __name__ == "__main__":
    main()
