# Troubleshooting Guide

This document provides solutions to common issues encountered with OpenSite Analytics.

## Installation Issues

### Backend Installation

#### Problem: pip install fails with dependency conflicts

**Symptoms:**
```
ERROR: pip's dependency resolver does not currently take into account...
```

**Solutions:**
1. Upgrade pip:
```bash
pip3 install --upgrade pip
```

2. Use force reinstall:
```bash
pip3 install -r requirements.txt --force-reinstall
```

3. Create fresh virtual environment:
```bash
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

#### Problem: Python 3.13 compatibility issues

**Symptoms:**
```
AssertionError: The 'backref' keyword argument on Column...
```

**Solutions:**
1. Ensure SQLAlchemy is version 2.0.36+:
```bash
pip3 install --upgrade 'SQLAlchemy>=2.0.36'
```

2. Update pydantic:
```bash
pip3 install --upgrade 'pydantic[email]>=2.10.0'
```

### Frontend Installation

#### Problem: npm install fails

**Symptoms:**
```
npm ERR! code ENOENT
npm ERR! syscall open
```

**Solutions:**
1. Clear npm cache:
```bash
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

2. Use legacy peer deps:
```bash
npm install --legacy-peer-deps
```

#### Problem: Module not found errors

**Symptoms:**
```
Module not found: Can't resolve 'camelcase-css'
```

**Solutions:**
1. Install missing module:
```bash
npm install camelcase-css
```

2. Reinstall dependencies:
```bash
rm -rf node_modules
npm install
```

## Backend Issues

### Server Won't Start

#### Problem: Port already in use

**Symptoms:**
```
OSError: [Errno 48] Address already in use
```

**Solutions:**
1. Find and kill process:
```bash
lsof -ti:8000 | xargs kill -9
```

2. Use different port:
```bash
uvicorn main:app --port 8001
```

#### Problem: Database connection error

**Symptoms:**
```
sqlalchemy.exc.OperationalError: unable to open database file
```

**Solutions:**
1. Check database file permissions:
```bash
ls -la backend/analytics.db
```

2. Ensure directory exists:
```bash
mkdir -p backend
```

3. Reinitialize database:
```bash
rm backend/analytics.db
python3 backend/init_db.py
```

### Authentication Issues

#### Problem: "Could not validate credentials" error

**Symptoms:**
```
{"detail":"Could not validate credentials"}
```

**Solutions:**
1. Check SECRET_KEY in .env:
```bash
cat backend/.env | grep SECRET_KEY
```

2. Generate new SECRET_KEY:
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

3. Clear browser localStorage and login again

4. Check token expiration in config

#### Problem: Login fails with correct credentials

**Symptoms:**
- Login form returns error
- Credentials are correct

**Solutions:**
1. Check user exists in database:
```python
python3 -c "from database import SessionLocal; from models import User; db = SessionLocal(); print(db.query(User).all()); db.close()"
```

2. Reinitialize database:
```bash
python3 backend/init_db.py
```

3. Check password hashing in auth.py

### API Issues

#### Problem: CORS errors

**Symptoms:**
```
Access to XMLHttpRequest blocked by CORS policy
```

**Solutions:**
1. Check CORS_ORIGINS in .env:
```bash
cat backend/.env | grep CORS_ORIGINS
```

2. Ensure correct JSON format:
```env
CORS_ORIGINS=["http://localhost:3000"]
```

3. Restart backend server

#### Problem: Rate limiting errors

**Symptoms:**
```
429 Too Many Requests
```

**Solutions:**
1. Wait for rate limit to reset (default: 60 seconds)
2. Increase rate limit in .env:
```env
RATE_LIMIT_REQUESTS=200
RATE_LIMIT_PERIOD=60
```
3. Check if you're being rate limited legitimately

## Frontend Issues

### Build Errors

#### Problem: TypeScript compilation errors

**Symptoms:**
```
Type error: Cannot find name 'Component'
```

**Solutions:**
1. Clear Next.js cache:
```bash
rm -rf .next
npm run dev
```

2. Install TypeScript types:
```bash
npm install --save-dev @types/node @types/react @types/react-dom
```

3. Check tsconfig.json configuration

#### Problem: Build fails with module resolution errors

**Symptoms:**
```
Module not found: Can't resolve '@/components/...'
```

**Solutions:**
1. Check tsconfig.json paths:
```json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

2. Restart dev server

### Runtime Errors

#### Problem: Page not found on navigation

**Symptoms:**
- 404 error when clicking links
- Routes not working

**Solutions:**
1. Check Next.js app directory structure
2. Ensure page.tsx exists in folder
3. Check for case sensitivity in file names
4. Restart dev server

#### Problem: API calls fail in browser

**Symptoms:**
```
Network Error
TypeError: Failed to fetch
```

**Solutions:**
1. Check NEXT_PUBLIC_API_URL in .env.local:
```bash
cat frontend/.env.local | grep NEXT_PUBLIC_API_URL
```

2. Ensure backend is running
3. Check browser console for CORS errors
4. Verify API endpoint is correct

### WebSocket Issues

#### Problem: WebSocket connection fails

**Symptoms:**
```
WebSocket connection to 'ws://localhost:8000/ws/...' failed
```

**Solutions:**
1. Check if WebSocket endpoint exists in backend
2. Verify site_id is valid
3. Check authentication token
4. Ensure WebSocket is not blocked by firewall

## Analytics Issues

### Tracking Not Working

#### Problem: No data showing in dashboard

**Symptoms:**
- Dashboard shows 0 page views
- Tracking code installed but no data

**Solutions:**
1. Verify tracking code is installed correctly:
```html
<!-- Check script is in <head> section -->
<!-- Check site_key and api_key are correct -->
<!-- Check API URL is correct -->
```

2. Check browser console for errors:
```javascript
// Look for JavaScript errors
// Check network tab for failed requests
```

3. Test tracking endpoint directly:
```bash
curl -X POST http://localhost:8000/api/track/pageview \
  -H "Content-Type: application/json" \
  -d '{"site_id":1,"api_key":"your-key","url":"/test"}'
