# scripts/validate_config.py

import yaml
import os
import sys

REQUIRED_CONFIG_KEYS = [
    "ec2_public_ip",
    "server_user",
    "ssh_key_path",
    "deployment_bucket"
]

REQUIRED_SECRETS_KEYS = [
    "aws_access_key_id",
    "aws_secret_access_key",
    "database_password",
    "openai_api_key"
]

def validate_yaml_file(filepath, required_keys):
    try:
        with open(filepath, 'r') as f:
            data = yaml.safe_load(f)
    except Exception as e:
        print(f"❌ Error reading {filepath}: {e}")
        sys.exit(1)

    missing = [key for key in required_keys if key not in data]
    if missing:
        print(f"❌ Missing keys in {filepath}: {missing}")
        sys.exit(1)
    else:
        print(f"✅ {filepath} validated successfully.")

def run_validation():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_path, 'config', 'config.yml')
    secrets_path = os.path.join(base_path, 'config', 'secrets.yml')

    validate_yaml_file(config_path, REQUIRED_CONFIG_KEYS)
    validate_yaml_file(secrets_path, REQUIRED_SECRETS_KEYS)

if __name__ == "__main__":
    run_validation()
