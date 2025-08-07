# Flask API Endpoints Reference

## Authentication Endpoints
- **POST /api/auth/login** - User authentication
- **POST /api/auth/register** - User registration
- **GET /logout** - User logout

## Trading Data Endpoints
- **GET /api/v2/personalized-recommendations** - User-specific trading recommendations
- **GET /api/v2/market-data** - Current market data
- **GET /api/v2/market-summary** - Market overview summary

## WebSocket Endpoints
- **GET /ws/live-data** - Real-time trading data stream

## Web Interface Routes
- **GET /** - Landing page
- **GET /login** - Login interface
- **GET /dashboard** - User dashboard

## Current Server Configuration
- **Framework**: Flask with session-based authentication
- **Database**: SQLite (lima_trading.db)
- **Service**: Gunicorn on port 8080
- **Authentication**: Session cookies with secret key

*Last Updated: $(date)*
*Status: Production Active*
