# **PANDUAN PENGEMBANGAN MODEL AI SEALEN**

---

## **📦 DATASET - LINK TERPERCAYA**

### **1. TACO Dataset (Deteksi Sampah Umum)** ⭐⭐⭐⭐⭐
```
URL Official: http://tacodataset.org/
GitHub: https://github.com/pedropro/TACO
Kaggle: https://www.kaggle.com/datasets/kneroma/tacotrashdataset

Specs:
- 1,500 gambar
- 60 kelas sampah
- Format: COCO JSON
- Lisensi: CC BY 4.0 (GRATIS)
```

### **2. SeaClear Marine Debris (Sampah Bawah Air)** ⭐⭐⭐⭐⭐
```
URL: https://www.nature.com/articles/s41597-024-03759-2
Download: Check supplementary materials

Specs:
- 8,610 gambar underwater
- 40 kategori objek
- Format: COCO + segmentation masks
- Perfect untuk robot laut
```

### **3. Pre-trained TACO Models**
```
Kaggle: https://www.kaggle.com/datasets/bouweceunen/trained-models-taco-trash-annotations-in-context

Contains:
- SSD MobileNet v2 (trained 100k steps)
- Format: .pb, .uff, .engine
- Ready untuk transfer learning
```

---

## **🎯 MODEL 1: DETEKSI SAMPAH (WASTE DETECTION)**

### **Tujuan**: Deteksi dan lokalisasi sampah dalam gambar

### **Arsitektur**: YOLOv8

### **Code Setup**:
```python
# Install dependencies
pip install ultralytics opencv-python pillow

# Download TACO dataset
git clone https://github.com/pedropro/TACO.git
cd TACO
python3 download.py
```

### **Training Script**:
```python
from ultralytics import YOLO

# Load pretrained YOLOv8
model = YOLO('yolov8n.pt')  # nano version (cepat)

# Train on TACO dataset
results = model.train(
    data='taco.yaml',          # dataset config
    epochs=100,                # jumlah epoch
    imgsz=640,                 # ukuran gambar
    batch=16,                  # batch size
    device=0,                  # GPU
    project='sealen_models',   # folder output
    name='waste_detector'      # nama model
)

# Save model
model.save('waste_detector_v1.pt')
```

### **Dataset Config (taco.yaml)**:
```yaml
# taco.yaml
path: ./TACO/data
train: images/train
val: images/val

# Classes (contoh 10 kelas utama)
names:
  0: plastic_bottle
  1: can
  2: plastic_bag
  3: cigarette
  4: paper
  5: cardboard
  6: glass_bottle
  7: metal
  8: styrofoam
  9: other_trash
```

### **Inference Code**:
```python
# Load trained model
model = YOLO('waste_detector_v1.pt')

# Predict
results = model.predict(
    source='test_image.jpg',
    conf=0.5,                  # confidence threshold
    save=True                  # save hasil
)

# Get detections
for result in results:
    boxes = result.boxes      # bounding boxes
    for box in boxes:
        cls = int(box.cls)    # class
        conf = float(box.conf) # confidence
        coords = box.xyxy[0]  # coordinates
        print(f"Class: {cls}, Conf: {conf:.2f}, Coords: {coords}")
```

### **Expected Performance**:
```
Target Metrics:
- mAP@0.5: >75%
- Inference time: <50ms per image
- Model size: <50MB
```

---

## **🎯 MODEL 2: KLASIFIKASI SAMPAH (WASTE CLASSIFICATION)**

### **Tujuan**: Klasifikasi jenis sampah yang terdeteksi

### **Arsitektur**: ResNet50 + Transfer Learning

### **Training Script**:
```python
import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model

# Load pretrained ResNet50
base_model = ResNet50(
    weights='imagenet',
    include_top=False,
    input_shape=(224, 224, 3)
)

# Freeze base layers
base_model.trainable = False

# Add custom layers
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(256, activation='relu')(x)
x = Dense(128, activation='relu')(x)
output = Dense(10, activation='softmax')(x)  # 10 classes

# Create model
model = Model(inputs=base_model.input, outputs=output)

# Compile
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Train
history = model.fit(
    train_dataset,
    validation_data=val_dataset,
    epochs=50,
    batch_size=32
)

# Save
model.save('waste_classifier_v1.h5')
```

### **Data Preparation**:
```python
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Augmentation
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True,
    zoom_range=0.2
)

val_datagen = ImageDataGenerator(rescale=1./255)

# Load data
train_dataset = train_datagen.flow_from_directory(
    'TACO/data/train',
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical'
)

val_dataset = val_datagen.flow_from_directory(
    'TACO/data/val',
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical'
)
```

### **Expected Performance**:
```
Target Metrics:
- Accuracy: >85%
- Precision/Recall: >80%
- Inference time: <30ms per image
```

---

## **🎯 MODEL 3: REINFORCEMENT LEARNING (ROBOT CONTROL)**

### **Tujuan**: Belajar strategi optimal untuk navigasi dan pengumpulan sampah

