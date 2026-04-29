# Configuration Guide

This guide explains all configuration options for OpenSite Analytics.

## Backend Configuration

The backend configuration is managed through environment variables in `backend/.env`.

### Database Settings

```env
DATABASE_URL=sqlite:///./analytics.db
```

- **DATABASE_URL**: SQLite database connection string
- Default: `sqlite:///./analytics.db`
- For production, consider using PostgreSQL or MySQL

### API Settings

```env
API_HOST=0.0.0.0
API_PORT=8000
```

- **API_HOST**: Host address to bind the API server
- Default: `0.0.0.0` (all interfaces)
- **API_PORT**: Port for the API server
- Default: `8000`

### JWT Authentication

```env
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

- **SECRET_KEY**: Secret key for JWT token signing
- **Important**: Change this in production!
- Generate a secure key: `python3 -c "import secrets; print(secrets.token_urlsafe(32))"`
- **ALGORITHM**: JWT algorithm
- Default: `HS256`
- **ACCESS_TOKEN_EXPIRE_MINUTES**: Token expiration time
- Default: `30` minutes

### CORS Settings

```env
CORS_ORIGINS=["http://localhost:3000"]
```

- **CORS_ORIGINS**: List of allowed origins for CORS
- Format: JSON array of URLs
- Default: `["http://localhost:3000"]`
- Example: `["http://localhost:3000", "https://yourdomain.com"]`

### Rate Limiting

```env
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_PERIOD=60
```

- **RATE_LIMIT_REQUESTS**: Maximum requests per period
- Default: `100`
- **RATE_LIMIT_PERIOD**: Time period in seconds
- Default: `60` (1 minute)

### Data Retention

```env
DATA_RETENTION_DAYS=90
```

- **DATA_RETENTION_DAYS**: Number of days to keep analytics data
- Default: `90` days
- Old data is automatically cleaned up by the scheduler

## Frontend Configuration

The frontend configuration is managed through environment variables in `frontend/.env.local`.

### API URL

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

- **NEXT_PUBLIC_API_URL**: Backend API URL
- Default: `http://localhost:8000`
- Must include protocol (http:// or https://)

## Advanced Configuration

### Using PostgreSQL Instead of SQLite

1. Install PostgreSQL and create a database:

```bash
createdb opensite_analytics
```

2. Update `backend/.env`:

```env
DATABASE_URL=postgresql://user:password@localhost/opensite_analytics
```

3. Install PostgreSQL dependencies:

```bash
pip3 install psycopg2-binary
```

### Using MySQL Instead of SQLite

1. Install MySQL and create a database:

```bash
mysql -u root -p
CREATE DATABASE opensite_analytics;
```

2. Update `backend/.env`:

```env
DATABASE_URL=mysql+pymysql://user:password@localhost/opensite_analytics
```

3. Install MySQL dependencies:

```bash
pip3 install pymysql
```

### Custom JWT Secret Generation

Generate a secure random secret key:

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

Copy the output and use it as your `SECRET_KEY`.

### Email Notifications (Future)

To enable email notifications (not yet implemented), you would add:

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM=noreply@yourdomain.com
```

## Security Best Practices

1. **Never commit `.env` files** to version control
2. **Use strong, random secret keys** for JWT
3. **Change default credentials** immediately after installation
4. **Use HTTPS** in production
5. **Restrict CORS origins** to only your domains
6. **Enable rate limiting** to prevent abuse
7. **Regularly update dependencies**
8. **Set appropriate data retention policies**
