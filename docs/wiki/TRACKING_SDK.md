# Tracking SDK Guide

This guide explains how to use the OpenSite Analytics JavaScript tracking SDK.

## Overview

The OpenSite Analytics tracking SDK is a lightweight JavaScript library that allows you to track page views, events, and custom data on your website.

## Installation

### Method 1: Direct Script Tag

Add this to your HTML `<head>` section:

```html
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
</script>
```

### Method 2: NPM Package (Future)

```bash
npm install opensite-analytics
```

```javascript
import OpenSite from 'opensite-analytics'
OpenSite.init('YOUR_SITE_KEY', 'YOUR_API_KEY')
```

## Initialization

### Basic Initialization

```javascript
OpenSite('init', 'YOUR_SITE_KEY', 'YOUR_API_KEY')
```

### Configuration Options

```javascript
OpenSite('init', 'YOUR_SITE_KEY', 'YOUR_API_KEY', {
  apiURL: 'https://analytics.yourdomain.com',
  autoTrack: true,
  debug: false,
  sessionTimeout: 30 * 60 * 1000 // 30 minutes
})
```

**Options:**
- `apiURL`: Custom API URL (default: from script src)
- `autoTrack`: Automatically track page views (default: true)
- `debug`: Enable debug logging (default: false)
- `sessionTimeout`: Session timeout in milliseconds (default: 30 minutes)

## Page View Tracking

### Automatic Tracking

By default, the SDK automatically tracks page views when the page loads.

### Manual Page View Tracking

```javascript
// Track current page
OpenSite('trackPageview')

// Track specific URL
OpenSite('trackPageview', '/custom-url')

// Track with custom title
OpenSite('trackPageview', '/about', {
  title: 'About Us Page'
})

// Track with referrer
OpenSite('trackPageview', '/product', {
  title: 'Product Page',
  referrer: 'https://google.com'
})
```

### Single Page Applications

For SPAs, manually track route changes:

```javascript
// React Router example
import { useEffect } from 'react'
import { useLocation } from 'react-router-dom'

function RouteTracker() {
  const location = useLocation()

  useEffect(() => {
    OpenSite('trackPageview', location.pathname, {
      title: document.title
    })
  }, [location])

  return null
}
```

```javascript
// Next.js example
import { useEffect } from 'react'
import { useRouter } from 'next/navigation'

export default function RouteTracker() {
  const router = useRouter()

  useEffect(() => {
    const handleRouteChange = (url: string) => {
      OpenSite('trackPageview', url)
    }

    router.events.on('routeChangeComplete', handleRouteChange)
    return () => {
      router.events.off('routeChangeComplete', handleRouteChange)
    }
  }, [router])

  return null
}
```

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
  video_id: '123',
  duration: 120
})
```

### Common Event Examples

```javascript
// Form submission
OpenSite('trackEvent', 'form_submit', {
  form_id: 'contact-form',
  form_name: 'Contact Us'
})

// File download
OpenSite('trackEvent', 'file_download', {
  file_name: 'guide.pdf',
  file_type: 'pdf'
})

// Video play
OpenSite('trackEvent', 'video_play', {
  video_id: 'abc123',
  video_title: 'Product Demo'
})

// Outbound link click
OpenSite('trackEvent', 'outbound_click', {
  url: 'https://external-site.com',
  link_text: 'Visit Partner'
})

// Search
OpenSite('trackEvent', 'search', {
  search_term: 'analytics',
  result_count: 42
})

