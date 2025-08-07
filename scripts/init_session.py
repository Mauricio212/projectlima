# scripts/init_session.py

from load_config_and_secrets import load_all_configs
from validate_config import run_validation
import os
import json
from datetime import datetime

def load_last_session():
    try:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        last_state_path = os.path.join(base_path, 'logs', 'last_state.json')
        if os.path.exists(last_state_path):
            with open(last_state_path, 'r') as f:
                state = json.load(f)
            return state
    except Exception as e:
        print(f"⚠️ Could not load last session state: {e}")
    return {}

def main():
    print("🔵 Initializing Project Lima Session...\n")

    # Step 1: Validate configs
    run_validation()

    # Step 2: Load configs
    config = load_all_configs()

    # Step 3: Load last session memory
    last_session = load_last_session()

    print("\n🔵 Context Loaded Successfully:")
    print(f"- EC2 Public IP: {config.get('ec2_public_ip')}")
    print(f"- Server User: {config.get('server_user')}")
    print(f"- Deployment Bucket: {config.get('deployment_bucket')}")
    print(f"- Last Session: {last_session.get('last_session', 'N/A')}")
    print(f"- Last Pending Task: {last_session.get('pending_task', 'None')}\n")

    print("✅ Project Lima Session Bootstrap Complete.\n")

if __name__ == "__main__":
    main()
