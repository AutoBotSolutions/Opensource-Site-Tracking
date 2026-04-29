# User Management Guide

This guide covers user management in OpenSite Analytics.

## Overview

OpenSite Analytics supports user authentication, role-based access, and team collaboration.

## User Roles

### Admin
- Full system access
- Manage all users
- Configure system settings
- Access all sites

### User
- Create and manage own sites
- View analytics for own sites
- Configure site settings

### Viewer (Future)
- Read-only access to assigned sites
- Cannot modify settings

## User Creation

### Via Registration

Users can self-register through the registration page:

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword"
  }'
```

### Via API

```python
# In main.py
@app.post("/api/users")
async def create_user(
    user: UserCreate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    # Admin only endpoint
    hashed_password = hash_password(user.password)
    new_user = User(email=user.email, password_hash=hashed_password)
    db.add(new_user)
    db.commit()
    return new_user
```

### Via Database

```python
from database import SessionLocal
from models import User
from auth import hash_password

db = SessionLocal()
user = User(
    email="admin@example.com",
    password_hash=hash_password("admin123")
)
db.add(user)
db.commit()
```

## User Authentication

### Login

```javascript
// Frontend login
const response = await fetch('/api/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'password'
  })
})

const { access_token, user } = await response.json()
localStorage.setItem('token', access_token)
```

### Token Validation

Tokens are validated on each request:

```python
# In auth.py
async def get_current_user(authorization: str = Header(None), db: Session = Depends(get_db)):
    token = authorization.split(" ")[1]
    payload = verify_token(token)
    user = db.query(User).filter(User.id == payload["sub"]).first()
    return user
```

## Password Management

### Password Reset (Future)

```python
@app.post("/api/auth/reset-password")
async def reset_password(email: str):
    # Generate reset token
    reset_token = generate_reset_token()
    
    # Send email
    send_reset_email(email, reset_token)
    
    return {"status": "email_sent"}
```

### Password Change

```python
@app.post("/api/auth/change-password")
async def change_password(
    old_password: str,
    new_password: str,
    current_user: User = Depends(get_current_user)
):
    if not verify_password(old_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect password")
    
    current_user.password_hash = hash_password(new_password)
    db.commit()
    
    return {"status": "password_changed"}
```

## User Permissions

### Site Ownership

Users can only access sites they own:

```python
@app.get("/api/sites/{site_id}")
async def get_site(
    site_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    site = db.query(Site).filter(
        Site.id == site_id,
        Site.owner_id == current_user.id
    ).first()
    
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    return site
```

### Admin Override

Admins can access all sites:

```python
async def get_current_admin_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user
```

## Team Collaboration (Future)

### Team Creation

```python
@app.post("/api/teams")
async def create_team(
    team: TeamCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    team = Team(
        name=team.name,
        owner_id=current_user.id
    )
    db.add(team)
    db.commit()
    return team
```

### Team Member Management

```python
@app.post("/api/teams/{team_id}/members")
async def add_team_member(
    team_id: int,
    user_id: int,
    role: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    member = TeamMember(
        team_id=team_id,
        user_id=user_id,
        role=role
    )
    db.add(member)
    db.commit()
    return member
```

## User Activity Tracking

### Login History

```python
class LoginHistory(Base):
    __tablename__ = "login_history"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    ip_address = Column(String(45))
    user_agent = Column(String(255))
    login_time = Column(DateTime, default=datetime.utcnow)
```

### Activity Logs

```python
@app.middleware("http")
async def log_activity(request: Request, call_next):
    response = await call_next(request)
    
    if request.url.path.startswith("/api/"):
        log_activity(
            user_id=get_user_id_from_token(request),
            endpoint=request.url.path,
            method=request.method,
            status_code=response.status_code
        )
    
    return response
```

## Security Best Practices

1. **Strong passwords** - Enforce complexity requirements
2. **Rate limiting** - Prevent brute force attacks
3. **Secure sessions** - Use httpOnly cookies
4. **Two-factor authentication** - Optional 2FA
5. **Audit logs** - Track user actions
6. **Regular password updates** - Prompt users to change passwords
7. **Account lockout** - After failed attempts
8. **Secure password storage** - Always use bcrypt

## Troubleshooting

### Login Issues

**Problem:** User cannot login

**Solutions:**
1. Verify email and password are correct
2. Check if account is active
3. Verify JWT token configuration
4. Check browser console for errors

### Permission Issues

**Problem:** User cannot access site

**Solutions:**
1. Verify user owns the site
2. Check if user is admin
3. Verify token is valid
4. Check site ownership in database

## Best Practices

1. Use strong, unique passwords
2. Enable 2FA for admin accounts
3. Regular security audits
4. Monitor login attempts
5. Review user permissions
6. Document user roles
7. Implement password policies
8. Regular password rotations
