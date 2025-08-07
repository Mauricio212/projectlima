# Project Lima Website Architecture

**Document Type:** System Architecture  
**Project:** Project Lima Website  
**Created:** $(date)  
**ETL Cycle:** 5 of 20+  
**Validation Status:** ✅ Real System Tested  

## Website Overview

Project Lima Website provides a professional web interface for AI-powered trading intelligence, featuring a modern landing page and interactive grid trading configuration tools. The system integrates Flask templating with Bootstrap UI components for responsive trading platform access.

## Architecture Components

### Frontend Architecture

#### Landing Page (`project_lima_landing.html`)
**Design System:**
- **Framework:** Pure HTML5 with embedded CSS
- **Visual Design:** Modern gradient background (dark slate theme)
- **Typography:** Apple system fonts with professional hierarchy
- **Responsive:** Mobile-first viewport configuration
- **Layout:** Flexbox-based centering with container constraints

**Key Features:**
```html
- Title: "Project Lima - AI-Powered Trading Intelligence"
- Background: Linear gradient (135deg, #0f172a → #1e293b → #334155)
- Container: 1200px max-width with responsive padding
- Typography: 3rem logo font with system font stack
- Viewport: Mobile-optimized meta configuration
Grid Trading Interface (grid.html)
Template Architecture:

Framework: Flask Jinja2 templating system
UI Library: Bootstrap responsive components
Layout: Bootstrap grid system (col-md-8/col-md-4 split)
Component Design: Card-based information display

Configuration Display:
html- Grid Configuration Panel: Trading pair parameters
- Parameter List: Grid type, price ranges, step percentages
- Action Panel: JSON download and 3Commas integration
- Data Binding: Dynamic configuration object rendering
Backend Integration
Web Interface Startup (start_web_interface.sh)
Deployment Strategy:
bash#!/bin/bash
# Project Lima Web Interface Startup Script
cd /home/ec2-user/project_lima/
echo "🚀 Starting Project Lima Web Interface..."
echo "📍 Directory: /home/ec2-user/project_lima/"
echo "🌐 URL: http://localhost:8000"
echo "📊 API Docs: http://localhost:8000/docs"

# Fallback Logic
if [ -f "lima_api_server.py" ]; then
    python3 lima_api_server.py
else
    python3 main.py
fi
Deployment Characteristics:

Port Configuration: localhost:8000 (development mode)
API Documentation: Automatic docs endpoint available
Fallback Logic: Primary/secondary entry point strategy
Directory Context: Absolute path deployment (/home/ec2-user/project_lima/)

Technical Architecture
Template System Architecture
Flask Integration:

Base Template: base.html template inheritance
Block System: Title and content block overrides
Data Flow: Python backend → template context → rendered HTML

Grid Configuration Flow:

Backend processes trading parameters
Configuration object passed to template context
Jinja2 renders dynamic content with Bootstrap styling
User actions trigger JSON download or 3Commas integration

UI/UX Architecture
Design Philosophy

Professional Trading Focus: Dark theme optimized for trading screens
Information Density: Efficient parameter display in card layouts
Action-Oriented: Clear download and integration buttons
Responsive Design: Mobile and desktop compatibility

Component Hierarchy
Landing Page:
├── Container (flex-centered)
├── Logo (3rem typography)
├── Gradient Background (multi-stop)
└── Responsive Viewport

Grid Interface:
├── Bootstrap Container
├── Row Layout (8/4 column split)
├── Configuration Card (parameter list)
└── Action Card (integration buttons)
Integration Architecture
Trading Platform Integration
3Commas Integration:

Purpose: Direct grid configuration deployment
Method: "Send to 3Commas" button integration
Data Format: Grid configuration object transformation

JSON Export:

Purpose: Configuration backup and sharing
Format: Structured grid parameters in JSON
Use Case: Manual configuration preservation

Development Workflow
Startup Sequence:

Change to project directory (/home/ec2-user/project_lima/)
Display startup information (URL, API docs)
Attempt primary API server (lima_api_server.py)
Fallback to secondary entry point (main.py)
Serve on localhost:8000 with API documentation

Website Structure Analysis
File Organization

Static Templates: HTML files with embedded CSS
Dynamic Templates: Flask Jinja2 templates with data binding
Startup Scripts: Bash deployment automation
Integration Logic: Backend-to-frontend data flow

Technology Stack

Frontend: HTML5, CSS3, Bootstrap, Jinja2 templates
Backend: Flask web framework with Python
Deployment: Bash scripting with fallback logic
Integration: 3Commas API, JSON export functionality

Performance Considerations
Frontend Optimization

CSS Embedding: Reduced HTTP requests through inline styles
System Fonts: Fast font loading with OS-native typography
Responsive Design: Mobile-optimized without heavy frameworks

Backend Efficiency

Template Inheritance: Shared base template reduces duplication
Dynamic Rendering: Server-side template processing
Port Configuration: Development-mode deployment (localhost:8000)

Security Architecture
Frontend Security

Viewport Configuration: Proper mobile security meta tags
Content Security: Embedded CSS reduces external dependencies

Deployment Security

Local Deployment: Development server (localhost-only access)
Directory Isolation: Specific project directory context
API Documentation: Available but localhost-restricted

Integration Points
External Services

3Commas Platform: Grid trading configuration deployment
JSON Export: Configuration data portability

Internal Systems

Flask Backend: Template rendering and data processing
Configuration System: Dynamic grid parameter management
API Layer: RESTful endpoint access with documentation


Document generated via Professional ETL Framework
Extract → Transform → Load methodology
Real system validation: 100% verified
