"""
SEALEN API Server
FastAPI server for serving ML models
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import numpy as np
from PIL import Image
import io
import json
from pathlib import Path

# Import model handlers
try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False

try:
    import tensorflow as tf
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False

try:
    from stable_baselines3 import DQN
    SB3_AVAILABLE = True
except ImportError:
    SB3_AVAILABLE = False

# Initialize FastAPI app
app = FastAPI(
    title="SEALEN ML API",
    description="Marine Robotics AI System - Model Serving API",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model storage
models = {
    'detector': None,
    'classifier': None,
    'rl_agent': None
}

# Pydantic models for request/response
class Detection(BaseModel):
    class_id: int
    class_name: str
    confidence: float
    bbox: List[float]

class DetectionResponse(BaseModel):
    detections: List[Detection]
    image_size: List[int]
    processing_time: float

class ClassificationResponse(BaseModel):
    class_id: int
    class_name: str
    confidence: float
    all_probabilities: Dict[str, float]

class RLState(BaseModel):
    robot_x: float
    robot_y: float
    battery: float
    nearest_waste_x: float
    nearest_waste_y: float

class RLAction(BaseModel):
    action: str
    action_id: int
    confidence: float

class ModelInfo(BaseModel):
    model_type: str
    loaded: bool
    path: Optional[str]

# Startup event - Load models
@app.on_event("startup")
async def load_models():
    """Load all ML models on startup"""
    models_dir = Path("../models")
    
    # Load Detection Model (YOLOv8)
    if YOLO_AVAILABLE:
        detector_path = models_dir / "detection" / "waste_detector_v1_final.pt"
        if detector_path.exists():
            try:
                models['detector'] = YOLO(str(detector_path))
                print(f"✅ Detection model loaded: {detector_path}")
            except Exception as e:
                print(f"❌ Failed to load detection model: {e}")
        else:
            print(f"⚠️ Detection model not found: {detector_path}")
    else:
        print("⚠️ Ultralytics not available, detection disabled")
    
    # Load Classification Model (ResNet50)
    if TF_AVAILABLE:
        classifier_path = models_dir / "classification" / "waste_classifier_v1" / "waste_classifier_v1_final.h5"
        if classifier_path.exists():
            try:
                models['classifier'] = tf.keras.models.load_model(str(classifier_path))
                print(f"✅ Classification model loaded: {classifier_path}")
            except Exception as e:
                print(f"❌ Failed to load classification model: {e}")
        else:
            print(f"⚠️ Classification model not found: {classifier_path}")
    else:
        print("⚠️ TensorFlow not available, classification disabled")
    
    # Load RL Agent (DQN)
    if SB3_AVAILABLE:
        rl_path = models_dir / "reinforcement" / "dqn_ocean_cleaning" / "dqn_ocean_cleaning_final.zip"
        if rl_path.exists():
            try:
                models['rl_agent'] = DQN.load(str(rl_path))
                print(f"✅ RL agent loaded: {rl_path}")
            except Exception as e:
                print(f"❌ Failed to load RL agent: {e}")
        else:
            print(f"⚠️ RL agent not found: {rl_path}")
    else:
        print("⚠️ Stable-Baselines3 not available, RL disabled")

# Health check endpoint
@app.get("/")
async def root():
    return {
        "message": "SEALEN ML API is running",
        "version": "1.0.0",
        "models_loaded": {
            "detector": models['detector'] is not None,
            "classifier": models['classifier'] is not None,
            "rl_agent": models['rl_agent'] is not None
        }
    }

# Detection endpoint
@app.post("/api/detect", response_model=DetectionResponse)
async def detect_waste(file: UploadFile = File(...)):
    """
    Detect waste in uploaded image using YOLOv8
    """
    if models['detector'] is None:
        raise HTTPException(status_code=503, detail="Detection model not loaded")
    
    try:
        # Read and process image
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes))
        
        # Run detection
        import time
        start_time = time.time()
        results = models['detector'].predict(image, conf=0.5, verbose=False)
        processing_time = time.time() - start_time
        
        # Parse results
        detections = []
        for result in results:
            for box in result.boxes:
                detection = Detection(
                    class_id=int(box.cls),
                    class_name=result.names[int(box.cls)],
                    confidence=float(box.conf),
                    bbox=box.xyxy[0].tolist()
                )
                detections.append(detection)
        
        return DetectionResponse(
            detections=detections,
            image_size=[image.width, image.height],
            processing_time=processing_time
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Detection failed: {str(e)}")

# Classification endpoint
@app.post("/api/classify", response_model=ClassificationResponse)
async def classify_waste(file: UploadFile = File(...)):
    """
    Classify waste type using ResNet50
    """
    if models['classifier'] is None:
        raise HTTPException(status_code=503, detail="Classification model not loaded")
    
    try:
        # Read and process image
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes))
        image = image.resize((224, 224))
        image_array = np.array(image) / 255.0
        image_array = np.expand_dims(image_array, axis=0)
        
        # Predict
        predictions = models['classifier'].predict(image_array, verbose=0)
        class_id = int(np.argmax(predictions))
        confidence = float(np.max(predictions))
        
        # Load class mapping
        class_mapping_path = Path("../models/classification/waste_classifier_v1/class_mapping.json")
        if class_mapping_path.exists():
            with open(class_mapping_path) as f:
                class_mapping = json.load(f)
            class_name = class_mapping.get(str(class_id), f"Class {class_id}")
        else:
            class_name = f"Class {class_id}"
        
        # All probabilities
        all_probs = {
            class_mapping.get(str(i), f"Class {i}"): float(predictions[0][i])
            for i in range(len(predictions[0]))
        }
        
        return ClassificationResponse(
            class_id=class_id,
            class_name=class_name,
            confidence=confidence,
            all_probabilities=all_probs
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Classification failed: {str(e)}")

# RL action endpoint
@app.post("/api/rl_action", response_model=RLAction)
async def get_rl_action(state: RLState):
    """
    Get action from RL agent given current state
    """
    if models['rl_agent'] is None:
        raise HTTPException(status_code=503, detail="RL agent not loaded")
    
    try:
        # Convert state to array
        state_array = np.array([
            state.robot_x,
            state.robot_y,
            state.battery,
            state.nearest_waste_x,
            state.nearest_waste_y
        ], dtype=np.float32)
        
        # Predict action
        action, _ = models['rl_agent'].predict(state_array, deterministic=True)
        
        # Action mapping
        action_map = {
            0: 'north',
            1: 'south',
            2: 'east',
            3: 'west',
            4: 'collect'
        }
        
        return RLAction(
            action=action_map[int(action)],
            action_id=int(action),
            confidence=1.0  # DQN doesn't provide confidence scores
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RL prediction failed: {str(e)}")

# Model info endpoint
@app.get("/api/models/info")
async def get_models_info():
    """Get information about loaded models"""
    return {
        "detector": ModelInfo(
            model_type="YOLOv8",
            loaded=models['detector'] is not None,
            path="../models/detection/waste_detector_v1_final.pt"
        ),
        "classifier": ModelInfo(
            model_type="ResNet50",
            loaded=models['classifier'] is not None,
            path="../models/classification/waste_classifier_v1/waste_classifier_v1_final.h5"
        ),
        "rl_agent": ModelInfo(
            model_type="DQN",
            loaded=models['rl_agent'] is not None,
            path="../models/reinforcement/dqn_ocean_cleaning/dqn_ocean_cleaning_final.zip"
        )
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
