# Service Configuration Documentation

## Primary Services
### Project Lima Flask Application
- **Service**: Gunicorn WSGI server
- **Workers**: 4 processes
- **Port**: 8080
- **Process ID**: 2523868 (master)
- **Configuration**: wsgi_lima:app
- **Status**: Active and responding

### Web Server (Port 80/443)
- **Service**: Unknown web server
- **Ports**: 80 (HTTP), 443 (HTTPS)
- **Status**: Listening
- **Purpose**: Likely nginx or Apache frontend

### Redis Cache
- **Service**: Redis server
- **Port**: 6379 (localhost only)
- **Purpose**: Caching/session storage
- **Status**: Active

## Process Management
- **Python Environment**: lima_env (Python 3.9)
- **Application Directory**: /home/ec2-user/project_lima/
- **Log Files**: app.log, gunicorn.log

## Security Configuration
- **Firewall**: Default AWS security groups
- **Access Control**: SSH key-based authentication
- **Application Security**: API key authentication for warehouse

*Last Updated: $(date)*
*Status: All services operational*