// Error
OpenSite('trackEvent', 'error', {
  error_message: 'Failed to load data',
  error_code: 500
})
```

## Session Management

### Session ID

The SDK automatically generates and manages session IDs. You can access the current session ID:

```javascript
const sessionId = OpenSite('getSessionId')
console.log('Session ID:', sessionId)
```

### Custom Session ID

```javascript
OpenSite('init', 'SITE_KEY', 'API_KEY', {
  sessionId: 'custom-session-123'
})
```

### Session Timeout

```javascript
// Set custom session timeout (30 minutes)
OpenSite('init', 'SITE_KEY', 'API_KEY', {
  sessionTimeout: 30 * 60 * 1000
})
```

## User Identification

### Set User ID

```javascript
OpenSite('setUserId', 'user_123')
```

### Set User Properties

```javascript
OpenSite('setUserProperties', {
  plan: 'pro',
  signup_date: '2026-01-01',
  company: 'Acme Corp'
})
```

### Reset User

```javascript
OpenSite('resetUser')
```

## Custom Dimensions

### Set Custom Dimension

```javascript
OpenSite('setDimension', 'dimension1', 'value')
```

### Set Multiple Dimensions

```javascript
OpenSite('setDimensions', {
  dimension1: 'value1',
  dimension2: 'value2',
  dimension3: 'value3'
})
```

## E-commerce Tracking

### Product View

```javascript
OpenSite('trackEvent', 'product_view', {
  product_id: '123',
  product_name: 'Analytics Pro',
  product_category: 'Software',
  product_price: 99.99,
  currency: 'USD'
})
```

### Add to Cart

```javascript
OpenSite('trackEvent', 'add_to_cart', {
  product_id: '123',
  product_name: 'Analytics Pro',
  quantity: 2,
  price: 99.99,
  currency: 'USD'
})
```

### Purchase

```javascript
OpenSite('trackEvent', 'purchase', {
  order_id: 'ORD-123',
  total: 199.98,
  currency: 'USD',
  items: [
    {
      product_id: '123',
      product_name: 'Analytics Pro',
      quantity: 2,
      price: 99.99
    }
  ]
})
```

## A/B Testing

### Track Experiment

```javascript
OpenSite('setExperiment', 'experiment_1', 'variant_a')
```

### Track Conversion

```javascript
OpenSite('trackEvent', 'conversion', {
  experiment_id: 'experiment_1',
  variant: 'variant_a',
  goal: 'signup'
})
```

## Debugging

### Enable Debug Mode

```javascript
OpenSite('init', 'SITE_KEY', 'API_KEY', {
  debug: true
})
```

Debug mode logs all tracking calls to the console.

### Verify Tracking

```javascript
// Check if SDK is loaded
if (window.OpenSite) {
  console.log('SDK loaded')
}

// Check initialization status
OpenSite('isInitialized', function(status) {
  console.log('Initialized:', status)
})
```

## Advanced Usage

### Queue Management

The SDK queues events when offline and sends them when connection is restored:

```javascript
// Configure queue size
OpenSite('init', 'SITE_KEY', 'API_KEY', {
  queueSize: 100,
  flushInterval: 5000 // 5 seconds
})
```

### Batch Sending

Send multiple events in a single request:

```javascript
OpenSite('flush')
```

### Custom HTTP Headers

```javascript
OpenSite('init', 'SITE_KEY', 'API_KEY', {
  headers: {
    'X-Custom-Header': 'value'
  }
})
```

## Privacy & Compliance

### Do Not Track

```javascript
// Respect DNT
if (navigator.doNotTrack === '1') {
  OpenSite('disable')
}
```

### GDPR Consent

```javascript
// Disable tracking until consent
OpenSite('init', 'SITE_KEY', 'API_KEY', {
  autoTrack: false
})

// Enable after consent
function onConsentGiven() {
  OpenSite('enable')
  OpenSite('trackPageview')
}
```

### Data Anonymization

```javascript
OpenSite('init', 'SITE_KEY', 'API_KEY', {
  anonymizeIp: true
})
```

## Performance

### Async Loading

The SDK loads asynchronously to prevent blocking page load:

```html
<script>
  (function(w,d,s,id){
    // ... async loading
  })(window,document,"script","opensite-analytics");
</script>
```

### Lazy Loading

Load SDK only when needed:

```javascript
function loadTracking() {
  const script = document.createElement('script')
  script.src = 'http://localhost:8000/tracking-script.js'
  script.async = true
  script.onload = () => {
    OpenSite('init', 'SITE_KEY', 'API_KEY')
  }
  document.head.appendChild(script)
}

// Load on user interaction
document.addEventListener('click', loadTracking, { once: true })
```

## Browser Compatibility

The SDK supports:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+
- Opera 76+

For older browsers, use polyfills for:
- Promise
- fetch
- Array.prototype.includes

## Troubleshooting

### SDK Not Loading

**Problem:** SDK script fails to load

**Solutions:**
1. Check script URL is correct
2. Verify backend is running
3. Check browser console for errors
4. Verify CORS settings

### Events Not Tracking

**Problem:** Events not appearing in dashboard

**Solutions:**
1. Verify site key and API key are correct
2. Check browser console for errors
3. Verify site is active
4. Check network tab for failed requests
5. Enable debug mode

### Session Issues

**Problem:** Sessions not tracking correctly

**Solutions:**
1. Check session timeout settings
2. Verify cookies are enabled
3. Check for ad-blockers
4. Verify localStorage is available

## Best Practices

1. **Place script in `<head>`** for accurate tracking
2. **Use descriptive event names** (e.g., `button_click` not `clk`)
3. **Consistent event naming** across your application
4. **Test in development** before production
5. **Respect user privacy** (GDPR/CCPA compliance)
6. **Monitor performance** impact
7. **Use custom dimensions** for additional context
8. **Document custom events** for team reference
9. **Handle errors gracefully**
10. **Keep SDK updated**
