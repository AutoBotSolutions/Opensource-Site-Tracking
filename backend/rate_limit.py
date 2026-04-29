from fastapi import Request, HTTPException
from collections import defaultdict
import time
from typing import Dict
from functools import wraps

# Simple in-memory rate limiter
# For production, use Redis or similar
class RateLimiter:
    def __init__(self):
        self.requests: Dict[str, list] = defaultdict(list)
    
    def is_allowed(self, key: str, limit: int, window: int = 60) -> bool:
        """Check if request is allowed within rate limit"""
        now = time.time()
        # Remove old requests outside the window
        self.requests[key] = [t for t in self.requests[key] if t > now - window]
        
        if len(self.requests[key]) >= limit:
            return False
        
        self.requests[key].append(now)
        return True

# Global rate limiter instance
rate_limiter = RateLimiter()

def get_rate_limit_per_minute() -> int:
    """Get rate limit from environment or default"""
    import os
    return int(os.getenv('RATE_LIMIT_PER_MINUTE', '100'))

def rate_limit(limit: int = None):
    """Rate limiting decorator for endpoints"""
    if limit is None:
        limit = get_rate_limit_per_minute()
    
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Try to get client IP from request
            request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
            
            if request:
                # Get client IP (considering proxy headers)
                client_ip = request.headers.get('X-Forwarded-For', request.client.host if request.client else 'unknown')
                # If multiple IPs, take the first one
                client_ip = client_ip.split(',')[0].strip()
                
                if not rate_limiter.is_allowed(client_ip, limit):
                    raise HTTPException(status_code=429, detail="Rate limit exceeded")
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator
