from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, Dict, Any
from datetime import datetime


# Site schemas
class SiteBase(BaseModel):
    name: str
    domain: str


class SiteCreate(SiteBase):
    pass


class SiteResponse(SiteBase):
    id: int
    site_key: str
    api_key: str
    created_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True


# PageView schemas
class PageViewBase(BaseModel):
    site_id: int
    api_key: str
    url: str
    title: Optional[str] = None
    referrer: Optional[str] = None
    user_agent: Optional[str] = None
    ip_address: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    browser: Optional[str] = None
    os: Optional[str] = None
    device: Optional[str] = None
    screen_resolution: Optional[str] = None
    language: Optional[str] = None
    session_id: Optional[str] = None
    utm_source: Optional[str] = None
    utm_medium: Optional[str] = None
    utm_campaign: Optional[str] = None
    utm_term: Optional[str] = None
    utm_content: Optional[str] = None


class PageViewCreate(PageViewBase):
    pass


class PageViewResponse(PageViewBase):
    id: int
    created_at: datetime
    duration: int = 0
    
    class Config:
        from_attributes = True


# Event schemas
class EventBase(BaseModel):
    site_id: int
    api_key: str
    event_name: str
    event_category: Optional[str] = None
    event_data: Optional[Dict[str, Any]] = None
    url: Optional[str] = None
    user_agent: Optional[str] = None
    ip_address: Optional[str] = None
    session_id: Optional[str] = None


class EventCreate(EventBase):
    pass


class EventResponse(EventBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Session schemas
class SessionBase(BaseModel):
    site_id: int
    session_key: str
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    browser: Optional[str] = None
    os: Optional[str] = None
    device: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    landing_page: Optional[str] = None
    exit_page: Optional[str] = None


class SessionCreate(SessionBase):
    pass


class SessionResponse(SessionBase):
    id: int
    page_views: int
    duration: int
    is_bounce: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# User schemas
class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


# Goal schemas
class GoalBase(BaseModel):
    name: str
    description: Optional[str] = None
    goal_type: str
    target_value: Optional[str] = None


class GoalCreate(GoalBase):
    site_id: int


class GoalResponse(GoalBase):
    id: int
    site_id: int
    created_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True


# Analytics schemas
class AnalyticsSummary(BaseModel):
    site_id: int
    period: str
    total_pageviews: int
    unique_visitors: int
    total_sessions: int
    bounce_rate: float
    avg_session_duration: float
    top_pages: list
    top_referrers: list
    device_breakdown: Dict[str, int]
    browser_breakdown: Dict[str, int]
    country_breakdown: Dict[str, int]


class AnalyticsResponse(BaseModel):
    summary: AnalyticsSummary
    pageviews_over_time: list
    events_summary: list
