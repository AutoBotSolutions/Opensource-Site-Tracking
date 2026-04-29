# Custom Events Guide

This guide explains how to implement and track custom events in OpenSite Analytics.

## Overview

Custom events allow you to track specific user actions beyond page views, such as button clicks, form submissions, and video plays.

## Event Tracking

### Basic Event

```javascript
OpenSite('trackEvent', 'button_click')
```

### Event with Data

```javascript
OpenSite('trackEvent', 'signup', {
  plan: 'pro',
  source: 'homepage'
})
```

### Event with Category

```javascript
OpenSite('trackEvent', 'video_play', {
  category: 'engagement',
  video_id: 'abc123',
  duration: 120
})
```

## Common Event Types

### Form Events

```javascript
// Form submission
document.getElementById('contact-form').addEventListener('submit', (e) => {
  OpenSite('trackEvent', 'form_submit', {
    form_id: 'contact-form',
    form_name: 'Contact Us'
  })
})

// Form field interaction
document.querySelectorAll('input').forEach(input => {
  input.addEventListener('focus', () => {
    OpenSite('trackEvent', 'form_field_focus', {
      field_name: input.name
    })
  })
})
```

### E-commerce Events

```javascript
// Product view
function trackProductView(productId, productName, price) {
  OpenSite('trackEvent', 'product_view', {
    product_id: productId,
    product_name: productName,
    product_price: price
  })
}

// Add to cart
function trackAddToCart(productId, quantity) {
  OpenSite('trackEvent', 'add_to_cart', {
    product_id: productId,
    quantity: quantity
  })
}

// Purchase
function trackPurchase(orderId, total, items) {
  OpenSite('trackEvent', 'purchase', {
    order_id: orderId,
    total: total,
    items: items
  })
}
```

### Content Events

```javascript
// Video play
document.getElementById('video-player').addEventListener('play', () => {
  OpenSite('trackEvent', 'video_play', {
    video_id: 'abc123',
    video_title: 'Product Demo'
  })
})

// Video pause
document.getElementById('video-player').addEventListener('pause', () => {
  OpenSite('trackEvent', 'video_pause', {
    video_id: 'abc123',
    watch_duration: 120
  })
})

// Video complete
document.getElementById('video-player').addEventListener('ended', () => {
  OpenSite('trackEvent', 'video_complete', {
    video_id: 'abc123'
  })
})
```

### Navigation Events

```javascript
// Menu click
document.querySelectorAll('.nav-link').forEach(link => {
  link.addEventListener('click', () => {
    OpenSite('trackEvent', 'menu_click', {
      menu_item: link.textContent,
      menu_section: 'main'
    })
  })
})

// Breadcrumb click
document.querySelectorAll('.breadcrumb a').forEach(link => {
  link.addEventListener('click', () => {
    OpenSite('trackEvent', 'breadcrumb_click', {
      breadcrumb_level: link.dataset.level
    })
  })
})
```

## Event Schema

### Required Fields

- `event_name`: String identifier for the event

### Optional Fields

- `event_data`: JSON object with custom properties
- `timestamp`: Override default timestamp
- `category`: Event category for grouping

### Event Data Best Practices

- Use snake_case for keys
- Keep data structure consistent
- Include relevant context
- Avoid sensitive data
- Use appropriate data types

## Event Naming Conventions

### Format

Use lowercase with underscores:
- `button_click` (not `ButtonClick` or `btn-clk`)
- `form_submit` (not `FormSubmit` or `form-submit`)

### Categories

Prefix with category when useful:
- `video_play`, `video_pause`, `video_complete`
- `form_submit`, `form_field_focus`
- `product_view`, `product_add`, `product_remove`

### Descriptive Names

Be specific and descriptive:
- `newsletter_signup` (not `signup`)
- `contact_form_submit` (not `form_submit` if multiple forms)

## Event Validation

### Backend Validation

```python
# In schemas.py
class EventCreate(BaseModel):
    event_name: str = Field(..., min_length=1, max_length=255)
    event_data: Optional[Dict[str, Any]] = None
    
    @validator('event_name')
    def validate_event_name(cls, v):
        if not re.match(r'^[a-z0-9_]+$', v):
            raise ValueError('Event name must be lowercase alphanumeric with underscores')
        return v
```

### Frontend Validation

```javascript
function trackEvent(eventName, eventData) {
  // Validate event name
  if (!/^[a-z0-9_]+$/.test(eventName)) {
    console.error('Invalid event name format')
    return
  }
  
  // Validate event data
  if (eventData && typeof eventData !== 'object') {
    console.error('Event data must be an object')
    return
  }
  
  OpenSite('trackEvent', eventName, eventData)
}
```

## Event Analytics

### Query Events

```python
@app.get("/api/events/{site_id}")
async def get_events(
    site_id: int,
    event_name: Optional[str] = None,
    period: str = "7days",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Event).filter(
        Event.site_id == site_id,
        Event.created_at >= get_date_start(period)
    )
    
    if event_name:
        query = query.filter(Event.event_name == event_name)
    
    events = query.all()
    return events
```

### Event Aggregation

```python
@app.get("/api/events/{site_id}/summary")
async def get_event_summary(
    site_id: int,
    period: str = "7days",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    events = db.query(Event).filter(
        Event.site_id == site_id,
        Event.created_at >= get_date_start(period)
    ).all()
    
    summary = {}
    for event in events:
        if event.event_name not in summary:
            summary[event.event_name] = 0
        summary[event.event_name] += 1
    
    return summary
```

## Best Practices

1. Use consistent naming conventions
2. Document custom events
3. Test event tracking
4. Avoid excessive events
5. Group related events
6. Use meaningful data
7. Review event performance
8. Set up goals for key events
