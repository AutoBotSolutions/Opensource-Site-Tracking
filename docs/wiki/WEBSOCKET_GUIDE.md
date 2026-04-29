# WebSocket Guide

This guide explains how to use WebSockets for real-time analytics updates in OpenSite Analytics.

## Overview

OpenSite Analytics supports real-time updates via WebSocket connections, allowing you to:
- Receive live page view events
- Track custom events in real-time
- Monitor visitor counts
- Get goal completion notifications

## WebSocket Endpoint

**URL:** `ws://localhost:8000/ws/{site_id}`

**Authentication:** JWT token in query parameter or header

## Connection

### Basic Connection

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/1?token=YOUR_JWT_TOKEN')

ws.onopen = () => {
  console.log('WebSocket connected')
}

ws.onmessage = (event) => {
  const data = JSON.parse(event.data)
  console.log('Received:', data)
}

ws.onerror = (error) => {
  console.error('WebSocket error:', error)
}

ws.onclose = () => {
  console.log('WebSocket disconnected')
}
```

### Authentication

**Method 1: Query Parameter**
```javascript
const token = localStorage.getItem('token')
const ws = new WebSocket(`ws://localhost:8000/ws/1?token=${token}`)
```

**Method 2: Header (if supported)**
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/1')
// Note: Headers in WebSocket handshake is limited, query param is preferred
```

## Event Types

### Page View Events

```json
{
  "type": "pageview",
  "data": {
    "id": 123,
    "url": "/about",
    "title": "About Us",
    "referrer": "https://google.com",
    "user_agent": "Mozilla/5.0...",
    "country": "US",
    "timestamp": "2026-04-29T12:00:00Z"
  }
}
```

### Custom Events

```json
{
  "type": "event",
  "data": {
    "id": 456,
    "event_name": "signup",
    "event_data": {
      "plan": "pro"
    },
    "timestamp": "2026-04-29T12:00:00Z"
  }
}
```

### Visitor Count Updates

```json
{
  "type": "visitor_count",
  "data": {
    "current": 42,
    "total_today": 1234
  }
}
```

### Goal Completions

```json
{
  "type": "goal",
  "data": {
    "goal_id": 1,
    "goal_name": "Newsletter Signup",
    "timestamp": "2026-04-29T12:00:00Z"
  }
}
```

## Frontend Implementation

### React Hook

```typescript
import { useEffect, useRef } from 'react'

interface WebSocketMessage {
  type: string
  data: any
}

export function useWebSocket(siteId: number, token: string) {
  const wsRef = useRef<WebSocket | null>(null)
  const listeners = useRef<Map<string, Function[]>>(new Map())

  useEffect(() => {
    const ws = new WebSocket(`ws://localhost:8000/ws/${siteId}?token=${token}`)
    
    ws.onopen = () => {
      console.log('WebSocket connected')
    }

    ws.onmessage = (event) => {
      const message: WebSocketMessage = JSON.parse(event.data)
      const eventListeners = listeners.current.get(message.type) || []
      eventListeners.forEach(callback => callback(message.data))
    }

    ws.onerror = (error) => {
      console.error('WebSocket error:', error)
    }

    ws.onclose = () => {
      console.log('WebSocket disconnected')
    }

    wsRef.current = ws

    return () => {
      ws.close()
    }
  }, [siteId, token])

  const on = (type: string, callback: Function) => {
    const currentListeners = listeners.current.get(type) || []
    listeners.current.set(type, [...currentListeners, callback])
  }

  const off = (type: string, callback: Function) => {
    const currentListeners = listeners.current.get(type) || []
    listeners.current.set(type, currentListeners.filter(cb => cb !== callback))
  }

  return { on, off }
}
```

### Usage Example

```typescript
function LiveAnalytics({ siteId }: { siteId: number }) {
  const token = localStorage.getItem('token') || ''
  const { on, off } = useWebSocket(siteId, token)
  const [pageviews, setPageviews] = useState([])

  useEffect(() => {
    const handlePageview = (data: any) => {
      setPageviews(prev => [data, ...prev].slice(0, 10))
    }

    on('pageview', handlePageview)

    return () => off('pageview', handlePageview)
  }, [on, off])

  return (
    <div>
      <h2>Live Page Views</h2>
      {pageviews.map(pv => (
        <div key={pv.id}>{pv.url}</div>
      ))}
    </div>
  )
}
```

## Backend Implementation

### WebSocket Endpoint

```python
from fastapi import WebSocket, WebSocketDisconnect
from typing import List

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, site_id: int):
        await websocket.accept()
        if site_id not in self.active_connections:
            self.active_connections[site_id] = []
        self.active_connections[site_id].append(websocket)

    def disconnect(self, websocket: WebSocket, site_id: int):
        if site_id in self.active_connections:
            self.active_connections[site_id].remove(websocket)
            if not self.active_connections[site_id]:
                del self.active_connections[site_id]

    async def broadcast(self, message: dict, site_id: int):
        if site_id in self.active_connections:
            for connection in self.active_connections[site_id]:
                try:
                    await connection.send_json(message)
                except:
                    await self.disconnect(connection, site_id)

manager = ConnectionManager()

@app.websocket("/ws/{site_id}")
async def websocket_endpoint(websocket: WebSocket, site_id: int):
    await manager.connect(websocket, site_id)
    try:
        while True:
            data = await websocket.receive_text()
            # Handle incoming messages if needed
    except WebSocketDisconnect:
        manager.disconnect(websocket, site_id)
```

### Broadcasting Events

```python
# When tracking a page view
async def broadcast_pageview(pageview: PageView):
    await manager.broadcast({
        "type": "pageview",
        "data": {
            "id": pageview.id,
            "url": pageview.url,
            "title": pageview.title,
            "referrer": pageview.referrer,
            "country": pageview.country,
            "timestamp": pageview.created_at.isoformat()
        }
    }, pageview.site_id)

