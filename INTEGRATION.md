# Integration Guide

This guide shows you how to integrate OpenSite Analytics into your websites and applications.

## Quick Start

1. Add your website in the dashboard at http://localhost:3000
2. Copy the integration code provided
3. Paste it into your website's HTML (before the closing `</body>` tag)

## Frontend Integration

### HTML/JavaScript

Add this snippet to your website's HTML:

```html
<script>
  (function(w,d,s,id){
    w.OpenSite=w.OpenSite||function(){(w.OpenSite.q=w.OpenSite.q||[]).push(arguments)};
    var f=d.getElementsByTagName(s)[0],
        j=d.createElement(s);
    j.async=true;
    j.src='http://your-server.com:8000/tracking-script.js';
    j.id=id;
    f.parentNode.insertBefore(j,f);
  })(window,document,'script','opensite-analytics');
  
  OpenSite('init', 'YOUR_SITE_KEY', 'YOUR_API_KEY');
  OpenSite('trackPageview');
</script>
```

### React

```jsx
import { useEffect } from 'react';

function Analytics({ siteKey, apiKey }) {
  useEffect(() => {
    const script = document.createElement('script');
    script.async = true;
    script.src = 'http://your-server.com:8000/tracking-script.js';
    script.id = 'opensite-analytics';
    document.head.appendChild(script);

    script.onload = () => {
      window.OpenSite('init', siteKey, apiKey);
      window.OpenSite('trackPageview');
    };

    return () => {
      document.head.removeChild(script);
    };
  }, [siteKey, apiKey]);

  return null;
}

export default Analytics;
```

### Vue.js

```vue
<template>
  <div></div>
</template>

<script>
export default {
  name: 'Analytics',
  props: {
    siteKey: String,
    apiKey: String
  },
  mounted() {
    const script = document.createElement('script');
    script.async = true;
    script.src = 'http://your-server.com:8000/tracking-script.js';
    script.id = 'opensite-analytics';
    document.head.appendChild(script);

    script.onload = () => {
      window.OpenSite('init', this.siteKey, this.apiKey);
      window.OpenSite('trackPageview');
    };
  }
}
</script>
```

## Backend Integration

### Python (Flask/Django)

```python
import requests

site_key = 'YOUR_SITE_KEY'
api_key = 'YOUR_API_KEY'
endpoint = 'http://your-server.com:8000/api/track'

# Track page view
def track_pageview(url, title, referrer=None):
    requests.post(f'{endpoint}/pageview', json={
        'site_id': site_key,
        'api_key': api_key,
        'url': url,
        'title': title,
        'referrer': referrer
    })

# Track custom event
def track_event(event_name, event_data=None, url=None):
    requests.post(f'{endpoint}/event', json={
        'site_id': site_key,
        'api_key': api_key,
        'event_name': event_name,
        'event_data': event_data,
        'url': url
    })
```

### Node.js (Express)

```javascript
const axios = require('axios');

const siteKey = 'YOUR_SITE_KEY';
const apiKey = 'YOUR_API_KEY';
const endpoint = 'http://your-server.com:8000/api/track';

// Track page view
async function trackPageview(url, title, referrer) {
  await axios.post(`${endpoint}/pageview`, {
    site_id: siteKey,
    api_key: apiKey,
    url,
    title,
    referrer
  });
}

// Track custom event
async function trackEvent(eventName, eventData, url) {
  await axios.post(`${endpoint}/event`, {
    site_id: siteKey,
    api_key: apiKey,
    event_name: eventName,
    event_data: eventData,
    url
  });
}
```

### PHP

