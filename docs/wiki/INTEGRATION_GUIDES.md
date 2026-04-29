# Integration Guides

This document provides integration guides for various platforms and frameworks.

## WordPress Integration

### Method 1: Using a Plugin

1. Create a custom plugin:

```php
<?php
/*
Plugin Name: OpenSite Analytics
Description: Add OpenSite Analytics tracking to WordPress
Version: 1.0
*/

function opensite_analytics_tracking_code() {
    $site_key = get_option('opensite_site_key');
    $api_key = get_option('opensite_api_key');
    $api_url = get_option('opensite_api_url', 'http://localhost:8000');
    
    if ($site_key && $api_key) {
        echo '<script>
  (function(w,d,s,id){
    w.OpenSite=w.OpenSite||function(){(w.OpenSite.q=w.OpenSite.q||[]).push(arguments)};
    var f=d.getElementsByTagName(s)[0],
        j=d.createElement(s);
    j.async=true;
    j.src="' . esc_js($api_url) . '/tracking-script.js";
    j.id=id;
    f.parentNode.insertBefore(j,f);
  })(window,document,"script","opensite-analytics");
  
  OpenSite("init", "' . esc_js($site_key) . '", "' . esc_js($api_key) . '");
  OpenSite("trackPageview");
</script>';
    }
}
add_action('wp_head', 'opensite_analytics_tracking_code');

// Admin settings page
function opensite_analytics_admin_menu() {
    add_options_page(
        'OpenSite Analytics',
        'OpenSite Analytics',
        'manage_options',
        'opensite-analytics',
        'opensite_analytics_settings_page'
    );
}
add_action('admin_menu', 'opensite_analytics_admin_menu');

function opensite_analytics_settings_page() {
    ?>
    <div class="wrap">
        <h1>OpenSite Analytics Settings</h1>
        <form method="post" action="options.php">
            <?php
            settings_fields('opensite_analytics_options');
            do_settings_sections('opensite-analytics');
            ?>
            <table class="form-table">
                <tr>
                    <th scope="row">Site Key</th>
                    <td>
                        <input type="text" 
                               name="opensite_site_key" 
                               value="<?php echo esc_attr(get_option('opensite_site_key')); ?>" 
                               class="regular-text">
                    </td>
                </tr>
                <tr>
                    <th scope="row">API Key</th>
                    <td>
                        <input type="text" 
                               name="opensite_api_key" 
                               value="<?php echo esc_attr(get_option('opensite_api_key')); ?>" 
                               class="regular-text">
                    </td>
                </tr>
                <tr>
                    <th scope="row">API URL</th>
                    <td>
                        <input type="text" 
                               name="opensite_api_url" 
                               value="<?php echo esc_attr(get_option('opensite_api_url', 'http://localhost:8000')); ?>" 
                               class="regular-text">
                    </td>
                </tr>
            </table>
            <?php submit_button(); ?>
        </form>
    </div>
    <?php
}

function opensite_analytics_register_settings() {
    register_setting('opensite_analytics_options', 'opensite_site_key');
    register_setting('opensite_analytics_options', 'opensite_api_key');
    register_setting('opensite_analytics_options', 'opensite_api_url');
}
add_action('admin_init', 'opensite_analytics_register_settings');
```

2. Install the plugin:
   - Save as `opensite-analytics.php`
   - Upload to `wp-content/plugins/`
   - Activate in WordPress admin

3. Configure:
   - Go to Settings → OpenSite Analytics
   - Enter your site key, API key, and API URL

### Method 2: Theme Integration

Add to your theme's `functions.php`:

```php
function opensite_analytics_tracking_code() {
    ?>
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
    <?php
}
add_action('wp_head', 'opensite_analytics_tracking_code');
```

## React Integration

### Basic Setup

1. Install the tracking script in `index.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
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
    </script>
</head>
<body>
    <div id="root"></div>
</body>
</html>
```

2. Create a custom hook:

