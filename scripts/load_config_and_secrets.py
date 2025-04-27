# scripts/load_config_and_secrets.py

import yaml
import os

def load_yaml(filepath):
    with open(filepath, 'r') as f:
        return yaml.safe_load(f)

def load_all_configs():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_path, 'config', 'config.yml')
    secrets_path = os.path.join(base_path, 'config', 'secrets.yml')
    
    config = load_yaml(config_path)
    secrets = load_yaml(secrets_path)

    full_config = {**config, **secrets}  # Merge both dictionaries
    return full_config
