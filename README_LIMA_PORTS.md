# Project Lima — Port Control (Simple, Stable)

## Purpose
Single source of truth for allowed ports from AWS Security Groups + real-time local usage check.
No fallbacks. No automation unless explicitly approved.

---

## Core Commands

### 1. Show Port Status
Shows:
- **Last AWS refresh (UTC)**
- AWS-allowed ports
- Ports in use locally
- Ports free now

Auto-refreshes AWS master if older than 1 day, or when `--refresh` is passed.

