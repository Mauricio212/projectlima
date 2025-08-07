#!/usr/bin/env python3

import json
import os
import datetime

# ====== CONFIGURATION ======
RULE_VERSION = "v3.2"
CONFIG_PATH = os.path.expanduser("~/project_lima/project_lima_config.json")
RULE_FILE = os.path.expanduser("~/project_lima/rules/golden_rules_v3.2.json")
EXPECTED_HASH = "38f659571e704f316d04985b0326e61524dc035034c96c5a4c82a2bce0451977"

# ====== BLAKE3 HASHING ======
def calculate_blake3(filepath):
    try:
        import blake3
    except ImportError:
        print("❌ blake3 module not installed. Run: pip3 install --user blake3")
        raise SystemExit(1)

    h = blake3.blake3()
    try:
        with open(filepath, "rb") as f:
            while chunk := f.read(8192):
                h.update(chunk)
        return h.hexdigest()
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        raise SystemExit(1)

# ====== MAIN VERIFICATION ======
def verify_ruleset():
    try:
        with open(CONFIG_PATH, "r") as f:
            config = json.load(f)

        assert config.get("ruleset_version") == RULE_VERSION, f"Config version mismatch: expected {RULE_VERSION}, got {config.get('ruleset_version')}"

        actual_hash = calculate_blake3(RULE_FILE)
        assert actual_hash == EXPECTED_HASH, f"Rule hash mismatch.\nExpected: {EXPECTED_HASH}\nFound:    {actual_hash}"

        print(f"✅ Golden Rules {RULE_VERSION} verified and trusted.")
        print(f"🔒 Hash match: {actual_hash}")
        print(f"📅 Verification time: {datetime.datetime.now().isoformat()}")

    except AssertionError as ae:
        print(f"❌ Verification failed: {ae}")
        raise SystemExit(1)
    except Exception as ex:
        print(f"❌ Fatal error: {ex}")
        raise SystemExit(1)

if __name__ == "__main__":
    verify_ruleset()