```php
<?php
$siteKey = 'YOUR_SITE_KEY';
$apiKey = 'YOUR_API_KEY';
$endpoint = 'http://your-server.com:8000/api/track';

function trackPageview($url, $title, $referrer = null) {
    global $siteKey, $apiKey, $endpoint;
    
    $data = [
        'site_id' => $siteKey,
        'api_key' => $apiKey,
        'url' => $url,
        'title' => $title,
        'referrer' => $referrer
    ];
    
    $ch = curl_init($endpoint . '/pageview');
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
    curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_exec($ch);
    curl_close($ch);
}

function trackEvent($eventName, $eventData = null, $url = null) {
    global $siteKey, $apiKey, $endpoint;
    
    $data = [
        'site_id' => $siteKey,
        'api_key' => $apiKey,
        'event_name' => $eventName,
        'event_data' => $eventData,
        'url' => $url
    ];
    
    $ch = curl_init($endpoint . '/event');
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
    curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_exec($ch);
    curl_close($ch);
}
?>
```

## Custom Event Tracking

Track custom events to monitor specific user actions:

### JavaScript

```javascript
// Track button click
OpenSite('trackEvent', 'button_click', {
  button_id: 'signup-button',
  page: '/pricing'
});

// Track form submission
OpenSite('trackEvent', 'form_submit', {
  form_name: 'contact-form',
  success: true
});

// Track download
OpenSite('trackEvent', 'file_download', {
  file_name: 'ebook.pdf',
  file_size: '2.5MB'
});
```

### Python

```python
# Track custom event
track_event('purchase_completed', {
    'product_id': '12345',
    'amount': 99.99,
    'currency': 'USD'
})
```

## Single Page Applications (SPAs)

For SPAs, you'll want to track page views when the route changes:

### React Router

```jsx
import { useEffect } from 'react';
import { useLocation } from 'react-router-dom';

function RouteTracker() {
  const location = useLocation();

  useEffect(() => {
    if (window.OpenSite) {
      window.OpenSite('trackPageview');
    }
  }, [location]);

  return null;
}
```

### Next.js

```jsx
import { useEffect } from 'react';
import { useRouter } from 'next/router';

function RouteTracker() {
  const router = useRouter();

  useEffect(() => {
    const handleRouteChange = () => {
      if (window.OpenSite) {
        window.OpenSite('trackPageview');
      }
    };

    router.events.on('routeChangeComplete', handleRouteChange);

    return () => {
      router.events.off('routeChangeComplete', handleRouteChange);
    };
  }, [router]);

  return null;
}
```

## Server-Side Tracking

For server-side rendered applications or API tracking:

### Python (FastAPI)

```python
from fastapi import Request
import httpx

@app.middleware("http")
async def analytics_middleware(request: Request, call_next):
    response = await call_next(request)
    
    # Track page view
    async with httpx.AsyncClient() as client:
        await client.post('http://your-server.com:8000/api/track/pageview', json={
            'site_id': 'YOUR_SITE_KEY',
            'api_key': 'YOUR_API_KEY',
            'url': str(request.url),
            'title': 'Server Rendered Page',
            'user_agent': request.headers.get('user-agent')
        })
    
    return response
```

## Privacy and GDPR

To comply with GDPR, you can:

1. Add consent management before initializing tracking
2. Allow users to opt-out
3. Anonymize IP addresses (already done by default)

```javascript
// Only track if user consented
if (userConsent) {
  OpenSite('init', 'YOUR_SITE_KEY', 'YOUR_API_KEY');
  OpenSite('trackPageview');
}
```

## Testing Your Integration

1. Add the tracking code to your website
2. Visit your website in a browser
3. Check the dashboard at http://localhost:3000
4. You should see page views appearing in real-time

## Troubleshooting

### No data appearing in dashboard

- Check that your site_key and api_key are correct
- Verify the tracking script URL is accessible
- Check browser console for errors
- Ensure CORS is configured correctly in backend

### CORS errors

Update `backend/.env` to include your domain:

```
CORS_ORIGINS=http://localhost:3000,http://your-domain.com
```

### Session tracking not working

- Ensure cookies/localStorage are enabled
- Check that the tracking script is loading
- Verify session_id is being generated