### **Arsitektur**: Deep Q-Network (DQN)

### **Environment Setup**:
```python
import gym
import numpy as np

class OceanCleaningEnv(gym.Env):
    """Custom Environment untuk Robot Pembersih Laut"""
    
    def __init__(self, grid_size=20):
        super(OceanCleaningEnv, self).__init__()
        
        self.grid_size = grid_size
        
        # State: [robot_x, robot_y, battery, nearest_waste_x, nearest_waste_y]
        self.observation_space = gym.spaces.Box(
            low=0, high=grid_size, 
            shape=(5,), dtype=np.float32
        )
        
        # Actions: 0=N, 1=S, 2=E, 3=W, 4=Collect
        self.action_space = gym.spaces.Discrete(5)
        
        self.reset()
    
    def reset(self):
        # Robot position
        self.robot_pos = [self.grid_size//2, self.grid_size//2]
        self.battery = 100
        
        # Generate random waste
        self.waste_positions = []
        for _ in range(10):
            pos = [np.random.randint(0, self.grid_size),
                   np.random.randint(0, self.grid_size)]
            self.waste_positions.append(pos)
        
        return self._get_state()
    
    def step(self, action):
        # Move robot
        if action == 0:   # North
            self.robot_pos[1] = max(0, self.robot_pos[1] - 1)
        elif action == 1: # South
            self.robot_pos[1] = min(self.grid_size-1, self.robot_pos[1] + 1)
        elif action == 2: # East
            self.robot_pos[0] = min(self.grid_size-1, self.robot_pos[0] + 1)
        elif action == 3: # West
            self.robot_pos[0] = max(0, self.robot_pos[0] - 1)
        elif action == 4: # Collect
            # Check if waste nearby
            for waste in self.waste_positions:
                if self._distance(self.robot_pos, waste) < 1:
                    self.waste_positions.remove(waste)
                    return self._get_state(), 10, False, {}  # reward +10
        
        # Battery drain
        self.battery -= 1
        
        # Calculate reward
        reward = -0.1  # time penalty
        if self.battery < 20:
            reward -= 5  # low battery penalty
        
        # Check done
        done = (self.battery <= 0 or len(self.waste_positions) == 0)
        
        return self._get_state(), reward, done, {}
    
    def _get_state(self):
        if len(self.waste_positions) > 0:
            nearest_waste = min(self.waste_positions, 
                              key=lambda w: self._distance(self.robot_pos, w))
        else:
            nearest_waste = [0, 0]
        
        return np.array([
            self.robot_pos[0] / self.grid_size,
            self.robot_pos[1] / self.grid_size,
            self.battery / 100,
            nearest_waste[0] / self.grid_size,
            nearest_waste[1] / self.grid_size
        ], dtype=np.float32)
    
    def _distance(self, pos1, pos2):
        return np.sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)
```

### **DQN Training**:
```python
from stable_baselines3 import DQN
from stable_baselines3.common.callbacks import CheckpointCallback

# Create environment
env = OceanCleaningEnv()

# Checkpoint callback
checkpoint_callback = CheckpointCallback(
    save_freq=10000,
    save_path='./models/',
    name_prefix='dqn_ocean_cleaning'
)

# Create DQN model
model = DQN(
    policy='MlpPolicy',
    env=env,
    learning_rate=1e-4,
    buffer_size=50000,
    learning_starts=1000,
    batch_size=32,
    tau=1.0,
    gamma=0.99,
    exploration_fraction=0.1,
    exploration_final_eps=0.02,
    verbose=1,
    tensorboard_log="./tensorboard/"
)

# Train
model.learn(
    total_timesteps=500000,
    callback=checkpoint_callback
)

# Save final model
model.save("dqn_ocean_cleaning_final")
```

### **Testing/Inference**:
```python
# Load trained model
model = DQN.load("dqn_ocean_cleaning_final")

# Test
env = OceanCleaningEnv()
obs = env.reset()

for _ in range(1000):
    action, _states = model.predict(obs, deterministic=True)
    obs, reward, done, info = env.step(action)
    
    if done:
        print("Mission completed!")
        break
```

### **Expected Performance**:
```
Target Metrics:
- Average reward: >50 per episode
- Success rate: >80%
- Training time: ~2-4 hours
```

---

## **🔧 INTEGRASI MODEL KE SISTEM**

