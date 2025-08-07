# Infrastructure Overview

> **Project Lima – Personal AI Financial System**  
> Document Category: `01 system architecture`  
> Created: 2025-07-29  
> Maintainer: ChatGPT (Document Creator), Claude 4 Sonnet (Validator)

---

## 🧭 Purpose

This document outlines the high-level infrastructure design for Project Lima, including server environment, file structure, cloud components, and system boundaries. It ensures stability, scalability, and clarity for future maintenance and AI interaction.

---

## 🏗️ Structure

Project Lima runs on a single AWS EC2 instance with the following layout:

- **Server**: Amazon EC2, public IP `52.200.101.103`, Ubuntu 22.04 LTS
- **App Layer**: FastAPI app exposed on port 8001
- **Storage**: Local persistent disk (`~/project_lima/`)
- **Web Interface**: HTML + Markdown rendered documents
- **Data Input**: AI-generated `.md`, `.csv`, and `.txt` files
- **File Hierarchy**:
  - `warehouse/` – Structured documentation
  - `scripts/` – Operational tools (pipeline, logger, validator)
  - `logs/` – Execution and error tracking
- **Users**: Single admin operator + AI collaborators (ChatGPT + Claude)

---

## 🛡️ Golden Rule Alignment

This design follows Golden Rule v3.2 by enforcing:

- Simplicity: No microservices, no dockerized overload
- Local-first: No external storage dependencies
- 1-server max: Fully functional on one EC2 node
- Logical separation: Files, code, logs, and scripts are sandboxed
- Human-AI clarity: Directory structure maps directly to human and Claude workflows

---

## 🔁 Interdependencies

This doc governs or is referenced by:

- `deployment_procedures.md`
- `security_framework.md`
- `project_lima_overview.md`
- `run_project_lima_pipeline.py`

---

## 🛠️ Execution Examples

```bash
# Start the FastAPI backend
uvicorn main:app --host 0.0.0.0 --port 8001

# View warehouse
tree ~/project_lima/warehouse
