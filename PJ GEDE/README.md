# SEALEN - Marine Cleanup RL System (Project Bundle)

This bundle contains code, test scenarios, and helpers to simulate and train
a Reinforcement Learning agent for a marine waste-collection robot (simulation only).

## What's included
- `data_generator.py` : generate dummy transitions and CSV/json for training
- `env.py` : Gym-like environment wrapper for simulation
- `dqn_agent.py` : simple DQN implementation (PyTorch) and trainer
- `inference_pipeline.py` : glue between detector (YOLO), ResNet classifier, and decision
- `logger.py` : local sqlite logger and optional POST to website endpoint
- `send_to_website.py` : small helper to POST events to your backend
- `test_runner.py` : run short simulation episodes and print JSON lines (string outputs)
- `test_scenarios.json` : five test scenarios you specified
- `requirements.txt` : Python packages (suggested)
- `README.md` : this file

## Notes / Assumptions
- You already have `yolov8n.pt`. Place it in the same folder or change path in `inference_pipeline.py`.
- ResNet50 classifier is provided using torchvision; you should fine-tune it with your labeled crops for good performance.
- The DQN provided is educational and minimal; for production-quality training use stable-baselines3 or tune hyperparameters.
- The `logger.py` will POST to your website if you set environment variable `SEALEN_ENDPOINT` to your endpoint URL.
- The system prints step outputs as JSON strings (see `test_runner.py`) — suitable to be consumed by your backend.

## Backend (website) - suggested endpoints / fields to accept
Backend should provide:
1. POST `/api/events` - accept logs (JSON)
   - payload keys: timestamp, image, detections, decision
2. GET `/api/robot/status` - current robot status (pos, battery, mission_progress, collected_kg)
3. GET `/api/analytics/summary` - aggregated stats for dashboard
4. WebSocket `/ws/updates` - (optional) real-time push of events

## How to run (basic)
1. Create virtualenv, install `requirements.txt`.
2. Optionally run `python data_generator.py` to create training dataset.
3. Train DQN: `python dqn_agent.py` (or use `test_runner.py` which trains a small model if none found).
4. For inference put sample image `sample_frame.jpg` and run `python inference_pipeline.py`.

## Deliverable
A zip file in this bundle: `sealen_project_bundle.zip`
