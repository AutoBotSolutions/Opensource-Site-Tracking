# Deployment Guide

This guide covers deploying OpenSite Analytics to production.

## Prerequisites

- A server with SSH access
- Domain name configured
- SSL certificate (recommended)
- PostgreSQL or MySQL (recommended for production)

## Deployment Options

### Option 1: Docker Deployment (Recommended)

#### 1. Create Docker Compose File

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/opensite
      - SECRET_KEY=${SECRET_KEY}
      - CORS_ORIGINS=["https://yourdomain.com"]
    depends_on:
      - db
    volumes:
      - ./backend:/app
    command: uvicorn main:app --host 0.0.0.0 --port 8000

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=https://api.yourdomain.com
    depends_on:
      - backend

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=opensite
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

#### 2. Create Backend Dockerfile

Create `backend/Dockerfile`:

```dockerfile
FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### 3. Create Frontend Dockerfile

Create `frontend/Dockerfile`:

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]
```

#### 4. Deploy with Docker Compose

```bash
docker-compose up -d
```

### Option 2: Manual Deployment

#### Backend Deployment

1. Set up the server:

```bash
ssh user@your-server.com
```

2. Install dependencies:

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv postgresql nginx
```

3. Clone the repository:

```bash
git clone https://github.com/yourusername/opensource-site-tracking.git
cd opensource-site-tracking/backend
```

4. Set up virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

5. Set up PostgreSQL:

```bash
sudo -u postgres psql
CREATE DATABASE opensite;
CREATE USER opensite_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE opensite TO opensite_user;
\q
```

6. Configure environment variables:

```bash
cp .env.example .env
nano .env
```

Update with production values:

```env
DATABASE_URL=postgresql://opensite_user:secure_password@localhost/opensite
SECRET_KEY=your-production-secret-key
CORS_ORIGINS=["https://yourdomain.com"]
```

7. Initialize database:

```bash
python3 init_db.py
```

8. Set up systemd service:

Create `/etc/systemd/system/opensite-backend.service`:

```ini
[Unit]
Description=OpenSite Analytics Backend
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/home/your-user/opensource-site-tracking/backend
Environment="PATH=/home/your-user/opensource-site-tracking/backend/venv/bin"
ExecStart=/home/your-user/opensource-site-tracking/backend/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Start the service:

```bash
sudo systemctl enable opensite-backend
sudo systemctl start opensite-backend
```

#### Frontend Deployment

1. Install Node.js:

```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs
```

2. Build the frontend:

```bash
cd ../frontend
npm install
npm run build
```

3. Set up nginx:

Create `/etc/nginx/sites-available/opensite`:

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    # Frontend
    location / {
        root /home/your-user/opensource-site-tracking/frontend/.next;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # WebSocket
    location /ws/ {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/opensite /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Option 3: Cloud Deployment

#### Deploy to Vercel (Frontend)

1. Connect your GitHub repository to Vercel
2. Configure build settings:
   - Root directory: `frontend`
   - Build command: `npm run build`
   - Output directory: `.next`
3. Add environment variables:
   - `NEXT_PUBLIC_API_URL`: Your backend API URL

#### Deploy to Railway/Heroku (Backend)

1. Connect your GitHub repository
2. Configure build settings:
   - Root directory: `backend`
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
3. Add environment variables from your `.env` file
4. Add PostgreSQL addon

## SSL Configuration

### Using Let's Encrypt with Certbot

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

### Manual SSL Configuration

Update nginx configuration:

```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    # ... rest of configuration
}

server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}
```

## Security Hardening

### Firewall Configuration

```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### Application Security

1. Change default admin password immediately
2. Use strong SECRET_KEY
3. Enable rate limiting
4. Restrict CORS origins
5. Keep dependencies updated
6. Enable fail2ban for brute force protection

## Monitoring

### Application Monitoring

Consider using:
- Sentry for error tracking
- Prometheus for metrics
- Grafana for visualization

### Log Monitoring

- Use journalctl for systemd services:

```bash
sudo journalctl -u opensite-backend -f
```

- Configure log rotation

## Backup Strategy

### Database Backups

Automated backup script:

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump -U opensite_user opensite > /backups/opensite_$DATE.sql
# Keep last 7 days of backups
find /backups -name "opensite_*.sql" -mtime +7 -delete
```

Add to crontab:

```bash
0 2 * * * /path/to/backup-script.sh
```

## Scaling Considerations

### Horizontal Scaling

- Use load balancer (nginx, HAProxy)
- Run multiple backend instances
- Use Redis for session storage
- Use PostgreSQL read replicas

### Database Optimization

- Add indexes for frequently queried fields
- Use connection pooling
- Optimize slow queries
- Consider read replicas for analytics queries

## Troubleshooting

### Backend Not Starting

Check logs:

```bash
sudo journalctl -u opensite-backend -n 50
```

### Frontend Not Loading

Check nginx logs:

```bash
sudo tail -f /var/log/nginx/error.log
```

### Database Connection Issues

Verify database is running:

```bash
sudo systemctl status postgresql
```

Test connection:

```bash
psql -U opensite_user -d opensite -h localhost
```

## Performance Tuning

### Backend

- Use gunicorn with multiple workers:

```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

- Enable database connection pooling

### Frontend

- Enable gzip compression in nginx
- Use CDN for static assets
- Implement caching headers

## Maintenance

### Updates

1. Backup database
2. Pull latest changes
3. Update dependencies
4. Run migrations
5. Restart services

### Health Checks

Monitor:
- Backend health endpoint: `http://yourdomain.com/health`
- Database connectivity
- Disk space
- Memory usage
