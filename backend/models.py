from sqlalchemy import Column, Integer, String, DateTime, Text, Float, Boolean, ForeignKey, Index
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    sites = relationship("Site", back_populates="owner", cascade="all, delete-orphan")


class Site(Base):
    __tablename__ = "sites"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    domain = Column(String, unique=True, nullable=False, index=True)
    site_key = Column(String, unique=True, nullable=False, index=True)
    api_key = Column(String, unique=True, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    owner = relationship("User", back_populates="sites")
    pageviews = relationship("PageView", back_populates="site", cascade="all, delete-orphan")
    events = relationship("Event", back_populates="site", cascade="all, delete-orphan")
    sessions = relationship("Session", back_populates="site", cascade="all, delete-orphan")


class PageView(Base):
    __tablename__ = "pageviews"
    
    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey("sites.id"), nullable=False, index=True)
    session_id = Column(String, index=True)
    url = Column(Text, nullable=False)
    title = Column(String)
    referrer = Column(Text)
    user_agent = Column(String)
    ip_address = Column(String)
    country = Column(String)
    city = Column(String)
    browser = Column(String)
    os = Column(String)
    device = Column(String)
    screen_resolution = Column(String)
    language = Column(String)
    duration = Column(Integer, default=0)  # Time on page in seconds
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    site = relationship("Site", back_populates="pageviews")
    
    # Indexes for common queries
    __table_args__ = (
        Index('idx_pageviews_site_created', 'site_id', 'created_at'),
        Index('idx_pageviews_session', 'session_id'),
    )


class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey("sites.id"), nullable=False, index=True)
    session_id = Column(String, index=True)
    event_name = Column(String, nullable=False, index=True)
    event_category = Column(String)
    event_data = Column(Text)  # JSON string for additional data
    url = Column(Text)
    user_agent = Column(String)
    ip_address = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    site = relationship("Site", back_populates="events")
    
    # Indexes for common queries
    __table_args__ = (
        Index('idx_events_site_created', 'site_id', 'created_at'),
        Index('idx_events_name', 'event_name'),
    )


class Session(Base):
    __tablename__ = "sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey("sites.id"), nullable=False, index=True)
    session_key = Column(String, unique=True, nullable=False, index=True)
    ip_address = Column(String)
    user_agent = Column(String)
    browser = Column(String)
    os = Column(String)
    device = Column(String)
    country = Column(String)
    city = Column(String)
    landing_page = Column(Text)
    exit_page = Column(Text)
    page_views = Column(Integer, default=0)
    duration = Column(Integer, default=0)  # Session duration in seconds
    is_bounce = Column(Boolean, default=False)  # Single page session
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    site = relationship("Site", back_populates="sessions")
    
    # Indexes for common queries
    __table_args__ = (
        Index('idx_sessions_site_created', 'site_id', 'created_at'),
        Index('idx_sessions_key', 'session_key'),
    )


class Goal(Base):
    __tablename__ = "goals"
    
    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey("sites.id"), nullable=False, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    goal_type = Column(String, nullable=False)  # 'pageview', 'event', 'custom'
    target_value = Column(String)  # URL for pageview, event_name for event
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    site = relationship("Site")
