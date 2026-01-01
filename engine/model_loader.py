# engine/model_loader.py

import yaml
from pathlib import Path

MODEL_FILE = Path(__file__).parent / "models.yaml"

def load_models():
    with open(MODEL_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