### **1. Model Serving (FastAPI)**:
```python
from fastapi import FastAPI, File, UploadFile
from ultralytics import YOLO
import tensorflow as tf
import numpy as np
from PIL import Image
import io

app = FastAPI()

# Load models
waste_detector = YOLO('waste_detector_v1.pt')
waste_classifier = tf.keras.models.load_model('waste_classifier_v1.h5')
rl_agent = DQN.load("dqn_ocean_cleaning_final")

@app.post("/detect")
async def detect_waste(file: UploadFile = File(...)):
    """Deteksi sampah dalam gambar"""
    # Read image
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes))
    
    # Detect
    results = waste_detector.predict(image, conf=0.5)
    
    detections = []
    for result in results:
        for box in result.boxes:
            detections.append({
                "class": int(box.cls),
                "confidence": float(box.conf),
                "bbox": box.xyxy[0].tolist()
            })
    
    return {"detections": detections}

@app.post("/classify")
async def classify_waste(file: UploadFile = File(...)):
    """Klasifikasi jenis sampah"""
    # Read and preprocess
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes))
    image = image.resize((224, 224))
    image_array = np.array(image) / 255.0
    image_array = np.expand_dims(image_array, axis=0)
    
    # Predict
    predictions = waste_classifier.predict(image_array)
    class_id = int(np.argmax(predictions))
    confidence = float(np.max(predictions))
    
    return {
        "class": class_id,
        "confidence": confidence
    }

@app.post("/rl_action")
async def get_rl_action(state: dict):
    """Get action dari RL agent"""
    # Convert state to array
    state_array = np.array([
        state['robot_x'],
        state['robot_y'],
        state['battery'],
        state['nearest_waste_x'],
        state['nearest_waste_y']
    ])
    
    # Predict action
    action, _ = rl_agent.predict(state_array, deterministic=True)
    
    action_map = {0: 'north', 1: 'south', 2: 'east', 3: 'west', 4: 'collect'}
    
    return {
        "action": action_map[int(action)],
        "action_id": int(action)
    }
```

### **2. Run API Server**:
```bash
# Install
pip install fastapi uvicorn python-multipart

# Run
uvicorn api_server:app --host 0.0.0.0 --port 8000 --reload
```

---

## **📊 EVALUASI MODEL**

### **1. Waste Detection Metrics**:
```python
from ultralytics import YOLO

# Load model
model = YOLO('waste_detector_v1.pt')

# Evaluate on validation set
metrics = model.val(data='taco.yaml')

print(f"mAP@0.5: {metrics.box.map50}")
print(f"mAP@0.5:0.95: {metrics.box.map}")
print(f"Precision: {metrics.box.mp}")
print(f"Recall: {metrics.box.mr}")
```

### **2. Classification Metrics**:
```python
from sklearn.metrics import classification_report, confusion_matrix

# Get predictions
y_true = []
y_pred = []

for images, labels in val_dataset:
    predictions = waste_classifier.predict(images)
    y_pred.extend(np.argmax(predictions, axis=1))
    y_true.extend(np.argmax(labels, axis=1))

# Report
print(classification_report(y_true, y_pred))
print(confusion_matrix(y_true, y_pred))
```

### **3. RL Performance**:
```python
# Test 100 episodes
total_rewards = []
success_count = 0

for episode in range(100):
    obs = env.reset()
    episode_reward = 0
    done = False
    
    while not done:
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, done, info = env.step(action)
        episode_reward += reward
    
    total_rewards.append(episode_reward)
    if episode_reward > 0:
        success_count += 1

print(f"Average Reward: {np.mean(total_rewards):.2f}")
print(f"Success Rate: {success_count}%")
```

---

## **📝 CHECKLIST PENGEMBANGAN**

### **Phase 1: Waste Detection (Week 1-2)**
- [ ] Download TACO dataset
- [ ] Setup YOLOv8 environment
- [ ] Train detection model (100 epochs)
- [ ] Evaluate mAP >75%
- [ ] Export model for inference

### **Phase 2: Classification (Week 3-4)**
- [ ] Prepare classified dataset
- [ ] Setup ResNet50 transfer learning
- [ ] Train classifier (50 epochs)
- [ ] Evaluate accuracy >85%
- [ ] Export model

### **Phase 3: RL Agent (Week 5-8)**
- [ ] Create custom environment
- [ ] Implement reward function
- [ ] Train DQN agent (500k steps)
- [ ] Test success rate >80%
- [ ] Fine-tune hyperparameters

### **Phase 4: Integration (Week 9-10)**
- [ ] Create FastAPI server
- [ ] Test all endpoints
- [ ] Docker containerization
- [ ] Deploy to cloud
- [ ] Load testing

---

## **🚀 QUICK START COMMANDS**

```bash
# 1. Setup environment
conda create -n sealen python=3.9
conda activate sealen

# 2. Install dependencies
pip install ultralytics tensorflow stable-baselines3 fastapi uvicorn

# 3. Download datasets
git clone https://github.com/pedropro/TACO.git
cd TACO && python3 download.py

# 4. Train detection model
python train_detector.py

# 5. Train classifier
python train_classifier.py

# 6. Train RL agent
python train_rl_agent.py

# 7. Run API server
uvicorn api_server:app --reload
```

---

## **📌 CATATAN PENTING**

1. **GPU Required**: Training membutuhkan GPU (minimal GTX 1060)
2. **Storage**: Minimal 50GB untuk dataset dan models
3. **RAM**: Minimal 16GB
4. **Training Time**: 
   - Detection: ~3-4 jam
   - Classification: ~2-3 jam
   - RL: ~2-4 jam

**Dokumentasi lengkap siap untuk coding agent!** 🚀