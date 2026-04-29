# Performance Optimization

Strategies for optimizing OpenSite Analytics performance.

## Database Optimization

### Indexing

Add indexes for frequently queried columns:

```python
from sqlalchemy import Index

Index('idx_pageviews_site_time', PageView.site_id, PageView.created_at),
Index('idx_events_name', Event.event_name),
```

### Query Optimization

Use eager loading to avoid N+1 queries:

```python
from sqlalchemy.orm import joinedload

sites = db.query(Site).options(joinedload(Site.pageviews)).all()
```

### Connection Pooling

Configure connection pool in database.py:

```python
engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=40,
    pool_pre_ping=True
)
```

## Caching

### Redis Caching

Install Redis:
```bash
pip3 install redis
```

Basic caching implementation:
```python
import redis
from datetime import timedelta

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def get_analytics_cached(site_id: int):
    cache_key = f"analytics:{site_id}"
    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    
    data = calculate_analytics(site_id)
    redis_client.setex(cache_key, 300, json.dumps(data))
    return data
```

## Frontend Optimization

### Code Splitting

Use dynamic imports for large components:

```typescript
const AnalyticsChart = dynamic(() => import('./AnalyticsChart'), {
  loading: () => <LoadingSpinner />
})
```

### Image Optimization

Use Next.js Image component:
```typescript
import Image from 'next/image'

<Image src="/logo.png" alt="Logo" width={200} height={50} />
```

### Lazy Loading

Implement lazy loading for charts:
```typescript
const { ref, inView } = useInView()

return (
  <div ref={ref}>
    {inView && <AnalyticsChart />}
  </div>
)
```

## Backend Optimization

### Async Operations

Use async/await for I/O operations:

```python
@app.get("/api/analytics/{site_id}")
async def get_analytics(site_id: int):
    # Async database operations
    data = await db.execute(query)
    return data
```

### Background Tasks

Offload heavy computations to background:

```python
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()

@scheduler.scheduled_job('interval', minutes=5)
async def aggregate_analytics():
    # Heavy computation
    pass
```

## Monitoring

### Performance Metrics

Track key metrics:
- Response times
- Database query duration
- Memory usage
- CPU usage
- WebSocket connections

### Profiling

Use Python profiler:
```bash
python3 -m cProfile -o profile.stats main.py
```

## Scaling

### Horizontal Scaling

- Use load balancer (nginx, HAProxy)
- Run multiple backend instances
- Use Redis for session storage
- Implement database read replicas

### Database Scaling

- Use PostgreSQL instead of SQLite
- Add read replicas for analytics queries
- Partition large tables by date
- Use connection pooling

## Best Practices

1. **Profile before optimizing** - identify bottlenecks
2. **Measure everything** - use metrics
3. **Cache strategically** - cache expensive operations
4. **Use pagination** - limit result sets
5. **Optimize queries** - use indexes and efficient joins
6. **Monitor continuously** - track performance over time
7. **Test at scale** - simulate high load
8. **Document changes** - track optimizations
