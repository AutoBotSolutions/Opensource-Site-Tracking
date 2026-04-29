# Site Management Guide

This guide covers site management in OpenSite Analytics.

## Overview

Sites represent the websites you want to track. Each site has unique tracking keys and API keys.

## Creating Sites

### Via Dashboard

1. Login to dashboard
2. Click "New Site"
3. Enter site name and domain
4. Click "Create Site"

### Via API

```bash
curl -X POST http://localhost:8000/api/sites \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Website",
    "domain": "example.com"
  }'
```

### Response

```json
{
  "id": 1,
  "name": "My Website",
  "domain": "example.com",
  "site_key": "abc123...",
  "api_key": "xyz789...",
  "created_at": "2026-04-29T12:00:00",
  "is_active": true
}
```

## Site Configuration

### Site Settings

```python
class SiteSettings(Base):
    __tablename__ = "site_settings"
    
    id = Column(Integer, primary_key=True)
    site_id = Column(Integer, ForeignKey("sites.id"))
    timezone = Column(String(50), default="UTC")
    exclude_bots = Column(Boolean, default=True)
    anonymize_ip = Column(Boolean, default=False)
    custom_domain = Column(String(255))
```

### Update Settings

```python
@app.put("/api/sites/{site_id}/settings")
async def update_site_settings(
    site_id: int,
    settings: SiteSettingsUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    site = db.query(Site).filter(
        Site.id == site_id,
        Site.owner_id == current_user.id
    ).first()
    
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    # Update settings
    for key, value in settings.dict().items():
        setattr(site, key, value)
    
    db.commit()
    return site
```

## Site Keys

### Site Key (Public)

Used in the tracking script to identify the site:

```html
<script>
  OpenSite("init", "YOUR_SITE_KEY", "YOUR_API_KEY");
</script>
```

### API Key (Private)

Used for server-to-server API calls:

```python
import requests

headers = {
    "X-API-Key": "YOUR_API_KEY"
}

response = requests.post(
    "http://localhost:8000/api/track/pageview",
    headers=headers,
    json={...}
)
```

### Regenerate Keys

```python
@app.post("/api/sites/{site_id}/regenerate-keys")
async def regenerate_keys(
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
    
    site.site_key = generate_site_key()
    site.api_key = generate_api_key()
    db.commit()
    
    return site
```

## Site Status

### Activate/Deactivate Site

```python
@app.patch("/api/sites/{site_id}/status")
async def toggle_site_status(
    site_id: int,
    is_active: bool,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    site = db.query(Site).filter(
        Site.id == site_id,
        Site.owner_id == current_user.id
    ).first()
    
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    site.is_active = is_active
    db.commit()
    
    return {"status": "updated", "is_active": is_active}
```

### Delete Site

```python
@app.delete("/api/sites/{site_id}")
async def delete_site(
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
    
    # Delete associated data
    db.query(PageView).filter(PageView.site_id == site_id).delete()
    db.query(Event).filter(Event.site_id == site_id).delete()
    db.query(Goal).filter(Goal.site_id == site_id).delete()
    
    db.delete(site)
    db.commit()
    
    return {"status": "deleted"}
```

## Site Analytics

### Data Retention

Configure data retention per site:

```python
class SiteRetention(Base):
    __tablename__ = "site_retention"
    
    id = Column(Integer, primary_key=True)
    site_id = Column(Integer, ForeignKey("sites.id"))
    retention_days = Column(Integer, default=90)
```

### Export Data

```python
@app.get("/api/sites/{site_id}/export")
async def export_site_data(
    site_id: int,
    format: str = "csv",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    site = db.query(Site).filter(
        Site.id == site_id,
        Site.owner_id == current_user.id
    ).first()
    
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    # Export data
    if format == "csv":
        return export_to_csv(site_id)
    elif format == "json":
        return export_to_json(site_id)
```

## Multi-Domain Tracking

### Subdomains

Track subdomains as separate sites or same site:

```python
# Same site with subdomain tracking
site = Site(
    name="Main Site",
    domain="example.com",
    include_subdomains=True
)
```

### Multiple Domains

Track multiple domains under one site:

```python
# Add custom domain
@app.post("/api/sites/{site_id}/domains")
async def add_custom_domain(
    site_id: int,
    domain: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    custom_domain = CustomDomain(
        site_id=site_id,
        domain=domain
    )
    db.add(custom_domain)
    db.commit()
    return custom_domain
```

## Site Verification

### Domain Verification

Verify domain ownership before allowing tracking:

```python
@app.post("/api/sites/{site_id}/verify")
async def verify_domain(
    site_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    site = db.query(Site).filter(Site.id == site_id).first()
    
    # Check DNS TXT record
    verification_code = generate_verification_code()
    site.verification_code = verification_code
    db.commit()
    
    return {
        "verification_code": verification_code,
        "instruction": f"Add TXT record: opensite-verify={verification_code}"
    }
```

## Best Practices

1. Use descriptive site names
2. Verify domain ownership
3. Keep API keys secure
4. Regularly rotate keys
5. Monitor site activity
6. Set appropriate data retention
7. Use subdomain strategy wisely
8. Document site configurations
9. Test tracking after setup
10. Review site permissions regularly
