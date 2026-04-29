# API Documentation

OpenSite Analytics provides a RESTful API for managing sites, tracking analytics, and user authentication.

## Base URL

```
http://localhost:8000
```

## Authentication

All API endpoints (except login and register) require JWT authentication.

### Headers

```
Authorization: Bearer <your_jwt_token>
Content-Type: application/json
```

## Endpoints

### Authentication

#### Login

```http
POST /api/auth/login
```

**Request Body:**

```json
{
  "email": "admin@example.com",
  "password": "admin123"
}
```

**Response:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "email": "admin@example.com",
    "id": 1
  }
}
```

#### Register

```http
POST /api/auth/register
```

**Request Body:**

```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response:**

```json
{
  "email": "user@example.com",
  "id": 2,
  "created_at": "2026-04-29T12:00:00"
}
```

#### Get Current User

```http
GET /api/auth/me
```

**Response:**

```json
{
  "email": "admin@example.com",
  "id": 1,
  "created_at": "2026-04-29T12:00:00"
}
```

### Sites

#### List Sites

```http
GET /api/sites
```

**Response:**

```json
[
  {
    "id": 1,
    "name": "My Website",
    "domain": "example.com",
    "site_key": "abc123",
    "api_key": "xyz789",
    "created_at": "2026-04-29T12:00:00",
    "is_active": true
  }
]
```

#### Get Site

```http
GET /api/sites/{site_id}
```

**Response:**

```json
{
  "id": 1,
  "name": "My Website",
  "domain": "example.com",
  "site_key": "abc123",
  "api_key": "xyz789",
  "created_at": "2026-04-29T12:00:00",
  "is_active": true
}
```

#### Create Site

```http
POST /api/sites
```

**Request Body:**

```json
{
  "name": "My Website",
  "domain": "example.com"
}
```

**Response:**

```json
{
  "id": 1,
  "name": "My Website",
  "domain": "example.com",
  "site_key": "abc123",
  "api_key": "xyz789",
  "created_at": "2026-04-29T12:00:00",
  "is_active": true
}
```

### Analytics

#### Get Analytics

```http
GET /api/analytics/{site_id}?period=7days
```

**Query Parameters:**

- `period`: Time period for analytics (default: `7days`)
  - Options: `1day`, `7days`, `30days`, `90days`

**Response:**

```json
{
  "summary": {
    "site_id": 1,
    "period": "7days",
    "total_pageviews": 1000,
    "unique_visitors": 500,
    "total_sessions": 300,
    "bounce_rate": 45.5,
    "avg_session_duration": 120.5,
    "top_pages": [["/", 500], ["/about", 200]],
    "top_referrers": [["google.com", 300], ["direct", 200]],
    "device_breakdown": {
      "Desktop": 600,
      "Mobile": 350,
      "Tablet": 50
    },
    "browser_breakdown": {
      "Chrome": 500,
      "Firefox": 300,
      "Safari": 200
    },
    "country_breakdown": {
      "US": 400,
      "UK": 200,
      "DE": 100
    }
  },
  "pageviews_over_time": [
    {"date": "2026-04-22", "pageviews": 100},
    {"date": "2026-04-23", "pageviews": 150}
  ],
  "events_summary": [
    ["signup", 50],
    ["purchase", 25]
  ]
}
```

### Tracking

#### Track Page View

```http
POST /api/track/pageview
```

**Request Body:**

```json
{
  "site_id": 1,
  "api_key": "xyz789",
  "url": "/about",
  "title": "About Us",
  "referrer": "https://google.com",
  "user_agent": "Mozilla/5.0...",
  "session_id": "abc123"
}
```

**Response:**

```json
{
  "status": "success"
}
```

#### Track Event

```http
POST /api/track/event
```

**Request Body:**

```json
{
  "site_id": 1,
  "api_key": "xyz789",
  "event_name": "signup",
  "event_data": {
    "plan": "pro"
  },
  "session_id": "abc123"
}
```

**Response:**

```json
{
  "status": "success"
}
```

### Goals

#### Create Goal

```http
POST /api/goals
```

**Request Body:**

```json
{
  "site_id": 1,
  "name": "Newsletter Signup",
  "description": "Track newsletter signups",
  "goal_type": "event",
  "target_value": "newsletter_signup"
}
```

**Response:**

```json
{
  "id": 1,
  "site_id": 1,
  "name": "Newsletter Signup",
  "description": "Track newsletter signups",
  "goal_type": "event",
  "target_value": "newsletter_signup",
  "created_at": "2026-04-29T12:00:00"
}
```

#### Get Goals

```http
GET /api/goals/{site_id}
```

**Response:**

```json
[
  {
    "id": 1,
    "site_id": 1,
    "name": "Newsletter Signup",
    "description": "Track newsletter signups",
    "goal_type": "event",
    "target_value": "newsletter_signup",
    "created_at": "2026-04-29T12:00:00"
  }
]
```

## Error Responses

All endpoints may return error responses in the following format:

```json
{
  "detail": "Error message"
}
```

### Common HTTP Status Codes

- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required or invalid
- `403 Forbidden`: Access denied
- `404 Not Found`: Resource not found
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

## Rate Limiting

The API has rate limiting enabled:
- Default: 100 requests per minute per IP
- Tracking endpoints have higher limits (200 requests per minute)

## Interactive API Documentation

Interactive API documentation is available at:

```
http://localhost:8000/docs
```

This provides a Swagger UI where you can test all endpoints directly.
