# GeoIP Setup Guide

This guide explains how to set up GeoIP location detection in OpenSite Analytics.

## Overview

OpenSite Analytics uses GeoIP2 to detect visitor locations based on IP addresses. This requires:

- GeoIP2 database file
- Python geoip2 library
- Configuration in backend

## Installation

### Install Python Library

```bash
cd backend
pip3 install geoip2
```

### Download GeoIP Database

#### MaxMind GeoLite2 (Free)

1. Create a MaxMind account at https://www.maxmind.com
2. Generate a license key
3. Download the database:

```bash
mkdir -p backend/geoip
cd backend/geoip

# Download GeoLite2 City database
wget "https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-City&license_key=YOUR_LICENSE_KEY&suffix=tar.gz" -O GeoLite2-City.tar.gz

# Extract
tar -xzf GeoLite2-City.tar.gz
mv GeoLite2-City_*/GeoLite2-City.mmdb .
rm GeoLite2-City.tar.gz
rm -rf GeoLite2-City_*
```

#### Alternative: DB-IP (Free)

```bash
cd backend/geoip
wget https://download.db-ip.com/free/dbip-city-lite-2024-01.mmdb.gz
gunzip dbip-city-lite-2024-01.mmdb.gz
```

## Configuration

### Update Backend Configuration

Add to `backend/.env`:

```env
GEOIP_DATABASE_PATH=/path/to/GeoLite2-City.mmdb
```

### Update GeoIP Service

Edit `backend/geoip.py`:

```python
import geoip2.database
from pathlib import Path
from config import settings

class GeoIPService:
    def __init__(self):
        db_path = Path(settings.GEOIP_DATABASE_PATH)
        if db_path.exists():
            self.reader = geoip2.database.Reader(db_path)
        else:
            self.reader = None
            print("GeoIP database not found. Location detection disabled.")
    
    def get_location(self, ip_address: str) -> dict:
        """Get location information for IP address"""
        if not self.reader:
            return {"country": "Unknown", "city": "Unknown"}
        
        try:
            response = self.reader.city(ip_address)
            return {
                "country": response.country.iso_code or "Unknown",
                "city": response.city.name or "Unknown",
                "region": response.subdivisions.most_specific.name or "Unknown",
                "latitude": response.location.latitude,
                "longitude": response.location.longitude
            }
        except Exception as e:
            print(f"GeoIP lookup failed for {ip_address}: {e}")
            return {"country": "Unknown", "city": "Unknown"}
    
    def close(self):
        """Close the database reader"""
        if self.reader:
            self.reader.close()

# Global instance
geoip_service = GeoIPService()
```

### Update Tracking Endpoint

Edit `backend/main.py` to use GeoIP:

```python
from geoip import geoip_service

@app.post("/api/track/pageview")
async def track_pageview(pageview: PageViewCreate, db: Session = Depends(get_db)):
    # Get location from IP
    location = geoip_service.get_location(pageview.ip_address)
    
    # Create page view with location
    new_pageview = PageView(
        site_id=pageview.site_id,
        session_id=pageview.session_id,
        url=pageview.url,
        title=pageview.title,
        referrer=pageview.referrer,
        user_agent=pageview.user_agent,
        ip_address=pageview.ip_address,
        country=location["country"],
        city=location["city"],
        created_at=datetime.utcnow()
    )
    
    db.add(new_pageview)
    db.commit()
    
    return {"status": "success"}
```

## Database Updates

### Automatic Updates

Create a script to update the database automatically:

```bash
#!/bin/bash
# update_geoip.sh

GEOIP_DIR="/home/robbie/Desktop/opensource-site-tracking/backend/geoip"
LICENSE_KEY="YOUR_LICENSE_KEY"

cd "$GEOIP_DIR"

# Download new database
wget "https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-City&license_key=$LICENSE_KEY&suffix=tar.gz" -O GeoLite2-City.tar.gz.new

# Extract new database
mkdir -p temp
tar -xzf GeoLite2-City.tar.gz.new -C temp
mv temp/GeoLite2-City_*/GeoLite2-City.mmdb GeoLite2-City.mmdb.new
rm -rf temp GeoLite2-City.tar.gz.new

# Backup old database
mv GeoLite2-City.mmdb GeoLite2-City.mmdb.old

# Replace with new database
mv GeoLite2-City.mmdb.new GeoLite2-City.mmdb

echo "GeoIP database updated successfully"
```

Make executable and add to crontab:

```bash
chmod +x update_geoip.sh

# Update weekly on Tuesday at 3 AM
0 3 * * 2 /path/to/update_geoip.sh
```

## Testing

### Test GeoIP Lookup

