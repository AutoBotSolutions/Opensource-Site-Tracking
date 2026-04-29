# Goals Tracking Guide

This guide explains how to set up and track conversion goals in OpenSite Analytics.

## Overview

Goals allow you to track important conversions on your website, such as signups, purchases, or form submissions.

## Goal Types

### Page View Goals

Track when users visit specific pages (e.g., thank you pages, confirmation pages).

### Event Goals

Track when specific events occur (e.g., button clicks, form submissions).

## Creating Goals

### Via Dashboard

1. Go to site analytics page
2. Click "Add Goal"
3. Enter goal details:
   - Name: "Newsletter Signup"
   - Type: "pageview" or "event"
   - Target: "/thank-you" or "signup_completed"
4. Click "Create Goal"

### Via API

```bash
curl -X POST http://localhost:8000/api/goals \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "site_id": 1,
    "name": "Newsletter Signup",
    "goal_type": "pageview",
    "target_value": "/thank-you"
  }'
```

## Tracking Goals

### Page View Goals

Automatically tracked when user visits target page:

```html
<!-- User visits /thank-you -->
<!-- Goal automatically recorded -->
```

### Event Goals

Manually track events:

```javascript
// Track goal completion
OpenSite('trackEvent', 'newsletter_signup', {
  email: 'user@example.com'
})
```

## Goal Analytics

### View Goal Performance

```python
@app.get("/api/goals/{site_id}/analytics")
async def get_goal_analytics(
    site_id: int,
    period: str = "7days",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    goals = db.query(Goal).filter(Goal.site_id == site_id).all()
    
    analytics = []
    for goal in goals:
        # Count goal completions
        if goal.goal_type == "pageview":
            count = db.query(PageView).filter(
                PageView.url == goal.target_value,
                PageView.created_at >= get_date_start(period)
            ).count()
        else:
            count = db.query(Event).filter(
                Event.event_name == goal.target_value,
                Event.created_at >= get_date_start(period)
            ).count()
        
        analytics.append({
            "goal_id": goal.id,
            "goal_name": goal.name,
            "completions": count
        })
    
    return analytics
```

## Goal Examples

### Newsletter Signup

**Type:** Event
**Target:** `newsletter_signup`

```javascript
// On form submission
document.getElementById('newsletter-form').addEventListener('submit', (e) => {
  OpenSite('trackEvent', 'newsletter_signup')
})
```

### Purchase

**Type:** Page View
**Target:** `/purchase-success`

```javascript
// After successful purchase
window.location.href = '/purchase-success'
// Goal automatically tracked
```

### Contact Form

**Type:** Event
**Target:** `contact_form_submit`

```javascript
// On form submission
document.getElementById('contact-form').addEventListener('submit', (e) => {
  OpenSite('trackEvent', 'contact_form_submit', {
    form_id: 'contact-form'
  })
})
```

## Goal Funnels (Future)

Create multi-step funnels:

```python
@app.post("/api/funnels")
async def create_funnel(
    funnel: FunnelCreate,
    current_user: User = Depends(get_current_user)
):
    # Define funnel steps
    steps = [
        {"type": "pageview", "target": "/product"},
        {"type": "pageview", "target": "/cart"},
        {"type": "pageview", "target": "/checkout"},
        {"type": "pageview", "target": "/success"}
    ]
    
    funnel = Funnel(
        name=funnel.name,
        site_id=funnel.site_id,
        steps=steps
    )
    db.add(funnel)
    db.commit()
    
    return funnel
```

## Best Practices

1. Use descriptive goal names
2. Set up goals before launching campaigns
3. Test goal tracking
4. Monitor goal performance
5. Use event goals for dynamic actions
6. Use page view goals for static pages
7. Document goal definitions
8. Regular review of goal relevance
