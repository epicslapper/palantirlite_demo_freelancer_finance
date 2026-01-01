# check_yaml.py
from engine.model_loader import load_models

# Load the models.yaml
models = load_models()

# Print the result
print("Loaded models.yaml:")
print(models)