```typescript
// hooks/useAnalytics.ts
import { useEffect } from 'react'

export function useAnalytics() {
  useEffect(() => {
    // Track initial page view
    if (window.OpenSite) {
      window.OpenSite('trackPageview')
    }
  }, [])

  const trackEvent = (eventName: string, eventData?: object) => {
    if (window.OpenSite) {
      window.OpenSite('trackEvent', eventName, eventData)
    }
  }

  const trackPageView = (url?: string) => {
    if (window.OpenSite) {
      window.OpenSite('trackPageview', url)
    }
  }

  return { trackEvent, trackPageView }
}
```

3. Use in components:

```typescript
import { useAnalytics } from '@/hooks/useAnalytics'

function MyComponent() {
  const { trackEvent, trackPageView } = useAnalytics()

  const handleClick = () => {
    trackEvent('button_click', { button: 'signup' })
  }

  return (
    <button onClick={handleClick}>
      Sign Up
    </button>
  )
}
```

### React Router Integration

```typescript
import { useEffect } from 'react'
import { useLocation } from 'react-router-dom'

function AnalyticsTracker() {
  const location = useLocation()

  useEffect(() => {
    if (window.OpenSite) {
      window.OpenSite('trackPageview', location.pathname)
    }
  }, [location])

  return null
}

// In your App component
function App() {
  return (
    <>
      <AnalyticsTracker />
      <Routes>
        {/* your routes */}
      </Routes>
    </>
  )
}
```

## Next.js Integration

### App Router (Next.js 14)

1. Create analytics component:

```typescript
// components/Analytics.tsx
'use client'

import { useEffect } from 'react'
import { usePathname } from 'next/navigation'

export default function Analytics() {
  const pathname = usePathname()

  useEffect(() => {
    // Load tracking script
    const script = document.createElement('script')
    script.src = `${process.env.NEXT_PUBLIC_API_URL}/tracking-script.js`
    script.async = true
    script.id = 'opensite-analytics'
    document.head.appendChild(script)

    // Initialize
    script.onload = () => {
      if (window.OpenSite) {
        window.OpenSite('init', process.env.NEXT_PUBLIC_SITE_KEY, process.env.NEXT_PUBLIC_API_KEY)
        window.OpenSite('trackPageview')
      }
    }

    return () => {
      document.head.removeChild(script)
    }
  }, [])

  useEffect(() => {
    if (window.OpenSite) {
      window.OpenSite('trackPageview', pathname)
    }
  }, [pathname])

  return null
}
```

2. Add to layout:

```typescript
// app/layout.tsx
import Analytics from '@/components/Analytics'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html>
      <head>
        <Analytics />
      </head>
      <body>{children}</body>
    </html>
  )
}
```

### Custom Events

```typescript
'use client'

import { useAnalytics } from '@/hooks/useAnalytics'

export default function SignupButton() {
  const { trackEvent } = useAnalytics()

  const handleSignup = () => {
    trackEvent('signup', { plan: 'pro' })
    // ... signup logic
  }

  return <button onClick={handleSignup}>Sign Up</button>
}
```

## Vue.js Integration

### Vue 3 with Composition API

```typescript
// composables/useAnalytics.ts
import { onMounted, ref } from 'vue'

export function useAnalytics() {
  const isLoaded = ref(false)

  onMounted(() => {
    const script = document.createElement('script')
    script.src = 'http://localhost:8000/tracking-script.js'
    script.async = true
    script.id = 'opensite-analytics'
    document.head.appendChild(script)

    script.onload = () => {
      if ((window as any).OpenSite) {
        ;(window as any).OpenSite('init', 'YOUR_SITE_KEY', 'YOUR_API_KEY')
        ;(window as any).OpenSite('trackPageview')
        isLoaded.value = true
      }
    }
  })

  const trackEvent = (eventName: string, eventData?: object) => {
    if (isLoaded.value && (window as any).OpenSite) {
      ;(window as any).OpenSite('trackEvent', eventName, eventData)
    }
  }

  const trackPageView = (url?: string) => {
    if (isLoaded.value && (window as any).OpenSite) {
      ;(window as any).OpenSite('trackPageview', url)
    }
  }

  return { trackEvent, trackPageView, isLoaded }
}
```

### Vue Router Integration

