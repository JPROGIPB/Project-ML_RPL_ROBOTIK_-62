"""
Inference pipeline (updated):
- Load YOLO detection model (prefer `yolov11n.pt`, fallback to `yolov8n.pt`)
- Optionally use a classifier; if `classifier` is None the pipeline will only use YOLO detections
- Produce a simple decision (heuristic or DQN if provided)
- Log events via `Logger`
"""
import os
import time
import json
import numpy as np

# detection: uses ultralytics if installed. The repo may contain yolov11n.pt or yolov8n.pt
try:
    from ultralytics import YOLO
    yolo_available = True
except Exception:
    YOLO = None
    yolo_available = False

import torch
from PIL import Image

from logger import Logger
from dqn_agent import QNet


def load_detector(weights_path=None):
    """Load YOLO detector. If weights_path is None, prefer `yolov11n.pt` then `yolov8n.pt`.
    Returns None if ultralytics not available.
    """
    if not yolo_available:
        print("ultralytics YOLO not installed. Detection will be mocked.")
        return None
    if weights_path is None:
        if os.path.exists("yolov11n.pt"):
            weights_path = "yolov11n.pt"
        elif os.path.exists("yolov8n.pt"):
            weights_path = "yolov8n.pt"
        else:
            # user-provided weights not found, let ultralytics load default if it accepts
            weights_path = "yolov8n.pt"
    model = YOLO(weights_path)
    return model


def infer_frame(image_path, detector=None, classifier=None, device=None, dqn_model=None):
    """
    Run detection (required) and optionally DQN decision.

    - `detector`: YOLO model or None (mock)
    - `classifier`: not used when None. If provided, crops will be classified.
    - `device`: torch device used for classifier/DQN (optional)
    - `dqn_model`: QNet or None

    Returns decision dict.
    """
    logger = Logger()
    detections = []

    img = Image.open(image_path).convert('RGB')
    img_w, img_h = img.size

    if detector is None:
        # MOCK detection: pretend one box at center
        detections = [{'xyxy': [50, 50, 150, 150], 'conf': 0.8, 'class': 'waste'}]
        if classifier is not None:
            crop = img.crop((50, 50, 150, 150))
            try:
                with torch.no_grad():
                    x = _transform(crop).unsqueeze(0).to(device)
                    out = classifier(x)
                    pred = int(out.argmax(1)[0].cpu().numpy())
                    detections[0]['type'] = pred
            except Exception:
                detections[0]['type'] = None
    else:
        # detector(image_path) returns Results; handle both single result and iterable
        try:
            results = detector(image_path)
        except Exception as e:
            print("Detector failed to run:", e)
            results = []

        # results can be list-like; iterate
        for res in results:
            # each res has .boxes; boxes may have xyxy, conf, cls
            boxes = getattr(res, 'boxes', [])
            # confidence threshold to filter weak detections
            conf_thresh = 0.3
            for b in boxes:
                try:
                    # ultralytics box fields vary; try multiple ways
                    xy = None
                    conf = None
                    cls_id = None
                    label = None
                    if hasattr(b, 'xyxy'):
                        arr = b.xyxy.cpu().numpy().astype(float)
                        # xyxy may be (N,4); take first if necessary
                        if arr.ndim == 2:
                            arr = arr[0]
                        xy = [int(arr[0]), int(arr[1]), int(arr[2]), int(arr[3])]
                    # use .item() to extract scalar safely and avoid numpy deprecation
                    if hasattr(b, 'conf'):
                        try:
                            conf = float(b.conf.cpu().item())
                        except Exception:
                            # fallback if item() not available
                            conf = float(b.conf.cpu().numpy().ravel()[0])
                    elif hasattr(b, 'confidence'):
                        try:
                            conf = float(b.confidence.cpu().item())
                        except Exception:
                            conf = float(b.confidence.cpu().numpy().ravel()[0])
                    if hasattr(b, 'cls'):
                        try:
                            cls_id = int(b.cls.cpu().item())
                        except Exception:
                            try:
                                cls_id = int(b.cls.cpu().numpy().ravel()[0])
                            except Exception:
                                cls_id = None

                    # try to resolve label name from result if available
                    if cls_id is not None and hasattr(res, 'names'):
                        try:
                            names = res.names
                            if isinstance(names, dict):
                                label = names.get(cls_id, None)
                            else:
                                label = names[cls_id]
                        except Exception:
                            label = None

                    # apply confidence threshold and round confidence for readability
                    if conf is not None and conf >= conf_thresh:
                        det_entry = {'xyxy': xy, 'conf': round(conf, 3), 'class_id': cls_id, 'label': label}
                        # no classifier in this workflow per user note
                        detections.append(det_entry)
                except Exception:
                    continue

    # Make decision: try to use DQN if provided, otherwise heuristic
    decision = {"action": "idle", "reason": "no model"}

    def _detections_to_state(detections, img_w, img_h, grid_size=100):
        """Convert detections (list of det_entry) to a SealenEnv-like state vector.

        Strategy (simple heuristic):
        - robot assumed at center of environment (grid_size/2, grid_size/2)
        - battery assumed 80.0
        - nearest waste chosen as the detection with highest confidence
        - map image pixel coordinates to environment grid by linear scaling
        - mission_progress set to 0.0 (unknown)
        """
        if not detections:
            # no detection -> return a default 'empty' state
            return np.array([grid_size/2, grid_size/2, 80.0, 0.0, 0.0, float(grid_size), 0.0], dtype=np.float32)

        # choose detection with max confidence
        best = max(detections, key=lambda d: d.get('conf', 0.0))
        xy = best.get('xyxy')
        if not xy:
            # fallback
            return np.array([grid_size/2, grid_size/2, 80.0, 0.0, 0.0, float(grid_size), 0.0], dtype=np.float32)

        # centroid in pixel coords
        x1, y1, x2, y2 = xy
        cx = (x1 + x2) / 2.0
        cy = (y1 + y2) / 2.0

        # map to grid scale
        gx = (cx / max(1, img_w)) * (grid_size - 1)
        gy = (cy / max(1, img_h)) * (grid_size - 1)

        rx = grid_size / 2.0
        ry = grid_size / 2.0
        battery = 80.0
        dist = float(((rx - gx) ** 2 + (ry - gy) ** 2) ** 0.5)
        progress = 0.0
        return np.array([rx, ry, battery, gx, gy, dist, progress], dtype=np.float32)

    if dqn_model is not None:
        # build state from detections and call DQN
        state = _detections_to_state(detections, img_w, img_h, grid_size=100)
        s = torch.tensor(state, dtype=torch.float32).unsqueeze(0)
        s = s.to(device) if device is not None else s
        with torch.no_grad():
            out = dqn_model(s).cpu().numpy()[0]
            act = int(out.argmax())
        mapping = {0: 'North', 1: 'South', 2: 'East', 3: 'West', 4: 'Collect', 5: 'ReturnHome'}
        decision = {"action": mapping.get(act, 'idle'), "raw_action": act, "state_used": state.tolist(), "detections": detections}
    else:
        if detections:
            decision = {"action": "Collect", "reason": "detected_waste", "detections": detections}

    # send log
    logger.log_event({
        'timestamp': time.time(),
        'image': os.path.basename(image_path),
        'detections': detections,
        'decision': decision
    })
    return decision


