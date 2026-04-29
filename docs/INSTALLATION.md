# Installation Guide

This guide will help you install and set up OpenSite Analytics on your server.

## Prerequisites

- Python 3.13 or higher
- Node.js 18 or higher
- npm or yarn
- SQLite (included with Python)

## Backend Installation

### 1. Navigate to the backend directory

```bash
cd backend
```

### 2. Create a virtual environment (recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Python dependencies

```bash
pip3 install -r requirements.txt
```

### 4. Set up environment variables

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and configure the following:

```env
# Database
DATABASE_URL=sqlite:///./analytics.db

# API Settings
API_HOST=0.0.0.0
API_PORT=8000

# JWT Settings
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS Settings
CORS_ORIGINS=["http://localhost:3000"]

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_PERIOD=60

# Data Retention
DATA_RETENTION_DAYS=90
```

### 5. Initialize the database

```bash
python3 init_db.py
```

This will create the database tables and a default user:
- Email: `admin@example.com`
- Password: `admin123`

**Important:** Change the default password after first login.

### 6. Start the backend server

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The backend will be available at `http://localhost:8000`

## Frontend Installation

### 1. Navigate to the frontend directory

```bash
cd frontend
```

### 2. Install Node.js dependencies

```bash
npm install
```

### 3. Set up environment variables

Create a `.env.local` file:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 4. Start the frontend development server

```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Verification

1. Visit `http://localhost:3000`
2. Login with `admin@example.com` / `admin123`
3. Create your first site
4. Copy the tracking code and add it to your website

## Troubleshooting

### Python Dependencies Issues

If you encounter dependency conflicts, try:

```bash
pip3 install --upgrade pip
pip3 install -r requirements.txt --force-reinstall
```

### Port Already in Use

If port 8000 or 3000 is already in use, you can change them in the `.env` files or use different ports:

```bash
# Backend
uvicorn main:app --host 0.0.0.0 --port 8001 --reload

# Frontend
npm run dev -- -p 3001
```

### Database Issues

If you encounter database errors, you can reset the database:

```bash
rm backend/analytics.db
python3 backend/init_db.py
```

## Production Deployment

For production deployment, see [DEPLOYMENT.md](DEPLOYMENT.md)