```typescript
// router/index.ts
import { createRouter, createWebHistory } from 'vue-router'
import { useAnalytics } from '@/composables/useAnalytics'

const router = createRouter({
  history: createWebHistory(),
  routes: [/* your routes */]
})

router.afterEach((to) => {
  const { trackPageView, isLoaded } = useAnalytics()
  if (isLoaded.value) {
    trackPageView(to.path)
  }
})

export default router
```

## Angular Integration

### Create Analytics Service

```typescript
// services/analytics.service.ts
import { Injectable } from '@angular/core'

declare global {
  interface Window {
    OpenSite?: any
  }

interface OpenSite {
  (command: string, ...args: any[]): void
}

@Injectable({
  providedIn: 'root'
})
export class AnalyticsService {
  private isLoaded = false

  constructor() {
    this.loadScript()
  }

  private loadScript() {
    const script = document.createElement('script')
    script.src = 'http://localhost:8000/tracking-script.js'
    script.async = true
    script.id = 'opensite-analytics'
    document.head.appendChild(script)

    script.onload = () => {
      if (window.OpenSite) {
        window.OpenSite('init', 'YOUR_SITE_KEY', 'YOUR_API_KEY')
        window.OpenSite('trackPageview')
        this.isLoaded = true
      }
    }
  }

  trackEvent(eventName: string, eventData?: object) {
    if (this.isLoaded && window.OpenSite) {
      window.OpenSite('trackEvent', eventName, eventData)
    }
  }

  trackPageView(url?: string) {
    if (this.isLoaded && window.OpenSite) {
      window.OpenSite('trackPageview', url)
    }
  }
}
```

### Router Integration

```typescript
// app/app.module.ts
import { NgModule } from '@angular/core'
import { RouterModule, Router, NavigationEnd } from '@angular/router'
import { AnalyticsService } from './services/analytics.service'

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {
  constructor(private router: Router, private analytics: AnalyticsService) {
    this.router.events.subscribe(event => {
      if (event instanceof NavigationEnd) {
        this.analytics.trackPageView(event.urlAfterRedirects)
      }
    })
  }
}
```

## Static HTML Sites

### Basic Integration

Add this to your HTML:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Your Site</title>
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
</head>
<body>
    <!-- your content -->
</body>
</html>
```

### Custom Events

```html
<button onclick="OpenSite('trackEvent', 'button_click', {button: 'signup'})">
  Sign Up
</button>
```

## API Integration

### Direct API Calls

You can send data directly via the REST API:

```javascript
// Track page view
fetch('http://localhost:8000/api/track/pageview', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    site_id: 1,
    api_key: 'YOUR_API_KEY',
    url: '/page',
    title: 'Page Title',
    referrer: document.referrer,
    user_agent: navigator.userAgent,
    session_id: 'session-123'
  })
})

// Track event
fetch('http://localhost:8000/api/track/event', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    site_id: 1,
    api_key: 'YOUR_API_KEY',
    event_name: 'signup',
    event_data: { plan: 'pro' },
    session_id: 'session-123'
  })
})
```

### Server-Side Tracking

```python
import requests

def track_pageview(site_id, api_key, url, user_agent):
    response = requests.post(
        'http://localhost:8000/api/track/pageview',
        json={
            'site_id': site_id,
            'api_key': api_key,
            'url': url,
            'user_agent': user_agent,
            'session_id': 'server-session'
        }
    )
    return response.json()
```

## Testing Integration

### Verify Tracking

1. Open browser developer tools
2. Go to Network tab
3. Look for requests to your API
4. Check Console for errors
5. Verify data appears in dashboard

### Debug Mode

Add this to test tracking:

```javascript
// After initialization
if (window.OpenSite) {
  window.OpenSite('trackPageview')
  console.log('Tracking initialized')
}
```

## Best Practices

1. **Place script in `<head>`** for accurate tracking
2. **Test in staging** before production
3. **Use environment variables** for keys
4. **Handle errors gracefully**
5. **Respect user privacy** (GDPR/CCPA compliance)
6. **Test custom events** thoroughly
7. **Monitor performance** impact
8. **Keep SDK updated**
9. **Use unique session IDs** for accurate session tracking
10. **Document custom events** for team reference
