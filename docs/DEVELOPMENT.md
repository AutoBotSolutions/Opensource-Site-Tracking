# Development Guide

This guide explains how to contribute to and develop OpenSite Analytics.

## Project Structure

```
opensource-site-tracking/
├── backend/                 # FastAPI backend
│   ├── main.py            # Main application
│   ├── models.py          # SQLAlchemy models
│   ├── schemas.py         # Pydantic schemas
│   ├── auth.py            # Authentication logic
│   ├── config.py          # Configuration
│   ├── database.py        # Database connection
│   ├── utils.py           # Utility functions
│   ├── tasks.py           # Background tasks
│   ├── geoip.py           # GeoIP service
│   ├── rate_limit.py      # Rate limiting
│   ├── init_db.py         # Database initialization
│   ├── requirements.txt    # Python dependencies
│   └── .env               # Environment variables
├── frontend/              # Next.js frontend
│   ├── src/
│   │   ├── app/          # Next.js app directory
│   │   │   ├── page.tsx  # Dashboard
│   │   │   ├── login/    # Login page
│   │   │   ├── register/ # Registration page
│   │   │   └── site/     # Site analytics
│   │   ├── components/   # React components
│   │   │   └── ui/       # UI components
│   │   └── lib/          # Utilities
│   │       └── api.ts    # API service
│   ├── package.json      # Node dependencies
│   └── .env.local       # Environment variables
└── docs/                # Documentation
```

## Backend Development

### Setting Up Development Environment

1. Create a virtual environment:

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

2. Install development dependencies:

```bash
pip3 install -r requirements.txt
pip3 install pytest pytest-asyncio httpx black flake8
```

3. Set up environment variables:

```bash
cp .env.example .env
# Edit .env with your settings
```

4. Initialize the database:

```bash
python3 init_db.py
```

### Running the Backend

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Testing

Run tests with pytest:

```bash
pytest
```

Run specific test file:

```bash
pytest tests/test_auth.py
```

### Code Style

Format code with black:

```bash
black .
```

Check code quality with flake8:

```bash
flake8 .
```

## Frontend Development

### Setting Up Development Environment

1. Install dependencies:

```bash
cd frontend
npm install
```

2. Set up environment variables:

```bash
cp .env.example .env.local
# Edit .env.local with your settings
```

### Running the Frontend

```bash
npm run dev
```

### Building for Production

```bash
npm run build
```

### Testing

Run tests with jest:

```bash
npm test
```

Run tests in watch mode:

```bash
npm test -- --watch
```

### Code Style

Format code with prettier:

```bash
npm run format
```

Check code with ESLint:

```bash
npm run lint
```

## Adding New Features

### Backend: Adding a New API Endpoint

1. Define the Pydantic schema in `schemas.py`:

```python
class NewFeatureCreate(BaseModel):
    name: str
    value: str

class NewFeatureResponse(BaseModel):
    id: int
    name: str
    value: str
    created_at: datetime
```

2. Add the endpoint in `main.py`:

```python
@app.post("/api/new-feature", response_model=NewFeatureResponse)
async def create_new_feature(
    feature: NewFeatureCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Your logic here
    pass
```

3. Add the model to `models.py` if needed

### Frontend: Adding a New Page

1. Create a new page in `src/app/`:

```bash
mkdir -p src/app/new-page
touch src/app/new-page/page.tsx
```

2. Add your page content:

```tsx
'use client'

export default function NewPage() {
  return (
    <div>
      <h1>New Page</h1>
    </div>
  )
}
```

3. Add navigation in the appropriate component

### Frontend: Adding a New Component

1. Create a new component in `src/components/`:

```bash
touch src/components/NewComponent.tsx
```

2. Add your component:

```tsx
interface NewComponentProps {
  title: string
}

export default function NewComponent({ title }: NewComponentProps) {
  return <div>{title}</div>
}
```

3. Import and use it in your pages

## Database Migrations

For schema changes, you'll need to:

1. Update the model in `models.py`
2. Create a migration script or update `init_db.py`
3. Test with a fresh database

Example migration script:

```python
from database import SessionLocal, engine, Base
from models import YourModel

def migrate():
    db = SessionLocal()
    try:
        # Your migration logic
        db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    migrate()
```

## API Documentation

API documentation is auto-generated using FastAPI's OpenAPI integration.

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

Update docstrings in your endpoint functions to improve documentation:

```python
@app.post("/api/endpoint")
async def endpoint_name(param: str):
    """
    Endpoint description
    
    Args:
        param: Parameter description
    
    Returns:
        Response description
    """
    pass
```

## WebSocket Development

Real-time updates are implemented using WebSockets.

### Backend WebSocket Endpoint

```python
@app.websocket("/ws/{site_id}")
async def websocket_endpoint(websocket: WebSocket, site_id: int):
    await manager.connect(websocket, site_id)
    try:
        while True:
            data = await websocket.receive_text()
            # Handle data
    finally:
        manager.disconnect(websocket, site_id)
```

### Frontend WebSocket Client

```typescript
class AnalyticsWebSocket {
  constructor(siteId: number) {
    this.siteId = siteId
    this.ws = null
  }

  connect() {
    this.ws = new WebSocket(`ws://localhost:8000/ws/${this.siteId}`)
    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      this.emit(data.type, data)
    }
  }

  on(event: string, callback: Function) {
    // Event handling
  }
}
```

## Performance Optimization

### Backend

- Use database indexes for frequently queried fields
- Implement caching for expensive operations
- Use connection pooling for database connections
- Optimize N+1 queries with eager loading

### Frontend

- Use React.memo for expensive components
- Implement virtual scrolling for long lists
- Lazy load components with React.lazy
- Optimize images and assets

## Security Considerations

- Always validate input data
- Use parameterized queries to prevent SQL injection
- Implement rate limiting to prevent abuse
- Sanitize user-generated content
- Keep dependencies updated
- Use HTTPS in production
- Implement proper CORS policies

## Contributing

1. Fork the repository
2. Create a feature branch:

```bash
git checkout -b feature/your-feature-name
```

3. Make your changes
4. Write tests for new features
5. Ensure code style compliance
6. Commit your changes:

```bash
git commit -m "Add your feature"
```

7. Push to your branch:

```bash
git push origin feature/your-feature-name
```

8. Create a pull request

## Pull Request Guidelines

- Describe what your PR does
- Reference related issues
- Add tests for new features
- Update documentation
- Ensure all tests pass
- Follow the existing code style

## Release Process

1. Update version numbers
2. Update CHANGELOG.md
3. Tag the release:

```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

4. Create GitHub release

## Getting Help

- Check existing issues
- Read the documentation
- Ask questions in discussions
- Create a new issue for bugs
