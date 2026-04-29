import secrets
import hashlib
from datetime import datetime, timedelta
from typing import Optional
from user_agents import parse


def generate_site_key() -> str:
    """Generate a unique site key"""
    return secrets.token_urlsafe(16)


def generate_api_key() -> str:
    """Generate a unique API key"""
    return secrets.token_urlsafe(32)


def generate_session_key() -> str:
    """Generate a unique session key"""
    return secrets.token_urlsafe(24)


def parse_user_agent(user_agent_string: str) -> dict:
    """Parse user agent string to extract browser, OS, and device info"""
    try:
        ua = parse(user_agent_string)
        return {
            "browser": f"{ua.browser.family} {ua.browser.version_string}",
            "os": f"{ua.os.family} {ua.os.version_string}",
            "device": "Mobile" if ua.is_mobile else "Tablet" if ua.is_tablet else "Desktop"
        }
    except Exception:
        return {
            "browser": "Unknown",
            "os": "Unknown",
            "device": "Unknown"
        }


def get_client_ip(request) -> str:
    """Get client IP address from request"""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def hash_ip(ip_address: str) -> str:
    """Hash IP address for privacy (GDPR compliant)"""
    return hashlib.sha256(ip_address.encode()).hexdigest()[:16]


def calculate_bounce_rate(sessions: list) -> float:
    """Calculate bounce rate from sessions"""
    if not sessions:
        return 0.0
    bounces = sum(1 for s in sessions if s.is_bounce)
    return (bounces / len(sessions)) * 100


def calculate_avg_duration(sessions: list) -> float:
    """Calculate average session duration in seconds"""
    if not sessions:
        return 0.0
    total_duration = sum(s.duration for s in sessions)
    return total_duration / len(sessions)


def get_date_range(period: str) -> tuple:
    """Get start and end date for a given period"""
    now = datetime.utcnow()
    
    if period == "today":
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = now
    elif period == "yesterday":
        start = (now - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        end = now.replace(hour=0, minute=0, second=0, microsecond=0)
    elif period == "7days":
        start = now - timedelta(days=7)
        end = now
    elif period == "30days":
        start = now - timedelta(days=30)
        end = now
    elif period == "90days":
        start = now - timedelta(days=90)
        end = now
    else:  # default to 7 days
        start = now - timedelta(days=7)
        end = now
    
    return start, end
