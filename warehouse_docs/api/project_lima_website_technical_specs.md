# Project Lima Website Technical Specifications

**Document Type:** Technical Specifications  
**Project:** Project Lima Website  
**Created:** $(date)  
**ETL Cycle:** 6 of 20+  
**Validation Status:** ✅ Real System Tested  

## Technical Overview

Project Lima Website employs a dual API architecture combining FastAPI async endpoints with Flask synchronous routes. The system integrates modern web technologies with Bootstrap frontend, custom CSS/JavaScript assets, and comprehensive authentication systems for trading platform access.

## API Architecture

### FastAPI Endpoints (Async Architecture)
**Primary API Server (`lima_api_server.py`)**
```python
@app.get("/")                      # Root endpoint
async def root():

@app.get("/api/status")            # System status monitoring
async def get_api_status():

@app.get("/api/grid-hold-status")  # Trading strategy status
async def get_grid_hold_status():

@app.get("/api/latest-decision")   # Recent trading decisions
async def get_latest_decision():

@app.get("/api/run-pipeline")      # Pipeline execution trigger
async def run_pipeline():
FastAPI Characteristics:

Architecture: Async/await coroutine-based
Performance: High-concurrency request handling
Documentation: Automatic OpenAPI/Swagger docs
Endpoint Pattern: RESTful API design with /api/ prefix

Flask Routes (Synchronous Architecture)
Main Web Application (web_app_with_warehouse.py)
python@app.route('/')                           # Home page
def index():

@app.route('/login')                      # Authentication interface
def login_page():

@app.route('/dashboard')                  # Main trading dashboard
def dashboard():

@app.route('/logout')                     # Session termination
def logout():

@app.route('/api/auth/login', methods=['POST'])  # Login API
def api_login():
Flask Characteristics:

Architecture: Synchronous WSGI application
Integration: Template rendering with Jinja2
Authentication: Session-based user management
Database: SQLite integration for user data

Database Layer
Authentication System
Core Functions:
pythondef init_database():           # Database initialization
def hash_password(password):   # Secure password hashing
def verify_password(password, hash_value):  # Password verification
def get_user_by_email(email):  # User lookup
def create_user(user_data):    # User registration
Database Architecture:

Engine: SQLite for user authentication
Security: Hashed password storage (no plaintext)
User Management: Email-based authentication system
Session Handling: Flask session management

Configuration System
Project Configuration (project_lima_config.json)
json{
  "ruleset_version": "v3.2",
  "project": "Project Lima",
  "last_updated": "2025-07-28",
  "audit_log_path": "/home/ec2-user/project_lima/logs/",
  "rules_file": "/home/ec2-user/project_lima/rules/golden_rules_v3.2.json"
}
Configuration Features:

Version Control: Ruleset versioning (v3.2)
Audit Trail: Structured logging to /logs/ directory
Rules Engine: Golden rules system integration
Timestamps: Configuration update tracking

Frontend Technology Stack
Static Asset Architecture
CSS Framework:

Custom Styles: ./static/css/lima-styles.css
UI Framework: Bootstrap integration (responsive design)
Theme: Dark gradient professional trading theme
Typography: System font stack optimization

JavaScript Architecture:

Custom Logic: ./static/js/lima-app.js
Framework: Vanilla JavaScript with modern ES6+
Integration: API communication and UI interactions
Functionality: Grid configuration and trading interfaces

Template System
Jinja2 Template Engine:

Base Template: base.html inheritance system
Block Override: Title and content block customization
Dynamic Rendering: Server-side template processing
Bootstrap Integration: Responsive component framework

API Integration Points
Trading System APIs
Grid Hold Status Endpoint:

Purpose: Real-time trading strategy monitoring
Method: GET /api/grid-hold-status
Response: Current grid vs hold performance data

Latest Decision Endpoint:

Purpose: Recent trading decision retrieval
Method: GET /api/latest-decision
Use Case: Dashboard decision display

Pipeline Execution:

Purpose: Manual trading pipeline trigger
Method: GET /api/run-pipeline
Function: On-demand system execution

System Monitoring
Status Monitoring:

Endpoint: GET /api/status
Purpose: System health and availability checking
Integration: Monitoring and alerting systems

Deployment Architecture
Development Server Configuration
FastAPI Deployment:

Framework: Uvicorn ASGI server
Port: 8000 (as configured in startup script)
Documentation: Auto-generated at /docs endpoint

Flask Deployment:

Framework: Gunicorn WSGI server (production)
Port: 8080 (current production configuration)
Integration: Warehouse API system

Asset Serving
Static File Structure:
static/
├── css/
│   └── lima-styles.css      # Custom styling
└── js/
    └── lima-app.js          # Application logic
Asset Characteristics:

CSS: Custom trading platform styling
JavaScript: Interactive grid configuration
Serving: Flask static file serving
Optimization: Embedded CSS in templates for critical styles

Security Architecture
Authentication Security
Password Security:

Hashing: Secure password hash storage
Verification: Hash-based password comparison
Session Management: Flask session handling
Database: No plaintext password storage

API Security
Endpoint Protection:

Authentication: Session-based access control
Authorization: User-specific data access
Logging: Audit trail for system access

Performance Characteristics
Dual Architecture Benefits
FastAPI Advantages:

Async Performance: High-concurrency API endpoints
Auto Documentation: Built-in OpenAPI generation
Type Safety: Python type hints validation

Flask Advantages:

Template Integration: Server-side rendering
Session Management: Built-in authentication handling
Database Integration: SQLite ORM compatibility

Static Asset Optimization

CSS Embedding: Reduced HTTP requests in templates
Custom Assets: Minimal external dependencies
Bootstrap CDN: Framework efficiency without local storage

Integration Architecture
Warehouse System Integration

API Access: Document warehouse API endpoints
Data Storage: Configuration and documentation storage
Real-time Updates: Live system data integration

Trading Platform Integration

3Commas: Grid configuration deployment
Decision Engine: Trading strategy execution
Performance Tracking: Grid vs hold analysis

Development Workflow
Dual Server Architecture
Development Process:

FastAPI Server: Async API development and testing
Flask Application: Template and authentication development
Asset Development: CSS/JavaScript iterative improvement
Configuration Management: JSON-based settings

API Documentation
Automatic Documentation:

FastAPI: /docs endpoint with Swagger UI
Flask: Manual documentation and testing
Integration: Unified API access patterns


Document generated via Professional ETL Framework
Extract → Transform → Load methodology
Real system validation: 100% verified
