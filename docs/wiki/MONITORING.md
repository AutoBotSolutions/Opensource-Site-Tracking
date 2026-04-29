# Monitoring Guide

This guide covers monitoring and observability for OpenSite Analytics.

## Overview

Effective monitoring ensures system reliability, performance optimization, and issue detection.

## Key Metrics

### Application Metrics
- Request rate (requests per second)
- Response time (p50, p95, p99)
- Error rate (4xx, 5xx)
- Active WebSocket connections
- Memory usage
- CPU usage

### Database Metrics
- Connection pool usage
- Query execution time
- Database size
- Transaction rate

## Monitoring Tools

### Prometheus + Grafana

**Install Prometheus:**
```bash
wget https://github.com/prometheus/prometheus/releases/download/v2.45.0/prometheus-2.45.0.linux-amd64.tar.gz
tar -xzf prometheus-2.45.0.linux-amd64.tar.gz
cd prometheus-2.45.0.linux-amd64
./prometheus --config.file=prometheus.yml
```

**Add Metrics to Backend:**
```python
pip3 install prometheus-fastapi-instrumentator prometheus-client
```

```python
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter, Histogram, Gauge

app = FastAPI()
Instrumentator().instrument(app).expose(app)

request_counter = Counter('api_requests_total', 'Total API requests', ['method', 'endpoint'])
request_duration = Histogram('api_request_duration_seconds', 'API request duration')
```

### Sentry (Error Tracking)

```bash
pip3 install sentry-sdk
```

```python
import sentry_sdk

sentry_sdk.init(
    dsn="YOUR_SENTRY_DSN",
    traces_sample_rate=1.0,
)
```

## Logging

### Backend Logging

```python
import logging
from logging.handlers import RotatingFileHandler

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler('backend.log', maxBytes=10485760, backupCount=5)
    ]
)

logger = logging.getLogger(__name__)
logger.info("Application started")
```

### Frontend Logging

```typescript
export class Logger {
  info(message: string, data?: object) {
    console.log(`[INFO] ${message}`, data)
  }
  error(message: string, error?: Error) {
    console.error(`[ERROR] ${message}`, error)
  }
}
```

## Health Checks

### Backend Health Check

```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "database": "ok",
        "disk_space": "ok"
    }
```

### Frontend Health Check

```typescript
async function healthCheck() {
  const response = await fetch('/health')
  return await response.json()
}
```

## Alerting

### Email Alerts

```python
import smtplib

def send_alert(subject: str, message: str):
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login('email', 'password')
        server.send_message(msg)
```

### Slack Alerts

```python
import requests

def send_slack_alert(webhook_url: str, message: str):
    requests.post(webhook_url, json={"text": message})
```

## Best Practices

1. Monitor key metrics continuously
2. Set up alerting for critical issues
3. Use structured logging
4. Implement health checks
5. Regular performance reviews
6. Document monitoring setup
7. Test alerting regularly
