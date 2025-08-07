# Current System Technical Specifications

**Document Type:** Technical Specifications  
**Project:** Current System (Main Production)  
**Created:** $(date)  
**ETL Cycle:** 2 of 20+  
**Validation Status:** ✅ Real System Tested  

## System Overview

Production Flask application running on AWS EC2 with SQLite database backend, serving personalized trading recommendations and market data through REST API and WebSocket connections.

## API Endpoints

### Core Application Routes
- **GET /** - Home page interface
- **GET /login** - User authentication interface  
- **GET /dashboard** - Main user dashboard
- **GET /logout** - Session termination

### Authentication API
- **POST /api/auth/login** - User authentication endpoint
- **POST /api/auth/register** - New user registration

### Trading API v2
- **GET /api/v2/personalized-recommendations** - User-specific trading suggestions
- **GET /api/v2/market-data** - Real-time market information
- **GET /api/v2/market-summary** - Market overview data

### Real-time Data
- **GET /ws/live-data** - WebSocket endpoint for live market feeds

## Database Schema

### Users Table
```sql
users (
    user_id TEXT PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    working_capital REAL NOT NULL,
    risk_tolerance TEXT NOT NULL,
    trading_experience TEXT NOT NULL,
    email_verified BOOLEAN DEFAULT FALSE,
    verification_token TEXT,
    created_date TEXT NOT NULL,
    last_login TEXT,
    subscription_plan TEXT DEFAULT 'free',
    is_active BOOLEAN DEFAULT TRUE
)
User Settings Table
sqluser_settings (
    user_id TEXT PRIMARY KEY,
    notifications BOOLEAN DEFAULT TRUE,
    auto_execute BOOLEAN DEFAULT FALSE,
    max_position_size INTEGER DEFAULT 25,
    preferred_pairs TEXT DEFAULT '["BTC/USDT","ETH/USDT"]',
    alert_threshold REAL DEFAULT 5.0,
    timezone TEXT DEFAULT 'UTC',
    FOREIGN KEY (user_id) REFERENCES users (user_id)
)
Portfolios Table
sqlportfolios (
    portfolio_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    total_value REAL NOT NULL,
    initial_capital REAL NOT NULL,
    profit_loss REAL NOT NULL,
    active_positions INTEGER DEFAULT 0,
    last_updated TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (user_id)
)
Trading Positions Table
sqltrading_positions (
    position_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    pair TEXT NOT NULL,
    strategy TEXT NOT NULL,
    entry_price REAL NOT NULL,
    position_size REAL NOT NULL,
    current_value REAL,
    profit_loss REAL DEFAULT 0,
    status TEXT DEFAULT 'active',
    opened_date TEXT NOT NULL,
    closed_date TEXT,
    FOREIGN KEY (user_id) REFERENCES users (user_id)
)
Performance History Table
sqlperformance_history (
    record_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    date TEXT NOT NULL,
    portfolio_value REAL NOT NULL,
    daily_return REAL NOT NULL,
    grid_performance REAL,
    hold_performance REAL,
    FOREIGN KEY (user_id) REFERENCES users (user_id)
)
Service Configuration
Gunicorn WSGI Server

Bind Address: 0.0.0.0:8080
Workers: 3 application workers + 1 master process
Timeout: 300 seconds
Keep-alive: 2 seconds
Max Requests: 1000 per worker
Entry Point: wsgi_lima:app

Process Architecture

1 master process managing worker lifecycle
3 worker processes handling HTTP requests
Load balancing across worker processes
Automatic worker recycling after 1000 requests

Data Flow Architecture
User Authentication Flow

User credentials submitted to /api/auth/login
Password hash verification against users table
Session establishment and dashboard redirect
Ongoing session validation for protected routes

Trading Data Pipeline

Market data ingestion (external sources)
Personalized recommendation engine processing
User-specific filtering based on settings table
Real-time delivery via REST API and WebSocket

Performance Tracking

Position data recorded in trading_positions table
Daily performance calculations stored in performance_history
Portfolio value updates maintained in portfolios table
Historical analysis for strategy optimization

Technical Stack Summary

Application Framework: Flask (Python)
WSGI Server: Gunicorn with multi-worker configuration
Database: SQLite with relational schema
Real-time Communication: WebSocket support
API Architecture: RESTful endpoints with versioning (v2)
Authentication: Hash-based password storage with session management
