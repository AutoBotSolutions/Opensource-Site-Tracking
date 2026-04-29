# Database Schema

This document provides detailed information about the OpenSite Analytics database schema.

## Overview

OpenSite Analytics uses a relational database schema designed for efficient analytics data storage and retrieval. The default database is SQLite, with support for PostgreSQL and MySQL.

## Entity Relationship Diagram

```
┌─────────────┐
│    Users    │
├─────────────┤
│ id (PK)     │
│ email       │
│ password    │
│ created_at  │
│ is_active   │
└─────────────┘
       │ 1
       │
       │ N
┌─────────────┐
│    Sites    │
├─────────────┤
│ id (PK)     │
│ name        │
│ domain      │
│ site_key    │
│ api_key     │
│ owner_id(FK)│
│ created_at  │
│ is_active   │
└─────────────┘
       │ 1
       │
       │ N
┌─────────────────────────────────────────────────┐
│              PageViews & Events                 │
├─────────────────────────────────────────────────┤
│ id (PK)                                        │
│ site_id (FK)                                   │
│ session_id                                     │
│ url / event_name                               │
│ user_agent / event_data                        │
│ ip_address                                     │
│ country                                        │
│ created_at                                     │
└─────────────────────────────────────────────────┘
```

## Tables

### Users

Stores user account information.

| Column | Type | Constraints | Description |
|--------|------|------------|-------------|
| id | Integer | PRIMARY KEY, AUTO INCREMENT | Unique user identifier |
| email | String(255) | UNIQUE, NOT NULL | User email address |
| password_hash | String(255) | NOT NULL | Bcrypt hashed password |
| created_at | DateTime | DEFAULT CURRENT_TIMESTAMP | Account creation timestamp |
| is_active | Boolean | DEFAULT TRUE | Account status |

**Indexes:**
- `email` (unique)

**Relationships:**
- One-to-many with Sites (owner_id)

### Sites

Stores website tracking configurations.

| Column | Type | Constraints | Description |
|--------|------|------------|-------------|
| id | Integer | PRIMARY KEY, AUTO INCREMENT | Unique site identifier |
| name | String(255) | NOT NULL | Site display name |
| domain | String(255) | UNIQUE, NOT NULL | Site domain name |
| site_key | String(64) | UNIQUE, NOT NULL | Public tracking key |
| api_key | String(64) | UNIQUE, NOT NULL | Private API key |
| owner_id | Integer | FOREIGN KEY, NOT NULL | User owner reference |
| created_at | DateTime | DEFAULT CURRENT_TIMESTAMP | Site creation timestamp |
| is_active | Boolean | DEFAULT TRUE | Site tracking status |

**Indexes:**
- `domain` (unique)
- `site_key` (unique)
- `api_key` (unique)
- `owner_id`

**Relationships:**
- Many-to-one with Users (owner_id)
- One-to-many with PageViews
- One-to-many with Events
- One-to-many with Sessions
- One-to-many with Goals

### PageViews

Stores individual page view events.

| Column | Type | Constraints | Description |
|--------|------|------------|-------------|
| id | Integer | PRIMARY KEY, AUTO INCREMENT | Unique page view identifier |
| site_id | Integer | FOREIGN KEY, NOT NULL | Site reference |
| session_id | String(255) | INDEXED | Session identifier |
| url | Text | NOT NULL | Page URL |
| title | String(255) | Page title |
| referrer | Text | Referrer URL |
| user_agent | Text | Browser user agent |
| ip_address | String(45) | IPv4 or IPv6 address |
| country | String(2) | ISO country code |
| created_at | DateTime | DEFAULT CURRENT_TIMESTAMP, INDEXED | Timestamp |

**Indexes:**
- `site_id`
- `session_id`
- `created_at`
- Composite index: `(site_id, created_at)`

**Relationships:**
- Many-to-one with Sites (site_id)

### Events

Stores custom event tracking data.

| Column | Type | Constraints | Description |
|--------|------|------------|-------------|
| id | Integer | PRIMARY KEY, AUTO INCREMENT | Unique event identifier |
| site_id | Integer | FOREIGN KEY, NOT NULL | Site reference |
| session_id | String(255) | INDEXED | Session identifier |
| event_name | String(255) | NOT NULL, INDEXED | Event name |
| event_data | JSON | Custom event properties | 
| created_at | DateTime | DEFAULT CURRENT_TIMESTAMP, INDEXED | Timestamp |

**Indexes:**
- `site_id`
- `session_id`
- `event_name`
- `created_at`
- Composite index: `(site_id, created_at)`

**Relationships:**
- Many-to-one with Sites (site_id)

### Sessions

Stores user session information.

| Column | Type | Constraints | Description |
|--------|------|------------|-------------|
| id | Integer | PRIMARY KEY, AUTO INCREMENT | Unique session identifier |
| site_id | Integer | FOREIGN KEY, NOT NULL | Site reference |
| session_id | String(255) | UNIQUE, NOT NULL | Session identifier |
| started_at | DateTime | DEFAULT CURRENT_TIMESTAMP | Session start time |
| ended_at | DateTime | Session end time | 
| page_views_count | Integer | DEFAULT 0 | Total page views in session |

