# Deployment Guide

This guide covers various deployment options for OpenSite Analytics.

## Docker Deployment (Recommended)

### Quick Start

```bash
# Clone the repository
git clone <repository-url>
cd opensite-site-traking

# Build and start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Development Mode

For development with hot reload:

```bash
docker-compose -f docker-compose.dev.yml up -d
```

### Production Docker

For production deployment:

1. Update environment variables in `docker-compose.yml`:
   - Change `SECRET_KEY` to a strong random value
   - Update `CORS_ORIGINS` to your production domain
   - Consider using PostgreSQL instead of SQLite

2. Build and deploy:
```bash
docker-compose -f docker-compose.yml up -d --build
```

## Manual Deployment

### Backend

#### System Requirements
- Python 3.9+
- pip
- Virtual environment (recommended)

#### Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Set environment variables
export DATABASE_URL=sqlite:///./analytics.db
export SECRET_KEY=your-secret-key
export CORS_ORIGINS=https://your-domain.com

# Initialize database
cd backend
python3 init_db.py

# Run with gunicorn (production)
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

#### Systemd Service

Create `/etc/systemd/system/opensite-analytics.service`:

```ini
[Unit]
Description=OpenSite Analytics Backend
After=network.target

[Service]
Type=notify
User=analytics
WorkingDirectory=/path/to/opensite-site-traking/backend
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable opensite-analytics
sudo systemctl start opensite-analytics
```

### Frontend

#### System Requirements
- Node.js 18+
- npm

#### Setup

```bash
# Install dependencies
cd frontend
npm install

# Build for production
npm run build

# Start production server
npm start
```

#### Nginx Configuration

```nginx
server {
    listen 80;
    server_name analytics.yourdomain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /ws {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```

### PostgreSQL Setup (Optional)

For production, use PostgreSQL instead of SQLite:

1. Install PostgreSQL:
```bash
sudo apt-get install postgresql postgresql-contrib
```

2. Create database:
```sql
CREATE DATABASE opensite_analytics;
CREATE USER analytics WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE opensite_analytics TO analytics;
```

3. Update environment variable:
```bash
export DATABASE_URL=postgresql://analytics:secure_password@localhost/opensite_analytics
```

## Cloud Deployment

### Vercel (Frontend)

1. Connect your repository to Vercel
2. Set environment variable: `NEXT_PUBLIC_API_URL`
3. Deploy

### Railway / Render (Backend)

1. Connect repository
2. Set environment variables
3. Deploy

### AWS

#### EC2

1. Launch EC2 instance
2. Install Docker
3. Clone repository
4. Run `docker-compose up -d`
5. Configure load balancer and SSL

#### ECS/Fargate

1. Create ECS cluster
2. Push Docker images to ECR
3. Create task definitions
4. Deploy services

## Security Considerations

1. **HTTPS**: Always use HTTPS in production
2. **Secrets**: Never commit `.env` files
3. **Firewall**: Restrict database access
4. **Updates**: Keep dependencies updated
5. **Backups**: Regular database backups
6. **Rate Limiting**: Configure appropriate rate limits
7. **CORS**: Restrict to your domains only

## Monitoring

### Health Checks

- Backend: `GET /health`
- Dashboard: Check frontend is accessible

### Logs

```bash
# Docker logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Systemd logs
sudo journalctl -u opensite-analytics -f
```

### Metrics

Consider adding:
- Prometheus metrics
- Grafana dashboards
- Error tracking (Sentry)

## Backup Strategy

### SQLite Backup

```bash
# Backup
cp analytics.db analytics.db.backup

# Automated backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
cp /path/to/analytics.db /backups/analytics_$DATE.db
find /backups -name "analytics_*.db" -mtime +30 -delete
```

### PostgreSQL Backup

```bash
pg_dump opensite_analytics > backup.sql
```

## Scaling

### Horizontal Scaling

- Use load balancer for multiple backend instances
- Use PostgreSQL for shared database
- Configure Redis for session management (if needed)

### Vertical Scaling

- Increase server resources
- Optimize database queries
- Add database indexes

## Troubleshooting

### Database Locked

- Ensure only one backend process is running
- Use PostgreSQL for production
- Check file permissions

### WebSocket Connection Failed

- Check firewall rules
- Verify reverse proxy WebSocket configuration
- Check CORS settings

### High Memory Usage

- Limit WebSocket connections
- Implement data retention
- Optimize database queries