# When tracking an event
async def broadcast_event(event: Event):
    await manager.broadcast({
        "type": "event",
        "data": {
            "id": event.id,
            "event_name": event.event_name,
            "event_data": event.event_data,
            "timestamp": event.created_at.isoformat()
        }
    }, event.site_id)
```

## Reconnection Strategy

### Automatic Reconnection

```typescript
function useWebSocketWithReconnect(siteId: number, token: string) {
  const wsRef = useRef<WebSocket | null>(null)
  const reconnectTimeoutRef = useRef<NodeJS.Timeout>()

  const connect = () => {
    const ws = new WebSocket(`ws://localhost:8000/ws/${siteId}?token=${token}`)
    
    ws.onopen = () => {
      console.log('WebSocket connected')
    }

    ws.onclose = () => {
      console.log('WebSocket disconnected, reconnecting in 5s...')
      reconnectTimeoutRef.current = setTimeout(connect, 5000)
    }

    ws.onerror = (error) => {
      console.error('WebSocket error:', error)
    }

    wsRef.current = ws
  }

  useEffect(() => {
    connect()

    return () => {
      clearTimeout(reconnectTimeoutRef.current)
      if (wsRef.current) {
        wsRef.current.close()
      }
    }
  }, [siteId, token])
}
```

### Exponential Backoff

```typescript
function useWebSocketWithBackoff(siteId: number, token: string) {
  const [retryCount, setRetryCount] = useState(0)
  const maxRetries = 5
  const baseDelay = 1000 // 1 second

  const connect = () => {
    const delay = Math.min(baseDelay * Math.pow(2, retryCount), 30000)
    
    setTimeout(() => {
      const ws = new WebSocket(`ws://localhost:8000/ws/${siteId}?token=${token}`)
      
      ws.onopen = () => {
        setRetryCount(0)
        console.log('WebSocket connected')
      }

      ws.onclose = () => {
        if (retryCount < maxRetries) {
          setRetryCount(prev => prev + 1)
          connect()
        }
      }

      wsRef.current = ws
    }, delay)
  }
}
```

## Performance Considerations

### Connection Limits

- Limit concurrent WebSocket connections per site
- Implement connection pooling for large deployments
- Monitor memory usage

### Message Throttling

```python
import asyncio
from collections import deque

class ThrottledConnectionManager:
    def __init__(self, max_messages_per_second: int = 10):
        self.manager = ConnectionManager()
        self.max_messages = max_messages_per_second
        self.message_queues: dict[int, deque] = {}

    async def broadcast_throttled(self, message: dict, site_id: int):
        if site_id not in self.message_queues:
            self.message_queues[site_id] = deque()
        
        self.message_queues[site_id].append(message)
        
        if len(self.message_queues[site_id]) >= self.max_messages:
            batch = list(self.message_queues[site_id])
            self.message_queues[site_id].clear()
            await self.manager.broadcast({"type": "batch", "data": batch}, site_id)
```

### Load Balancing

For horizontal scaling:
- Use Redis pub/sub for WebSocket message distribution
- Implement sticky sessions
- Use WebSocket-aware load balancer (nginx, HAProxy)

## Security

### Token Validation

```python
@app.websocket("/ws/{site_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    site_id: int,
    token: str = Query(...)
):
    # Validate token
    try:
        payload = verify_token(token)
        user_id = payload.get("sub")
    except:
        await websocket.close(code=1008, reason="Invalid token")
        return
    
    # Verify site ownership
    db = SessionLocal()
    site = db.query(Site).filter(
        Site.id == site_id,
        Site.owner_id == user_id
    ).first()
    
    if not site:
        await websocket.close(code=1008, reason="Site not found")
        return
    
    await manager.connect(websocket, site_id)
    # ... rest of implementation
```

### Rate Limiting

```python
from collections import defaultdict
import time

class WebSocketRateLimiter:
    def __init__(self, max_connections: int = 100, time_window: int = 60):
        self.max_connections = max_connections
        self.time_window = time_window
        self.connections: defaultdict[int, List[float]] = defaultdict(list)

    def can_connect(self, user_id: int) -> bool:
        now = time.time()
        # Remove old connections
        self.connections[user_id] = [
            t for t in self.connections[user_id]
            if now - t < self.time_window
        ]
        
        if len(self.connections[user_id]) >= self.max_connections:
            return False
        
        self.connections[user_id].append(now)
        return True
```

## Troubleshooting

### Connection Issues

**Problem:** WebSocket connection fails

**Solutions:**
1. Check if backend is running
2. Verify token is valid
3. Check firewall settings
4. Ensure WebSocket support is enabled in load balancer
5. Check browser console for errors

### Disconnection Issues

**Problem:** Frequent disconnections

**Solutions:**
1. Implement reconnection logic
2. Check network stability
3. Verify server timeout settings
4. Monitor server resources
5. Check for proxy timeout

### Performance Issues

**Problem:** High memory usage

**Solutions:**
1. Implement message throttling
2. Limit message history
3. Use connection pooling
4. Monitor and disconnect idle connections
5. Implement load balancing

## Best Practices

1. **Always implement reconnection logic** for production use
2. **Use exponential backoff** for reconnection attempts
3. **Limit message frequency** to prevent overwhelming clients
4. **Validate tokens** before establishing connections
5. **Monitor connection counts** and implement limits
6. **Handle errors gracefully** with proper error messages
7. **Use compression** for large payloads
8. **Implement heartbeats** to detect dead connections
9. **Log connection events** for debugging
10. **Test under load** to identify bottlenecks
