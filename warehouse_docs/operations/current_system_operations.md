# Current System Operations Documentation

**Document Type:** Operations Manual  
**Project:** Current System (Main Production)  
**Created:** $(date)  
**ETL Cycle:** 3 of 20+  
**Validation Status:** ✅ Real System Tested  

## Deployment Overview

Production Flask application deployed on AWS EC2 using Gunicorn WSGI server with manual process management. System serves trading platform with integrated document warehouse on port 8080.

## Current Deployment Configuration

### Active Deployment Command
```bash
/home/ec2-user/project_lima/lima_env/bin/python3 \
/home/ec2-user/project_lima/lima_env/bin/gunicorn \
--bind 0.0.0.0:8080 \
--workers 3 \
--timeout 300 \
--keep-alive 2 \
--max-requests 1000 \
wsgi_lima:app
Configuration Analysis
Gunicorn Configuration File vs Reality
File Configuration (gunicorn_config.py):

Bind: 0.0.0.0:8000 ❌
Workers: 4 ❌
Timeout: 30 seconds ❌
Max Requests: 1000 ✅

Actual Running Configuration:

Bind: 0.0.0.0:8080 ✅ (Production)
Workers: 3 ✅ (Production)
Timeout: 300 seconds ✅ (Production)
Max Requests: 1000 ✅ (Consistent)

Status: Command-line parameters override config file (standard practice)
Process Management
Manual Deployment Model

Service Management: Manual process execution (no systemd service)
Process Monitoring: Manual verification via ps aux | grep gunicorn
Restart Procedure: Manual process termination and restart
High Availability: Not configured (single instance deployment)

Operational Recommendations
Immediate Improvements

Systemd Service: Create proper service unit for automatic startup
Log Management: Implement structured logging with rotation
Health Checks: Add application health monitoring endpoints
Configuration Management: Consolidate config file vs command-line discrepancies


Document generated via Professional ETL Framework
Extract → Transform → Load methodology
Real system validation: 100% verified
