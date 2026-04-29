# System Architecture

This document provides an overview of the OpenSite Analytics system architecture.

## High-Level Architecture

OpenSite Analytics follows a modern microservices-inspired architecture with clear separation between frontend and backend:

```
┌─────────────────┐         ┌─────────────────┐
│   Next.js       │         │   FastAPI       │
│   Frontend      │◄────────┤   Backend       │
│   (Port 3000)   │  HTTP   │   (Port 8000)   │
└─────────────────┘         └─────────────────┘
                                    │
                                    ▼
                            ┌───────────────┐
                            │   SQLite/     │
                            │   PostgreSQL  │
                            │   Database    │
                            └───────────────┘
```

## Components

### Frontend (Next.js)

**Technology Stack:**
- Next.js 14 (App Router)
- React 18
- TypeScript
- TailwindCSS
- shadcn/ui components
- Recharts (data visualization)
- Axios (HTTP client)

**Key Features:**
- Server-side rendering (SSR)
- Static site generation (SSG)
- Client-side components for interactivity
- Responsive design
- Real-time updates (WebSocket)

**Directory Structure:**
```
frontend/
├── src/
│   ├── app/              # Next.js App Router pages
│   │   ├── page.tsx      # Dashboard
│   │   ├── login/        # Authentication
│   │   └── site/         # Site analytics
│   ├── components/       # React components
│   │   └── ui/           # UI components
│   └── lib/              # Utilities
│       └── api.ts        # API service
└── public/               # Static assets
```

### Backend (FastAPI)

**Technology Stack:**
- FastAPI (Python 3.13)
- SQLAlchemy (ORM)
- Pydantic (validation)
- JWT (authentication)
- APScheduler (background tasks)
- GeoIP2 (location detection)
- WebSocket (real-time updates)

**Key Features:**
- Async/await support
- Automatic API documentation (Swagger/ReDoc)
- Type hints and validation
- Rate limiting
- CORS support
- Background task scheduling

**Directory Structure:**
```
backend/
├── main.py              # FastAPI application
├── models.py            # SQLAlchemy models
├── schemas.py           # Pydantic schemas
├── auth.py              # Authentication logic
├── config.py            # Configuration
├── database.py          # Database connection
├── utils.py             # Utility functions
├── tasks.py             # Background tasks
├── geoip.py             # GeoIP service
├── rate_limit.py        # Rate limiting
└── init_db.py           # Database initialization
```

## Data Flow

### Authentication Flow

```
1. User submits credentials
   ↓
2. Frontend sends POST /api/auth/login
   ↓
3. Backend validates credentials
   ↓
4. Backend generates JWT token
   ↓
5. Backend returns token to frontend
   ↓
6. Frontend stores token in localStorage
   ↓
7. Frontend includes token in Authorization header
   ↓
8. Backend validates token on each request
```

### Tracking Flow

```
1. User visits website with tracking code
   ↓
2. JavaScript SDK sends data to backend
   ↓
3. Backend validates API key
   ↓
4. Backend processes and stores data
   ↓
5. Backend returns success response
   ↓
6. Background tasks aggregate data
   ↓
7. WebSocket pushes real-time updates
```

### Analytics Query Flow

```
1. User requests analytics dashboard
   ↓
2. Frontend sends GET /api/analytics/{site_id}
   ↓
3. Backend validates JWT token
   ↓
4. Backend queries database for site ownership
   ↓
5. Backend aggregates analytics data
   ↓
6. Backend returns structured analytics
   ↓
7. Frontend renders charts and visualizations
```

## Database Schema

### Core Tables

**Users**
- id (PK)
- email (unique)
- password_hash
- created_at
- is_active

**Sites**
- id (PK)
- name
- domain (unique)
- site_key (unique)
- api_key (unique)
- owner_id (FK → users.id)
- created_at
- is_active

**PageViews**
- id (PK)
- site_id (FK → sites.id)
- session_id
- url
- title
- referrer
- user_agent
- ip_address
- country
- created_at

**Events**
- id (PK)
- site_id (FK → sites.id)
- session_id
- event_name
- event_data (JSON)
- created_at

**Sessions**
- id (PK)
- site_id (FK → sites.id)
- session_id (unique)
- started_at
- ended_at
- page_views_count

**Goals**
- id (PK)
- site_id (FK → sites.id)
- name
- description
- goal_type
- target_value
- created_at

## Security Architecture

### Authentication
- JWT-based stateless authentication
- Token expiration (configurable)
- Secure password hashing (bcrypt)
- Token refresh mechanism

### Authorization
- Role-based access control (future)
- Site ownership validation
- API key verification for tracking

### Security Measures
- Rate limiting per IP
- CORS configuration
- SQL injection prevention (ORM)
- XSS protection
- CSRF protection (future)

## Performance Architecture

### Caching Strategy
- Database query optimization
- Connection pooling
- Future: Redis caching for frequent queries

### Scalability
- Stateless backend (easy horizontal scaling)
- Database read replicas (future)
- Load balancer support
- WebSocket connection management

### Background Tasks
- APScheduler for periodic tasks
- Data retention cleanup
- Analytics aggregation
- Email notifications (future)

## WebSocket Architecture

### Connection Management
```python
class ConnectionManager:
    - active_connections: dict
    - connect(websocket, site_id)
    - disconnect(websocket, site_id)
    - broadcast(message, site_id)
```

### Real-time Updates
- Page view events
- Custom events
- Visitor count updates
- Goal completions

## Deployment Architecture

### Development
- Frontend: Next.js dev server (port 3000)
- Backend: Uvicorn with auto-reload (port 8000)
- Database: SQLite (local file)

### Production Options
1. **Docker Compose**
   - Containerized services
   - Easy deployment
   - Scalable

2. **Manual Deployment**
   - Nginx reverse proxy
   - Systemd services
   - PostgreSQL database

3. **Cloud Platforms**
   - Vercel (frontend)
   - Railway/Heroku (backend)
   - Managed databases

## Monitoring & Logging

### Application Logging
- Structured logging
- Log levels (DEBUG, INFO, WARNING, ERROR)
- Request/response logging
- Error tracking

### Performance Monitoring
- Response time tracking
- Database query performance
- WebSocket connection health
- Resource usage

### Future Enhancements
- Prometheus metrics
- Grafana dashboards
- Sentry error tracking
- APM integration

## API Versioning

Current version: v1 (implicit)

Future versions will include:
- Version prefix in URL (`/api/v2/...`)
- Backward compatibility
- Deprecation warnings
- Migration guides

## Extensibility

### Plugin System (Future)
- Custom analytics processors
- Third-party integrations
- Custom authentication providers
- Custom storage backends

### Webhooks (Future)
- Event notifications
- Third-party integrations
- Custom workflows

## Technology Rationale

### Why FastAPI?
- Modern async support
- Automatic API documentation
- Type safety with Pydantic
- High performance
- Python ecosystem

### Why Next.js?
- Server-side rendering
- Excellent developer experience
- Built-in routing
- SEO friendly
- React ecosystem

### Why SQLAlchemy?
- Database agnostic
- Powerful ORM
- Migration support
- Type hints support
- Mature and stable

### Why JWT?
- Stateless authentication
- Cross-platform support
- Standardized
- Easy to implement
- Scalable
