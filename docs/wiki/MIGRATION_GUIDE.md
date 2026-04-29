# Migration Guide

This guide covers migrating to OpenSite Analytics from other analytics platforms.

## Overview

This guide helps you migrate from:
- Google Analytics (GA4)
- Matomo
- Plausible
- Other analytics platforms

## Pre-Migration Checklist

- [ ] Install OpenSite Analytics
- [ ] Configure database
- [ ] Set up user accounts
- [ ] Test tracking code
- [ ] Plan migration timeline
- [ ] Notify team members
- [ ] Backup existing data
- [ ] Document current setup

## Google Analytics Migration

### Export Data from GA

#### Using Google Analytics API

```python
# export_ga_data.py
from google.analytics.data_v1beta import BetaAnalyticsDataClient
import pandas as pd

def export_ga_data(property_id, start_date, end_date):
    client = BetaAnalyticsDataClient()
    
    # Page views
    request = client.run_report(
        property=f"properties/{property_id}",
        dimensions=[{"name": "date"}, {"name": "pageTitle"}],
        metrics=[{"name": "screenPageViews"}],
        date_ranges=[{"start_date": start_date, "end_date": end_date}]
    )
    
    # Convert to DataFrame
    data = []
    for row in request.rows:
        data.append({
            'date': row.dimension_values[0].value,
            'page_title': row.dimension_values[1].value,
            'page_views': row.metric_values[0].value
        })
    
    df = pd.DataFrame(data)
    df.to_csv('ga_pageviews.csv', index=False)
    
    return df
```

#### Manual Export

1. Go to Google Analytics
2. Navigate to Reports → Exploration
3. Select date range
4. Export as CSV

### Import Data to OpenSite Analytics

#### Import Page Views

```python
# import_to_opensite.py
import pandas as pd
from database import SessionLocal
from models import PageView, Site
from datetime import datetime

def import_page_views(csv_file, site_id):
    db = SessionLocal()
    
    # Read CSV
    df = pd.read_csv(csv_file)
    
    # Get site
    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        print(f"Site {site_id} not found")
        return
    
    # Import page views
    for _, row in df.iterrows():
        pageview = PageView(
            site_id=site_id,
            session_id='imported',
            url=row.get('page_path', '/'),
            title=row.get('page_title', ''),
            referrer='',
            user_agent='Imported',
            ip_address='0.0.0.0',
            country='',
            created_at=datetime.strptime(row['date'], '%Y%m%d')
        )
        db.add(pageview)
    
    db.commit()
    db.close()
    print(f"Imported {len(df)} page views")

if __name__ == "__main__":
    import_page_views('ga_pageviews.csv', site_id=1)
```

### Tracking Code Migration

#### Replace GA Code

**Old GA Code:**
```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

**New OpenSite Code:**
```html
<!-- OpenSite Analytics -->
<script>
  (function(w,d,s,id){
    w.OpenSite=w.OpenSite||function(){(w.OpenSite.q=w.OpenSite.q||[]).push(arguments)};
    var f=d.getElementsByTagName(s)[0],
        j=d.createElement(s);
    j.async=true;
    j.src='http://localhost:8000/tracking-script.js';
    j.id=id;
    f.parentNode.insertBefore(j,f);
  })(window,document,"script","opensite-analytics");
  
  OpenSite("init", "YOUR_SITE_KEY", "YOUR_API_KEY");
  OpenSite("trackPageview");
</script>
```

#### Event Mapping

| GA Event | OpenSite Event |
|----------|----------------|
| gtag('event', 'signup') | OpenSite('trackEvent', 'signup') |
| gtag('event', 'purchase') | OpenSite('trackEvent', 'purchase') |
| gtag('event', 'page_view') | OpenSite('trackPageview') |

### Custom Dimension Migration

GA custom dimensions need to be mapped to OpenSite custom dimensions:

```javascript
// GA
gtag('config', 'G-XXXXXXXXXX', {
  'custom_map': {'dimension1': 'user_type'}
});
gtag('event', 'page_view', {'user_type': 'premium'});

// OpenSite
OpenSite('setDimension', 'user_type', 'premium');
OpenSite('trackPageview');
```

## Matomo Migration

### Export Data from Matomo

#### Using Matomo API

```python
# export_matomo.py
import requests
import pandas as pd

def export_matomo_data(site_id, token, start_date, end_date):
    base_url = "https://your-matomo.com"
    
    # Page views
    response = requests.get(f"{base_url}/index.php", params={
        'module': 'API',
        'method': 'Actions.getPageUrls',
        'idSite': site_id,
        'format': 'JSON',
        'period': 'range',
        'date': f'{start_date},{end_date}',
        'token_auth': token
    })
    
    data = response.json()
    df = pd.DataFrame(data)
    df.to_csv('matomo_pageviews.csv', index=False)
    
    return df
```

### Import Data

Use the same import script as GA migration.

### Tracking Code Migration

**Old Matomo Code:**
```html
<!-- Matomo -->
<script>
  var _paq = window._paq = window._paq || [];
  _paq.push(['trackPageView']);
  _paq.push(['enableLinkTracking']);
  (function() {
    var u="//your-matomo.com/";
    _paq.push(['setTrackerUrl', u+'matomo.php']);
    _paq.push(['setSiteId', '1']);
    var d=document, g=d.createElement('script'), s=d.getElementsByTagName('script')[0];
    g.type='text/javascript'; g.async=true; g.src=u+'matomo.js'; s.parentNode.insertBefore(g,s);
  })();