**Indexes:**
- `site_id`
- `session_id` (unique)

**Relationships:**
- Many-to-one with Sites (site_id)

### Goals

Stores conversion goal definitions.

| Column | Type | Constraints | Description |
|--------|------|------------|-------------|
| id | Integer | PRIMARY KEY, AUTO INCREMENT | Unique goal identifier |
| site_id | Integer | FOREIGN KEY, NOT NULL | Site reference |
| name | String(255) | NOT NULL | Goal display name |
| description | Text | Goal description |
| goal_type | String(50) | NOT NULL | 'pageview' or 'event' |
| target_value | String(255) | Target URL or event name |
| created_at | DateTime | DEFAULT CURRENT_TIMESTAMP | Goal creation timestamp |

**Indexes:**
- `site_id`
- `goal_type`

**Relationships:**
- Many-to-one with Sites (site_id)

## Database Constraints

### Foreign Keys

1. **Sites.owner_id** → Users.id
   - ON DELETE: CASCADE
   - ON UPDATE: RESTRICT

2. **PageViews.site_id** → Sites.id
   - ON DELETE: CASCADE
   - ON UPDATE: RESTRICT

3. **Events.site_id** → Sites.id
   - ON DELETE: CASCADE
   - ON UPDATE: RESTRICT

4. **Sessions.site_id** → Sites.id
   - ON DELETE: CASCADE
   - ON UPDATE: RESTRICT

5. **Goals.site_id** → Sites.id
   - ON DELETE: CASCADE
   - ON UPDATE: RESTRICT

### Unique Constraints

- Users.email
- Sites.domain
- Sites.site_key
- Sites.api_key
- Sessions.session_id

### Not Null Constraints

All required fields have NOT NULL constraints as indicated in the table schemas.

## Data Types

### String Lengths

- Email: 255 characters
- Site name: 255 characters
- Domain: 255 characters
- Site key: 64 characters (generated)
- API key: 64 characters (generated)
- Event name: 255 characters
- Country code: 2 characters (ISO 3166-1 alpha-2)

### JSON Fields

- Events.event_data: Flexible JSON structure for custom event properties

## Indexing Strategy

### Primary Indexes
- All tables have primary key indexes on id columns

### Foreign Key Indexes
- All foreign key columns are indexed for join performance

### Performance Indexes
- PageViews.created_at: For time-based queries
- PageViews.session_id: For session aggregation
- Events.event_name: For event filtering
- Events.created_at: For time-based queries

### Composite Indexes
- PageViews: (site_id, created_at) for site-specific time queries
- Events: (site_id, created_at) for site-specific time queries

## Data Retention

Old data is automatically cleaned up based on the `DATA_RETENTION_DAYS` configuration (default: 90 days).

### Cleanup Process

The background scheduler runs a cleanup task that:
1. Deletes page views older than retention period
2. Deletes events older than retention period
3. Archives or deletes sessions with no recent activity

## Migration Guide

### Adding New Columns

```python
# In models.py
class Site(Base):
    # ... existing columns
    new_column = Column(String(255))

# Run migration
python3 migrate.py
```

### Adding New Tables

```python
# In models.py
class NewTable(Base):
    __tablename__ = "new_table"
    id = Column(Integer, primary_key=True)
    # ... other columns

# In init_db.py
Base.metadata.create_all(bind=engine)
```

### Modifying Constraints

1. Backup database
2. Apply changes manually or with migration tool
3. Test thoroughly
4. Deploy to production

## Performance Considerations

### Query Optimization

- Use indexed columns in WHERE clauses
- Avoid SELECT * when possible
- Use JOIN instead of subqueries
- Limit result sets with pagination

### Bulk Operations

- Use bulk inserts for multiple records
- Batch updates for performance
- Consider transactions for data consistency

### Database Size Management

- Regular cleanup of old data
- Archive historical data if needed
- Monitor database growth
- Set appropriate retention policies

## Backup Strategy

### SQLite

```bash
# Backup
cp analytics.db analytics.db.backup.$(date +%Y%m%d)

# Restore
cp analytics.db.backup.YYYYMMDD analytics.db
```

### PostgreSQL

```bash
# Backup
pg_dump -U user -d opensite > backup.sql

# Restore
psql -U user -d opensite < backup.sql
```

### MySQL

```bash
# Backup
mysqldump -u user -p opensite > backup.sql

# Restore
mysql -u user -p opensite < backup.sql
```

## Security Considerations

### Sensitive Data

- Passwords are hashed with bcrypt
- API keys are randomly generated
- IP addresses are stored for analytics only
- User agents are stored for analytics only

### Access Control

- Database access restricted to application
- No direct database access from frontend
- Connection strings in environment variables
- Regular security audits

## Future Enhancements

### Planned Schema Changes

- User roles and permissions
- Team/collaboration features
- A/B testing data
- Funnel analysis tables
- Custom dimension support

### Performance Improvements

- Partitioning for large tables
- Materialized views for common queries
- Read replicas for analytics queries
- Caching layer integration
