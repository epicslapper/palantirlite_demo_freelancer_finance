import yaml

def load_models(path="models.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)
