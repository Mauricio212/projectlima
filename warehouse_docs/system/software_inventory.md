# Software Inventory & Environment

## Python Environment
- **Version**: Python 3.9 (virtual environment: lima_env)
- **Location**: /home/ec2-user/project_lima/lima_env/
- **Package Manager**: pip
- **Key Packages**: Flask, Gunicorn, SQLite3

## System Software
- **Operating System**: Amazon Linux 2023
- **Web Servers**: nginx/Apache (ports 80/443)
- **Application Server**: Gunicorn (port 8080)
- **Database**: SQLite (lima_trading.db)
- **Cache**: Redis (port 6379)

## Project Lima Application Stack
- **Main Application**: web_app_professional_secured.py.modal_backup
- **WSGI Configuration**: wsgi_lima.py
- **Document Warehouse**: warehouse_api.py (fully operational)
- **Database**: SQLite with user management and trading data
- **Authentication**: Session-based with API key for warehouse

## Development Tools
- **Version Control**: File-based backups
- **Deployment**: Manual deployment with Gunicorn restart
- **Monitoring**: Log files (app.log, gunicorn.log)
- **Backup**: Multiple application versions maintained

## Directory Structure
/home/ec2-user/project_lima/
├── lima_env/                 # Python virtual environment
├── warehouse_docs/           # Document warehouse (6 documents)
├── wsgi_lima.py             # Production WSGI config
├── web_app_*.py             # Flask applications
├── lima_trading.db          # SQLite database
├── warehouse_api.py         # Document warehouse API
└── static/, templates/      # Web assets

*Last Updated: $(date)*
*Inventory Status: Complete*
