# UTM Tracking Guide

This guide explains UTM parameter tracking in OpenSite Analytics.

## Overview

UTM (Urchin Tracking Module) parameters allow you to track marketing campaigns and traffic sources.

## UTM Parameters

### Standard Parameters

- `utm_source`: Traffic source (google, facebook, newsletter)
- `utm_medium`: Marketing medium (cpc, email, social)
- `utm_campaign`: Campaign name (spring_sale, product_launch)
- `utm_term`: Search terms (analytics software)
- `utm_content`: Ad content (banner_a, text_link)

### URL Format

```
https://yourwebsite.com?utm_source=google&utm_medium=cpc&utm_campaign=spring_sale
```

## Implementation

### Automatic Tracking

UTM parameters are automatically tracked when present in URL:

```python
# In tracking endpoint
@app.post("/api/track/pageview")
async def track_pageview(pageview: PageViewCreate, request: Request):
    # Extract UTM parameters from referrer or URL
    utm_params = extract_utm_params(request)
    
    # Store with page view
    new_pageview = PageView(
        # ... other fields
        utm_source=utm_params.get('utm_source'),
        utm_medium=utm_params.get('utm_medium'),
        utm_campaign=utm_params.get('utm_campaign'),
        utm_term=utm_params.get('utm_term'),
        utm_content=utm_params.get('utm_content')
    )
```

### Extract UTM Parameters

```python
def extract_utm_params(request: Request) -> dict:
    """Extract UTM parameters from request"""
    params = {}
    
    # Check query parameters
    for param in ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content']:
        value = request.query_params.get(param)
        if value:
            params[param] = value
    
    return params
```

## Campaign Tracking

### Email Campaigns

```html
<!-- Email link -->
<a href="https://yourwebsite.com?utm_source=newsletter&utm_medium=email&utm_campaign=monthly_newsletter">
  Read More
</a>
```

### Social Media

```html
<!-- Twitter link -->
<a href="https://yourwebsite.com?utm_source=twitter&utm_medium=social&utm_campaign=product_launch">
  Learn More
</a>

<!-- Facebook link -->
<a href="https://yourwebsite.com?utm_source=facebook&utm_medium=social&utm_campaign=summer_sale">
  Shop Now
</a>
```

### Paid Advertising

```html
<!-- Google Ads -->
<a href="https://yourwebsite.com?utm_source=google&utm_medium=cpc&utm_campaign=summer_sale&utm_term=analytics">
  Analytics Software
</a>

<!-- Facebook Ads -->
<a href="https://yourwebsite.com?utm_source=facebook&utm_medium=cpc&utm_campaign=retargeting&utm_content=video_ad">
  Watch Demo
</a>
```

## UTM Analytics

### Campaign Performance

```python
@app.get("/api/analytics/{site_id}/campaigns")
async def get_campaign_analytics(
    site_id: int,
    period: str = "30days",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    pageviews = db.query(PageView).filter(
        PageView.site_id == site_id,
        PageView.created_at >= get_date_start(period),
        PageView.utm_campaign.isnot(None)
    ).all()
    
    campaigns = {}
    for pv in pageviews:
        campaign = pv.utm_campaign
        if campaign not in campaigns:
            campaigns[campaign] = {
                'pageviews': 0,
                'visitors': set()
            }
        campaigns[campaign]['pageviews'] += 1
        campaigns[campaign]['visitors'].add(pv.session_id)
    
    # Convert sets to counts
    for campaign in campaigns:
        campaigns[campaign]['visitors'] = len(campaigns[campaign]['visitors'])
    
    return campaigns
```

### Source/Medium Breakdown

```python
@app.get("/api/analytics/{site_id}/sources")
async def get_source_analytics(
    site_id: int,
    period: str = "30days",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    pageviews = db.query(PageView).filter(
        PageView.site_id == site_id,
        PageView.created_at >= get_date_start(period)
    ).all()
    
    sources = {}
    for pv in pageviews:
        source = pv.utm_source or 'direct'
        medium = pv.utm_medium or 'none'
        key = f"{source}/{medium}"
        
        if key not in sources:
            sources[key] = 0
        sources[key] += 1
    
    return sources
```

## Best Practices

1. Use consistent UTM parameter naming
2. Document campaign naming conventions
3. Use lowercase for parameter values
4. Avoid special characters in values
5. Track all marketing campaigns
6. Use utm_content for A/B testing
7. Regularly review campaign performance
8. Keep campaign names descriptive
