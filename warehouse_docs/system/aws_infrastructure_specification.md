# AWS Infrastructure Specification

## EC2 Instance Details
- **Public IP**: 52.200.101.103
- **Instance Type**: [Metadata unavailable - likely t3.small based on specs]
- **Region**: us-east-1 (inferred from IP range)
- **Availability Zone**: [Metadata unavailable]
- **Operating System**: Amazon Linux 2023
- **Architecture**: x86_64

## Hardware Specifications
- **CPUs**: 2 cores
- **Memory**: 3.7 GB total (2.9 GB available)
- **Storage**: 16 GB EBS volume (/dev/nvme0n1p1)
- **Usage**: 8.5 GB used, 7.5 GB available (54% utilized)

## Network Configuration
- **Port 80**: HTTP (nginx/web server)
- **Port 443**: HTTPS (SSL/TLS)
- **Port 8080**: Project Lima Flask/Gunicorn (4 workers)
- **Port 6379**: Redis server (localhost only)
- **Port 45203**: Unknown service (localhost only)

## Storage Layout
Filesystem        Size  Used Avail Use%
/dev/nvme0n1p1     16G  8.5G  7.5G  54%
tmpfs             1.9G     0  1.9G   0%

## Operating System
- **Distribution**: Amazon Linux 2023
- **Kernel**: Latest available
- **Package Manager**: yum/dnf

*Last Updated: $(date)*
*Status: Production Active*
