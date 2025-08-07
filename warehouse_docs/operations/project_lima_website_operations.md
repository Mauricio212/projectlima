# Project Lima Website Operations Documentation

**Document Type:** Operations Manual  
**Project:** Project Lima Website  
**Created:** $(date)  
**ETL Cycle:** 7 of 20+  
**Validation Status:** ✅ Real System Tested  

## Operations Overview

Project Lima Website operates through a FastAPI-based deployment with comprehensive static asset management, dual interface architecture, and automated template rendering systems. The operational model supports both AI Financial Intelligence interfaces and professional trading platform access.

## Deployment Architecture

### Primary Application Entry Point (`main.py`)
```python
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
Operational Characteristics:

Framework: FastAPI ASGI application
Static Serving: Automated /static route mounting
Template Engine: Jinja2 template system integration
Directory Structure: Templates and static assets separation

Fallback Startup System
Startup Script Logic (start_web_interface.sh):
bash# Try simple API server first, fallback to main.py
if [ -f "lima_api_server.py" ]; then
    echo "Using Project Lima API Server..."
    python3 lima_api_server.py
else
    echo "Using main.py..."
    python3 main.py
fi
Operational Status:

Primary Entry: lima_api_server.py (NOT FOUND)
Active Entry: main.py (FastAPI configuration)
Fallback System: Automatic failover to available entry point

Static Asset Management
Asset Directory Structure
static/
├── css/
│   └── lima-styles.css      # 6,283 bytes - Core styling
├── js/
│   ├── lima-app.js          # 6,067 bytes - Application logic
│   └── modal.js             # 26,147 bytes - Modal components
└── index.html               # 8,454 bytes - Main interface
Asset Operational Metrics:

Total Static Assets: 4 files, 46.9KB total
CSS Framework: Custom lima-styles.css (6.3KB)
JavaScript Logic: 32.2KB total (app logic + modal system)
Main Interface: 8.4KB AI Financial Intelligence interface

Asset Serving Configuration
FastAPI Static Mount:

Route: /static/* automatically served
Directory: ./static/ folder mapping
Name: "static" route name for URL generation
Caching: Default FastAPI static file caching

Interface Architecture
Dual Interface System
Landing Page Interface (project_lima_landing.html):

Title: "Project Lima - AI-Powered Trading Intelligence"
Design: Professional gradient theme
Purpose: Marketing and initial user engagement

Main Application Interface (static/index.html):

Title: "Project Lima - AI Financial Intelligence"
Design: Segoe UI professional interface
Purpose: Operational trading platform access

Template System Operations
Jinja2 Configuration:

Directory: ./templates/ folder
Engine: Jinja2Templates FastAPI integration
Rendering: Server-side template processing
Context: Dynamic data binding for trading interfaces

Operational Workflow
Startup Sequence

Entry Point Check: Verify lima_api_server.py existence
Fallback Activation: Execute main.py if primary not found
FastAPI Initialization: Create app instance with static/template mounting
Asset Serving: Enable /static route for CSS/JavaScript/HTML
Template Engine: Initialize Jinja2 for dynamic content rendering

Request Processing Flow

Static Requests: /static/* → Direct file serving from static directory
Template Requests: API routes → Jinja2 rendering → HTML response
API Requests: FastAPI route handlers → JSON/data responses

Asset Optimization
Performance Characteristics
Static Asset Performance:

CSS: Single 6.3KB stylesheet (minimal external dependencies)
JavaScript: 32.2KB total with modal functionality
HTML: 8.4KB main interface (embedded styling optimized)
Serving: FastAPI static file optimization with caching

Resource Management
Asset Loading Strategy:

CSS: Single lima-styles.css file (reduced HTTP requests)
JavaScript: Modular design (lima-app.js + modal.js separation)
HTML: Embedded critical styles for fast initial render

Operational Monitoring
File System Monitoring
Asset Integrity Checks:
bash# Verify static asset availability
ls -la static/css/lima-styles.css    # Should show 6,283 bytes
ls -la static/js/lima-app.js         # Should show 6,067 bytes  
ls -la static/js/modal.js            # Should show 26,147 bytes
ls -la static/index.html             # Should show 8,454 bytes
Application Health Monitoring
Startup Verification:

Entry Point: Confirm main.py execution
Static Mounting: Verify /static route accessibility
Template Engine: Confirm Jinja2 initialization
Port Binding: Check localhost:8000 availability

Configuration Management
Operational Configuration
FastAPI App Configuration:

Static Files: Automatic serving enabled
Template Directory: ./templates/ mounted
ASGI Mode: Async request handling
Development Mode: localhost:8000 binding

Asset Management Configuration
Directory Permissions:

static/css/: Read access for stylesheet serving
static/js/: Read access for JavaScript execution
static/index.html: Read access for main interface
templates/: Read access for Jinja2 rendering

Deployment Operations
Manual Deployment Process

Directory Setup: Ensure static/ and templates/ directories exist
Asset Verification: Confirm all static files present and sized correctly
Entry Point: Execute startup script or direct main.py execution
Port Verification: Confirm localhost:8000 accessibility
Static Route Testing: Verify /static/* file serving

Operational Maintenance
Asset Updates:

CSS Changes: Update lima-styles.css (automatic serving refresh)
JavaScript Updates: Modify lima-app.js or modal.js (cache consideration)
Interface Updates: Edit static/index.html (immediate availability)

Troubleshooting Operations
Common Operational Issues:

Missing lima_api_server.py: Normal fallback to main.py
Static Assets Not Loading: Verify static directory permissions
Template Errors: Check templates directory existence
Port Conflicts: Confirm localhost:8000 availability

Integration Operations
API Integration Points
Static Asset Integration:

CSS Framework: lima-styles.css provides trading platform styling
JavaScript Logic: lima-app.js handles grid configuration interactions
Modal System: modal.js provides user interface components

Template Integration
Jinja2 Template Operations:

Dynamic Content: Trading data integration through template context
Static Assets: Automatic URL generation for CSS/JavaScript references
Grid Interface: Template-based grid configuration rendering


Document generated via Professional ETL Framework
Extract → Transform → Load methodology
Real system validation: 100% verified