def print_human_readable(image_path, decision):
    """Cetak ringkasan hasil inference dalam Bahasa Indonesia."""
    action = decision.get('action', 'idle')
    dets = decision.get('detections', []) or []
    n = len(dets)

    # map action ke bahasa Indonesia
    action_map = {
        'Collect': 'Ambil sampah',
        'ReturnHome': 'Kembali ke base',
        'North': 'Gerak Utara',
        'South': 'Gerak Selatan',
        'East': 'Gerak Timur',
        'West': 'Gerak Barat',
        'idle': 'Diam'
    }
    action_text = action_map.get(action, action)

    print(f"Gambar: {os.path.basename(image_path)}")
    if n == 0:
        print("Hasil: Tidak ada objek terdeteksi.")
        print(f"Keputusan sistem: {action_text}")
        return

    # kumpulkan ringkasan label jika ada
    labels = []
    for d in dets:
        lbl = d.get('label') if isinstance(d.get('label'), str) else None
        if not lbl:
            cid = d.get('class_id')
            lbl = f"class_{cid}" if cid is not None else 'unknown'
        labels.append(lbl)

    # hitung frekuensi sederhana
    freq = {}
    for l in labels:
        freq[l] = freq.get(l, 0) + 1

    # ringkasan singkat
    summary_parts = [f"{v} {k}" for k, v in freq.items()]
    print(f"Hasil: {n} objek terdeteksi — {', '.join(summary_parts)}.")
    print(f"Keputusan sistem: {action_text}")

    # detail tiap deteksi
    for i, d in enumerate(dets, start=1):
        lbl = labels[i-1]
        conf = d.get('conf')
        bbox = d.get('xyxy')
        try:
            conf_pct = f"{float(conf)*100:.1f}%" if conf is not None else "n/a"
        except Exception:
            conf_pct = str(conf)
        print(f"Deteksi {i}: {lbl}, confidence {conf} ({conf_pct}), kotak {bbox}")



if __name__ == "__main__":
    # set up detector (prefer yolov11n.pt if present)
    det = load_detector()
    # Not using classifier per user request; set to None
    clf = None
    dev = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    dqn = None
    # try to load dqn if exists (optional)
    if os.path.exists("dqn_sealen.pth"):
        try:
            dq = QNet()
            dq.load_state_dict(torch.load("dqn_sealen.pth", map_location=dev))
            dq.to(dev)
            dq.eval()
            dqn = dq
        except Exception:
            dqn = None

    sample = "sample_frame.jpg"
    if os.path.exists(sample):
        decision = infer_frame(sample, det, clf, dev, dqn)
        print_human_readable(sample, decision)
    else:
        print("Place a sample_frame.jpg in folder to run inference demo.")
