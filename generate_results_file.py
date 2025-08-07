# generate_results_file.py — Project Lima Verified Output Script
# ✅ Golden Rule Compliant

import os
import pandas as pd
from datetime import datetime

# === Data to Save ===
sample_data = [
    {"token": "ETH", "score": 0.87},
    {"token": "BTC", "score": 0.81},
    {"token": "LINK", "score": 0.79},
]

df = pd.DataFrame(sample_data)

# === Output Configuration ===
output_dir = os.path.expanduser("~/project_lima/results")
os.makedirs(output_dir, exist_ok=True)

timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
filename = f"final_output_{timestamp}.csv"
output_path = os.path.join(output_dir, filename)

# === Save File (Overwrite Safe) ===
df.to_csv(output_path, index=False)

print(f"[✅] File successfully created: {output_path}")