```

4. Check site is active in database

#### Problem: Incorrect analytics data

**Symptoms:**
- Duplicate page views
- Wrong referrer information
- Incorrect device breakdown

**Solutions:**
1. Check for duplicate tracking code installation
2. Verify site domain matches registered domain
3. Check for bot traffic
4. Review tracking code placement

### Performance Issues

#### Problem: Dashboard loads slowly

**Symptoms:**
- Long loading times
- Timeout errors

**Solutions:**
1. Check database query performance
2. Add indexes to frequently queried columns
3. Implement pagination
4. Cache analytics data
5. Use database connection pooling

#### Problem: High memory usage

**Symptoms:**
- Backend process using excessive memory
- Server becomes unresponsive

**Solutions:**
1. Check for memory leaks
2. Implement data retention cleanup
3. Limit WebSocket connections
4. Use pagination for large datasets
5. Monitor with profiling tools

## Database Issues

### SQLite Issues

#### Problem: Database locked

**Symptoms:**
```
sqlite3.OperationalError: database is locked
```

**Solutions:**
1. Close all database connections
2. Check for long-running transactions
3. Restart backend server
4. Use WAL mode:
```python
# In database.py
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
```

#### Problem: Database corruption

**Symptoms:**
```
sqlite3.DatabaseError: database disk image is malformed
```

**Solutions:**
1. Restore from backup
2. Use SQLite recovery:
```bash
sqlite3 analytics.db ".recover" | sqlite3 recovered.db
```
3. Reinitialize database (last resort)

### PostgreSQL Issues

#### Problem: Connection pool exhausted

**Symptoms:**
```
sqlalchemy.exc.TimeoutError: QueuePool limit of size 5 overflow 10 reached
```

**Solutions:**
1. Increase pool size:
```python
engine = create_engine(DATABASE_URL, pool_size=20, max_overflow=40)
```

2. Close connections properly
3. Check for connection leaks

#### Problem: Slow queries

**Symptoms:**
- Analytics queries take long time
- Dashboard timeouts

**Solutions:**
1. Add indexes:
```python
# In models.py
from sqlalchemy import Index

Index('idx_pageviews_site_created', PageView.site_id, PageView.created_at)
```

2. Use EXPLAIN ANALYZE:
```sql
EXPLAIN ANALYZE SELECT * FROM pageviews WHERE site_id = 1;
```

3. Optimize queries
4. Consider read replicas

## Deployment Issues

### Docker Issues

#### Problem: Container won't start

**Symptoms:**
```
docker-compose up fails
Container exits immediately
```

**Solutions:**
1. Check logs:
```bash
docker-compose logs backend
```

2. Verify environment variables
3. Check volume permissions
4. Rebuild images:
```bash
docker-compose build --no-cache
```

#### Problem: Can't access service from host

**Symptoms:**
- localhost:port not accessible
- Connection refused

**Solutions:**
1. Check port mapping in docker-compose.yml
2. Verify service is running:
```bash
docker-compose ps
```
3. Check firewall settings
4. Use 0.0.0.0 instead of localhost

### Nginx Issues

#### Problem: 502 Bad Gateway

**Symptoms:**
- Nginx returns 502 error
- Backend not accessible

**Solutions:**
1. Check if backend is running
2. Verify upstream configuration
3. Check nginx error logs:
```bash
sudo tail -f /var/log/nginx/error.log
```
4. Test backend directly

#### Problem: SSL certificate errors

**Symptoms:**
- HTTPS not working
- Certificate errors

**Solutions:**
1. Renew certificate:
```bash
sudo certbot renew
```

2. Check certificate path in nginx config
3. Verify certificate is valid:
```bash
openssl x509 -in /path/to/cert.pem -text -noout
```

## Debugging Tips

### Enable Debug Mode

**Backend:**
```python
# In main.py
app = FastAPI(debug=True)
```

**Frontend:**
```bash
npm run dev
# Check browser console
```

### Enable Verbose Logging

**Backend:**
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

**Frontend:**
```typescript
// In api.ts
api.interceptors.request.use(request => {
  console.log('API Request:', request)
  return request
})
```

### Database Query Logging

```python
# In database.py
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)
```

### Network Debugging

```bash
# Check if port is open
netstat -an | grep 8000

# Test API endpoint
curl -v http://localhost:8000/health

# Check DNS
nslookup yourdomain.com
```

## Getting Help

If you can't resolve your issue:

1. Check existing documentation
2. Search GitHub issues
3. Enable debug logging
4. Collect relevant logs
5. Create a new issue with:
   - Description of the problem
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Environment details
   - Relevant logs
   - Screenshots if applicable
