from fastapi import FastAPI, Depends, HTTPException, Request, WebSocket, WebSocketDisconnect, Query, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from database import engine, Base, SessionLocal, get_db
from models import Site, PageView, Event, Session, User, Goal
from schemas import (
    SiteCreate, SiteResponse, 
    PageViewCreate, PageViewResponse,
    EventCreate, EventResponse,
    AnalyticsResponse, AnalyticsSummary,
    UserCreate, UserLogin, UserResponse, Token,
    GoalCreate, GoalResponse
)
from auth import (
    get_password_hash, verify_password, create_access_token,
    get_current_active_user, verify_token
)
from utils import (
    generate_site_key, generate_api_key, generate_session_key,
    parse_user_agent, get_client_ip, hash_ip,
    calculate_bounce_rate, calculate_avg_duration, get_date_range
)
from geoip import geoip_service
from config import settings
from rate_limit import rate_limit
from tasks import start_scheduler

# Create FastAPI app
app = FastAPI(
    title="OpenSite Analytics API",
    description="Self-hosted analytics platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root route
@app.get("/")
async def root():
    return {
        "message": "OpenSite Analytics API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

# Create database tables on startup
@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)
    start_scheduler()


# Health check
@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


# Authentication endpoints
@app.post("/api/auth/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if user already exists
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    new_user = User(
        email=user.email,
        password_hash=get_password_hash(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@app.post("/api/auth/login", response_model=Token)
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """Login and get access token"""
    # Verify user
    user = db.query(User).filter(User.email == user_credentials.email).first()
    if not user or not verify_password(user_credentials.password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password"
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": user.id})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


@app.get("/api/auth/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    """Get current user info"""
    return current_user


# Site management endpoints
@app.post("/api/sites", response_model=SiteResponse)
def create_site(site: SiteCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """Create a new site for tracking"""
    # Check if domain already exists for this user
    existing = db.query(Site).filter(Site.domain == site.domain, Site.owner_id == current_user.id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Domain already registered")
    
    new_site = Site(
        name=site.name,
        domain=site.domain,
        site_key=generate_site_key(),
        api_key=generate_api_key(),
        owner_id=current_user.id
    )
    db.add(new_site)
    db.commit()
    db.refresh(new_site)
    return new_site


@app.get("/api/sites", response_model=List[SiteResponse])
async def list_sites(current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """List all sites for current user"""
    return db.query(Site).filter(Site.owner_id == current_user.id).all()


@app.get("/api/sites/{site_id}", response_model=SiteResponse)
async def get_site(site_id: int, current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """Get a specific site"""
    site = db.query(Site).filter(
        Site.id == site_id,
        Site.owner_id == current_user.id
    ).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    return site


# Tracking endpoints
@app.post("/api/track/pageview")
@rate_limit(limit=200)  # Higher limit for tracking
async def track_pageview(pageview: PageViewCreate, request: Request, db: Session = Depends(get_db)):
    """Track a page view"""
    # Verify API key
    site = db.query(Site).filter(
        Site.id == pageview.site_id,
        Site.api_key == pageview.api_key,
        Site.is_active == True
    ).first()
    
    if not site:
        raise HTTPException(status_code=401, detail="Invalid site ID or API key")
    
    # Get client IP
    ip_address = pageview.ip_address or get_client_ip(request)
    hashed_ip = hash_ip(ip_address)
    
    # Get geographic location (if not provided)
    country = pageview.country
    city = pageview.city
    if not country or not city:
        geo_data = geoip_service.get_location(ip_address)
        country = geo_data.get('country') or country
        city = geo_data.get('city') or city
    
    # Parse user agent
    ua_info = parse_user_agent(pageview.user_agent or "") if pageview.user_agent else {}
    browser = ua_info.get("browser") or pageview.browser
    os = ua_info.get("os") or pageview.os
    device = ua_info.get("device") or pageview.device
    
    # Handle session
    session_key = pageview.session_id or generate_session_key()
    session = db.query(Session).filter(Session.session_key == session_key).first()
    
    if not session:
        # Create new session
        session = Session(
            site_id=site.id,
            session_key=session_key,
            ip_address=hashed_ip,
            user_agent=pageview.user_agent,
            browser=browser,
            os=os,
            device=device,
            country=pageview.country,
            city=pageview.city,
            landing_page=pageview.url,
            page_views=1,
            is_bounce=True
        )
        db.add(session)
    else:
        # Update existing session
        session.page_views += 1
        session.exit_page = pageview.url
        session.is_bounce = False
        session.updated_at = datetime.utcnow()
    
    db.commit()
    
    # Create page view record
    new_pageview = PageView(
        site_id=site.id,
        session_id=session_key,
        url=pageview.url,
        title=pageview.title,
        referrer=pageview.referrer,
        user_agent=pageview.user_agent,
        ip_address=hashed_ip,
        country=pageview.country,
        city=pageview.city,
        browser=browser,
        os=os,
        device=device,
        screen_resolution=pageview.screen_resolution,
        language=pageview.language
    )
    
    db.add(new_pageview)
    db.commit()
    
    # Broadcast real-time update via WebSocket
    await manager.broadcast_pageview(site.id, {
        "url": new_pageview.url,
        "title": new_pageview.title,
        "browser": new_pageview.browser,
        "device": new_pageview.device,
        "country": new_pageview.country,
        "created_at": new_pageview.created_at.isoformat()
    })
    
    return {"status": "success", "session_id": session_key}


@rate_limit(limit=200)  # Higher limit for tracking
@app.post("/api/track/event")
async def track_event(event: EventCreate, request: Request, db: Session = Depends(get_db)):
    """Track a custom event"""
    # Verify API key
    site = db.query(Site).filter(
        Site.id == event.site_id,
        Site.api_key == event.api_key,
        Site.is_active == True
    ).first()
    
    if not site:
        raise HTTPException(status_code=401, detail="Invalid site ID or API key")
    
    # Get client IP
    ip_address = event.ip_address or get_client_ip(request)
    hashed_ip = hash_ip(ip_address)
    
    # Create event record
    new_event = Event(
        site_id=site.id,
        session_id=event.session_id,
        event_name=event.event_name,
        event_category=event.event_category,
        event_data=json.dumps(event.event_data) if event.event_data else None,
        url=event.url,
        user_agent=event.user_agent,
        ip_address=hashed_ip
    )
    
    db.add(new_event)
    db.commit()
    
    # Broadcast real-time update via WebSocket
    await manager.broadcast_event(site.id, {
        "event_name": new_event.event_name,
        "event_category": new_event.event_category,
        "url": new_event.url,
        "created_at": new_event.created_at.isoformat()
    })
    
    return {"status": "success"}


# Analytics endpoints
@app.get("/api/analytics/{site_id}", response_model=AnalyticsResponse)
def get_analytics(
    site_id: int, 
    period: str = "7days",
    db: Session = Depends(get_db)
):
    """Get analytics summary for a site"""
    # Verify site exists
    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    # Get date range
    start_date, end_date = get_date_range(period)
    
    # Query pageviews
    pageviews = db.query(PageView).filter(
        PageView.site_id == site_id,
        PageView.created_at >= start_date,
        PageView.created_at <= end_date
    ).all()
    
    # Query sessions
    sessions = db.query(Session).filter(
        Session.site_id == site_id,
        Session.created_at >= start_date,
        Session.created_at <= end_date
    ).all()
    
    # Query events
    events = db.query(Event).filter(
        Event.site_id == site_id,
        Event.created_at >= start_date,
        Event.created_at <= end_date
    ).all()
    
    # Calculate metrics
    total_pageviews = len(pageviews)
    unique_visitors = len(set(p.ip_address for p in pageviews))
    total_sessions = len(sessions)
    bounce_rate = calculate_bounce_rate(sessions)
    avg_session_duration = calculate_avg_duration(sessions)
    
    # Top pages
    page_counts = {}
    for pv in pageviews:
        page_counts[pv.url] = page_counts.get(pv.url, 0) + 1
    top_pages = sorted(page_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    
    # Top referrers
    referrer_counts = {}
    for pv in pageviews:
        if pv.referrer:
            referrer_counts[pv.referrer] = referrer_counts.get(pv.referrer, 0) + 1
    top_referrers = sorted(referrer_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    
    # Device breakdown
    device_breakdown = {}
    for pv in pageviews:
        device_breakdown[pv.device or "Unknown"] = device_breakdown.get(pv.device or "Unknown", 0) + 1
    
    # Browser breakdown
    browser_breakdown = {}
    for pv in pageviews:
        browser_breakdown[pv.browser or "Unknown"] = browser_breakdown.get(pv.browser or "Unknown", 0) + 1
    
    # Country breakdown
    country_breakdown = {}
    for pv in pageviews:
        country_breakdown[pv.country or "Unknown"] = country_breakdown.get(pv.country or "Unknown", 0) + 1
    
    # Pageviews over time (hourly for last 7 days)
    pageviews_over_time = []
    for i in range(7):
        day_start = start_date + timedelta(days=i)
        day_end = day_start + timedelta(days=1)
        day_count = db.query(PageView).filter(
            PageView.site_id == site_id,
            PageView.created_at >= day_start,
            PageView.created_at < day_end
        ).count()
        pageviews_over_time.append({
            "date": day_start.strftime("%Y-%m-%d"),
            "pageviews": day_count
        })
    
    # Events summary
    event_counts = {}
    for ev in events:
        event_counts[ev.event_name] = event_counts.get(ev.event_name, 0) + 1
    events_summary = sorted(event_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    
    return AnalyticsResponse(
        summary=AnalyticsSummary(
            site_id=site_id,
            period=period,
            total_pageviews=total_pageviews,
            unique_visitors=unique_visitors,
            total_sessions=total_sessions,
            bounce_rate=round(bounce_rate, 2),
            avg_session_duration=round(avg_session_duration, 2),
            top_pages=top_pages,
            top_referrers=top_referrers,
            device_breakdown=device_breakdown,
            browser_breakdown=browser_breakdown,
            country_breakdown=country_breakdown
        ),
        pageviews_over_time=pageviews_over_time,
        events_summary=events_summary
    )


# Goal management endpoints
@app.post("/api/goals", response_model=GoalResponse)
async def create_goal(goal: GoalCreate, current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """Create a new goal"""
    # Verify site ownership
    site = db.query(Site).filter(
        Site.id == goal.site_id,
        Site.owner_id == current_user.id
    ).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    new_goal = Goal(
        site_id=goal.site_id,
        name=goal.name,
        description=goal.description,
        goal_type=goal.goal_type,
        target_value=goal.target_value
    )
    db.add(new_goal)
    db.commit()
    db.refresh(new_goal)
    return new_goal


@app.get("/api/goals/{site_id}", response_model=List[GoalResponse])
async def list_goals(site_id: int, current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """List all goals for a site"""
    # Verify site ownership
    site = db.query(Site).filter(
        Site.id == site_id,
        Site.owner_id == current_user.id
    ).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    return db.query(Goal).filter(Goal.site_id == site_id).all()


# Tracking script endpoint
@app.get("/tracking-script.js", response_class=HTMLResponse)
def get_tracking_script():
    """Serve the tracking JavaScript SDK"""
    script = '''
(function(window, document) {
    'use strict';
    
    var OpenSite = window.OpenSite || function() {
        (OpenSite.q = OpenSite.q || []).push(arguments);
    };
    
    OpenSite.version = '1.0.0';
    
    var config = {
        siteId: null,
        apiKey: null,
        endpoint: window.location.protocol + '//' + window.location.hostname + ':8000/api/track',
        sessionId: null,
        queue: []
    };
    
    // Generate or retrieve session ID
    function getSessionId() {
        var sessionId = localStorage.getItem('opensite_session_id');
        if (!sessionId) {
            sessionId = 'sess_' + Math.random().toString(36).substr(2, 16) + Date.now().toString(36);
            localStorage.setItem('opensite_session_id', sessionId);
        }
        return sessionId;
    }
    
    // Get page info
    function getPageInfo() {
        // Extract UTM parameters from URL
        function getUTMParams() {
            var params = {};
            var searchParams = new URLSearchParams(window.location.search);
            ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content'].forEach(function(param) {
                if (searchParams.has(param)) {
                    params[param] = searchParams.get(param);
                }
            });
            return params;
        }
        
        var utmParams = getUTMParams();
        
        return {
            url: window.location.href,
            title: document.title,
            referrer: document.referrer,
            userAgent: navigator.userAgent,
            screenResolution: screen.width + 'x' + screen.height,
            language: navigator.language,
            utm_source: utmParams.utm_source || null,
            utm_medium: utmParams.utm_medium || null,
            utm_campaign: utmParams.utm_campaign || null,
            utm_term: utmParams.utm_term || null,
            utm_content: utmParams.utm_content || null
        };
    }
    
    // Send data to server
    function send(endpoint, data) {
        var xhr = new XMLHttpRequest();
        xhr.open('POST', endpoint, true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    try {
                        var response = JSON.parse(xhr.responseText);
                        if (response.session_id) {
                            config.sessionId = response.session_id;
                        }
                    } catch(e) {}
                }
                // Process next queued item
                if (config.queue.length > 0) {
                    var next = config.queue.shift();
                    send(next.endpoint, next.data);
                }
            }
        };
        xhr.send(JSON.stringify(data));
    }
    
    // Queue data for sending
    function queue(endpoint, data) {
        if (config.sessionId) {
            data.session_id = config.sessionId;
        } else {
            data.session_id = getSessionId();
        }
        
        if (navigator.sendBeacon) {
            var blob = new Blob([JSON.stringify(data)], {type: 'application/json'});
            navigator.sendBeacon(endpoint, blob);
        } else {
            config.queue.push({endpoint: endpoint, data: data});
            if (config.queue.length === 1) {
                send(endpoint, data);
            }
        }
    }
    
    // Initialize
    OpenSite('init', function(siteId, apiKey) {
        config.siteId = siteId;
        config.apiKey = apiKey;
    });
    
    // Track page view
    OpenSite('trackPageview', function() {
        var pageInfo = getPageInfo();
        
        var data = {
            site_id: config.siteId,
            api_key: config.apiKey,
            url: pageInfo.url,
            title: pageInfo.title,
            referrer: pageInfo.referrer,
            user_agent: pageInfo.userAgent,
            screen_resolution: pageInfo.screenResolution,
            language: pageInfo.language,
            session_id: config.sessionId || getSessionId(),
            utm_source: pageInfo.utm_source,
            utm_medium: pageInfo.utm_medium,
            utm_campaign: pageInfo.utm_campaign,
            utm_term: pageInfo.utm_term,
            utm_content: pageInfo.utm_content
        };
        queue(config.endpoint + '/pageview', data);
    });
    
    // Track event
    OpenSite('trackEvent', function(eventName, eventData) {
        var pageInfo = getPageInfo();
        queue(config.endpoint + '/event', {
            site_id: config.siteId,
            api_key: config.apiKey,
            event_name: eventName,
            event_data: eventData || {},
            url: pageInfo.url,
            user_agent: pageInfo.userAgent
        });
    });
    
    // Auto-track page view on load
    if (document.readyState === 'complete') {
        OpenSite('trackPageview');
    } else {
        window.addEventListener('load', function() {
            OpenSite('trackPageview');
        });
    }
    
    // Track page visibility changes
    document.addEventListener('visibilitychange', function() {
        if (document.visibilityState === 'hidden') {
            // Page is hidden, could track time on page
        }
    });
    
    window.OpenSite = OpenSite;
    
})(window, document);
    '''
    return script


# WebSocket endpoint for real-time updates
@app.websocket("/ws/{site_id}")
async def websocket_endpoint(websocket: WebSocket, site_id: int, token: str = Query(...), db: Session = Depends(get_db)):
    """WebSocket endpoint for real-time analytics updates"""
    await manager.connect(websocket, site_id)
    
    try:
        # Send initial connection message
        await websocket.send_json({
            "type": "connected",
            "site_id": site_id,
            "message": "Connected to real-time analytics"
        })
        
        # Keep connection alive and handle incoming messages
        while True:
            data = await websocket.receive_text()
            # Echo back or handle client messages if needed
            await websocket.send_json({
                "type": "echo",
                "data": data
            })
            
    except WebSocketDisconnect:
        manager.disconnect(websocket, site_id)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket, site_id)
# WebSocket endpoint for real-time updates
@app.websocket("/ws/{site_id}")
async def websocket_endpoint(websocket: WebSocket, site_id: int, token: str = Query(...), db: Session = Depends(get_db)):
    """WebSocket endpoint for real-time analytics updates"""
    await manager.connect(websocket, site_id)
    
    try:
        # Send initial connection message
        await websocket.send_json({
            "type": "connected",
            "site_id": site_id,
            "message": "Connected to real-time analytics"
        })
        
        # Keep connection alive and handle incoming messages
        while True:
            data = await websocket.receive_text()
            # Echo back or handle client messages if needed
            await websocket.send_json({
                "type": "echo",
                "data": data
            })
            
    except WebSocketDisconnect:
        manager.disconnect(websocket, site_id)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket, site_id)