```python
# test_geoip.py
from geoip import geoip_service

# Test with known IPs
test_ips = [
    "8.8.8.8",      # Google DNS (US)
    "1.1.1.1",      # Cloudflare DNS (US/Australia)
    "208.67.222.222" # OpenDNS (US)
]

for ip in test_ips:
    location = geoip_service.get_location(ip)
    print(f"{ip}: {location}")

geoip_service.close()
```

### Test with Tracking

```bash
# Test tracking with IP
curl -X POST http://localhost:8000/api/track/pageview \
  -H "Content-Type: application/json" \
  -d '{
    "site_id": 1,
    "api_key": "your-api-key",
    "url": "/test",
    "ip_address": "8.8.8.8"
  }'

# Check database for location data
python3 -c "
from database import SessionLocal
from models import PageView
db = SessionLocal()
pv = db.query(PageView).order_by(PageView.id.desc()).first()
print(f'Country: {pv.country}, City: {pv.city}')
db.close()
"
```

## Privacy Considerations

### IP Anonymization

To comply with GDPR, anonymize IP addresses:

```python
def anonymize_ip(ip: str) -> str:
    """Anonymize IP by setting last octet to 0"""
    try:
        parts = ip.split('.')
        if len(parts) == 4:
            parts[-1] = '0'
            return '.'.join(parts)
        return ip
    except:
        return ip

# Use in tracking
ip_address = anonymize_ip(pageview.ip_address)
```

### Consent Required

Add consent check before GeoIP lookup:

```python
def get_location_with_consent(ip_address: str, consent: bool) -> dict:
    if not consent:
        return {"country": "Unknown", "city": "Unknown"}
    return geoip_service.get_location(ip_address)
```

## Troubleshooting

### Database Not Found

**Problem:** `GeoIP database not found` error

**Solutions:**
1. Verify database path in `.env`
2. Check database file exists
3. Verify file permissions
4. Download database if missing

### Lookup Failures

**Problem:** GeoIP lookup returns "Unknown"

**Solutions:**
1. Check IP address format
2. Verify database is not corrupted
3. Test with known IP addresses
4. Check database is up to date

### Performance Issues

**Problem:** Slow page view tracking

**Solutions:**
1. Use caching for frequent IPs
2. Consider using a faster database (MMDB format)
3. Implement async lookup
4. Use CDN for database distribution

### Memory Usage

**Problem:** High memory usage

**Solutions:**
1. Use GeoLite2 Country database (smaller) instead of City
2. Implement database reader pool
3. Close reader when not in use
4. Use streaming for large datasets

## Advanced Configuration

### Custom Database Path

```python
# In config.py
class Settings(BaseSettings):
    GEOIP_DATABASE_PATH: str = "geoip/GeoLite2-City.mmdb"
    GEOIP_MODE: str = "city"  # or "country" for smaller database
```

### Fallback Database

```python
class GeoIPService:
    def __init__(self):
        self.reader = None
        self.fallback_reader = None
        
        # Try primary database
        try:
            self.reader = geoip2.database.Reader(settings.GEOIP_DATABASE_PATH)
        except:
            print("Primary GeoIP database not found")
        
        # Try fallback database
        try:
            self.fallback_reader = geoip2.database.Reader(settings.GEOIP_DATABASE_FALLBACK)
        except:
            print("Fallback GeoIP database not found")
    
    def get_location(self, ip_address: str) -> dict:
        # Try primary
        if self.reader:
            try:
                return self._lookup(self.reader, ip_address)
            except:
                pass
        
        # Try fallback
        if self.fallback_reader:
            try:
                return self._lookup(self.fallback_reader, ip_address)
            except:
                pass
        
        return {"country": "Unknown", "city": "Unknown"}
```

### Caching

```python
from functools import lru_cache
import time

class CachedGeoIPService:
    def __init__(self):
        self.reader = geoip2.database.Reader(settings.GEOIP_DATABASE_PATH)
        self.cache = {}
        self.cache_ttl = 3600  # 1 hour
    
    def get_location(self, ip_address: str) -> dict:
        # Check cache
        if ip_address in self.cache:
            cached_data, timestamp = self.cache[ip_address]
            if time.time() - timestamp < self.cache_ttl:
                return cached_data
        
        # Lookup
        location = self._lookup(ip_address)
        
        # Cache result
        self.cache[ip_address] = (location, time.time())
        
        return location
```

## Best Practices

1. **Update database regularly** - Monthly or weekly
2. **Use appropriate database** - Country database if city data not needed
3. **Handle errors gracefully** - Fallback to "Unknown"
4. **Respect privacy** - Anonymize IPs, require consent
5. **Monitor performance** - Cache frequent lookups
6. **Test regularly** - Verify database integrity
7. **Document configuration** - Keep settings documented
8. **Backup database** - Keep copy of working database
9. **Use CDN** - For distributed deployments
10. **Comply with regulations** - GDPR, CCPA compliance