</script>
```

**New OpenSite Code:**
```html
<!-- OpenSite Analytics -->
<script>
  (function(w,d,s,id){
    w.OpenSite=w.OpenSite||function(){(w.OpenSite.q=w.OpenSite.q||[]).push(arguments)};
    var f=d.getElementsByTagName(s)[0],
        j=d.createElement(s);
    j.async=true;
    j.src='http://localhost:8000/tracking-script.js';
    j.id=id;
    f.parentNode.insertBefore(j,f);
  })(window,document,"script","opensite-analytics");
  
  OpenSite("init", "YOUR_SITE_KEY", "YOUR_API_KEY");
  OpenSite("trackPageview");
</script>
```

## Plausible Migration

### Export Data

Plausible doesn't provide direct data export. You may need to:
1. Use the Plausible API (if available)
2. Export reports manually
3. Start fresh with OpenSite

### Tracking Code Migration

**Old Plausible Code:**
```html
<!-- Plausible -->
<script defer data-domain="yourdomain.com" src="https://plausible.io/js/script.js"></script>
```

**New OpenSite Code:**
```html
<!-- OpenSite Analytics -->
<script>
  (function(w,d,s,id){
    w.OpenSite=w.OpenSite||function(){(w.OpenSite.q=w.OpenSite.q||[]).push(arguments)};
    var f=d.getElementsByTagName(s)[0],
        j=d.createElement(s);
    j.async=true;
    j.src='http://localhost:8000/tracking-script.js';
    j.id=id;
    f.parentNode.insertBefore(j,f);
  })(window,document,"script","opensite-analytics");
  
  OpenSite("init", "YOUR_SITE_KEY", "YOUR_API_KEY");
  OpenSite("trackPageview");
</script>
```

## Database Migration

### SQLite to PostgreSQL

#### Export from SQLite

```bash
sqlite3 analytics.db .dump > sqlite_dump.sql
```

#### Import to PostgreSQL

```bash
# Convert dump to PostgreSQL format
# Manual conversion may be needed for specific syntax

# Import
psql -U user -d opensite < sqlite_dump.sql
```

### PostgreSQL to MySQL

#### Export from PostgreSQL

```bash
pg_dump -U user -d opensite > postgres_dump.sql
```

#### Convert and Import to MySQL

Use a conversion tool like `pg2mysql` or manual conversion.

## Validation

### Data Validation

After migration, validate data:

```python
# validate_migration.py
from database import SessionLocal
from models import PageView, Event

def validate_migration():
    db = SessionLocal()
    
    # Check page views
    pageview_count = db.query(PageView).count()
    print(f"Total page views: {pageview_count}")
    
    # Check events
    event_count = db.query(Event).count()
    print(f"Total events: {event_count}")
    
    # Check date range
    first_pv = db.query(PageView).order_by(PageView.created_at).first()
    last_pv = db.query(PageView).order_by(PageView.created_at.desc()).first()
    
    print(f"Date range: {first_pv.created_at} to {last_pv.created_at}")
    
    db.close()

if __name__ == "__main__":
    validate_migration()
```

### Tracking Validation

Test tracking after code replacement:

```javascript
// Test tracking
OpenSite('trackPageview', '/test-page')
OpenSite('trackEvent', 'test_event', { test: true })

// Check in dashboard
```

## Rollback Plan

If migration fails:

1. **Revert tracking code**
   - Restore original tracking script
   - Clear OpenSite tracking code

2. **Restore database**
   - Restore from pre-migration backup
   - Verify data integrity

3. **Notify team**
   - Communicate rollback status
   - Schedule retry

## Post-Migration

### Parallel Running

Run both systems in parallel for validation period:

```html
<!-- Both GA and OpenSite -->
<script>
  // Google Analytics
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>

<script>
  // OpenSite Analytics
  OpenSite("init", "YOUR_SITE_KEY", "YOUR_API_KEY");
  OpenSite("trackPageview");
</script>
```

### Data Comparison

Compare metrics between systems:

```python
# compare_metrics.py
import pandas as pd

def compare_metrics(ga_file, opensite_file):
    ga_df = pd.read_csv(ga_file)
    os_df = pd.read_csv(opensite_file)
    
    # Compare page views
    ga_pv = ga_df['page_views'].sum()
    os_pv = len(os_df)
    
    print(f"GA Page Views: {ga_pv}")
    print(f"OpenSite Page Views: {os_pv}")
    print(f"Difference: {abs(ga_pv - os_pv)} ({abs(ga_pv - os_pv)/ga_pv*100:.2f}%)")
```

### Remove Old Tracking

After validation period:

1. Remove old tracking code
2. Update team documentation
3. Close old accounts
4. Archive old data

## Common Issues

### Data Discrepancies

**Problem:** Different metrics between systems

**Solutions:**
- Check date ranges match
- Verify time zones
- Check filtering rules
- Review bot filtering
- Understand metric definitions

### Tracking Conflicts

**Problem:** Both systems running causes issues

**Solutions:**
- Use different event names
- Check for JavaScript errors
- Monitor performance impact
- Remove one system during testing

### Import Failures

**Problem:** Data import fails

**Solutions:**
- Check CSV format
- Verify data types
- Handle missing values
- Use batch imports
- Check database constraints

## Best Practices

1. **Test in staging** before production migration
2. **Backup everything** before starting
3. **Run in parallel** for validation period
4. **Monitor closely** during migration
5. **Document the process** for future reference
6. **Communicate with team** throughout migration
7. **Validate data** at each step
8. **Have rollback plan** ready
9. **Schedule maintenance window** for final switch
10. **Archive old data** before deletion
