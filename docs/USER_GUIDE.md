# User Guide

This guide explains how to use OpenSite Analytics to track your website analytics.

## Getting Started

### 1. Login

Visit your OpenSite Analytics dashboard and log in with your credentials.

Default credentials (change after first login):
- Email: `admin@example.com`
- Password: `admin123`

### 2. Create Your First Site

1. Click the "New Site" button on the dashboard
2. Enter your site name (e.g., "My Blog")
3. Enter your domain (e.g., "myblog.com")
4. Click "Create Site"

### 3. Add Tracking Code

After creating a site, you'll see a tracking code snippet. Copy this code and add it to your website:

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
  })(window,document,'script','opensite-analytics');
  
  OpenSite('init', 'YOUR_SITE_KEY', 'YOUR_API_KEY');
  OpenSite('trackPageview');
</script>
```

Replace `YOUR_SITE_KEY` and `YOUR_API_KEY` with the values shown on your site page.

### 4. Start Tracking

Once the tracking code is added to your website, OpenSite Analytics will automatically start collecting data.

## Dashboard Features

### Site Overview

The main dashboard shows all your sites with:
- Site name and domain
- Total page views
- Unique visitors
- Quick access to detailed analytics

Click on any site to view detailed analytics.

### Analytics Dashboard

The analytics dashboard provides comprehensive insights:

#### Page Views Over Time

- Visual chart showing daily page view trends
- Select different time periods (1 day, 7 days, 30 days, 90 days)

#### Device Breakdown

- Desktop vs Mobile vs Tablet traffic
- Pie chart visualization

#### Browser Breakdown

- Visitors by browser (Chrome, Firefox, Safari, etc.)
- Helps optimize for popular browsers

#### Geographic Data

- Visitors by country
- Automatic IP-based location detection

#### Top Pages

- Most visited pages on your site
- View counts for each page
- Identify popular content

#### Top Referrers

- Traffic sources (search engines, social media, direct)
- Understand where your visitors come from

## Tracking Features

### Page View Tracking

Page views are tracked automatically when you add the tracking code.

### Custom Events

Track custom events on your website:

```javascript
OpenSite('trackEvent', 'signup', {
  plan: 'pro',
  source: 'homepage'
});
```

Common event examples:
- Button clicks
- Form submissions
- Downloads
- Video plays

### Goal Tracking

Create conversion goals to track important actions:

1. Go to your site's analytics page
2. Click "Add Goal"
3. Enter goal details:
   - Name (e.g., "Newsletter Signup")
   - Type (pageview or event)
   - Target (e.g., "/thank-you" or "newsletter_signup")
4. Click "Create Goal"

Track goal completions:

```javascript
// For pageview goals
// Automatically tracked when user visits the target page

// For event goals
OpenSite('trackEvent', 'newsletter_signup');
```

## UTM Tracking

OpenSite Analytics automatically tracks UTM parameters in your URLs:

```
https://yourwebsite.com?utm_source=google&utm_medium=cpc&utm_campaign=spring_sale
```

Trackable parameters:
- `utm_source`: Traffic source (google, facebook, etc.)
- `utm_medium`: Marketing medium (cpc, email, social)
- `utm_campaign`: Campaign name
- `utm_term`: Search terms
- `utm_content`: Ad content

View UTM analytics in the "Top Referrers" section.

## Real-Time Updates

OpenSite Analytics supports real-time updates via WebSocket (when enabled):

- Live page view feed
- Live event tracking
- Real-time visitor counts

## Data Management

### Data Retention

Analytics data is automatically cleaned up after the configured retention period (default: 90 days).

### Export Data

Export your analytics data for further analysis (feature coming soon).

### Delete Site

To delete a site and all its data:
1. Go to the site's analytics page
2. Click the delete button (if available)
3. Confirm deletion

**Warning:** This action cannot be undone.

## Tips and Best Practices

### 1. Place Tracking Code Correctly

Add the tracking code to the `<head>` section of your website for the most accurate tracking.

### 2. Use Consistent Event Names

Use clear, consistent event names (e.g., `button_click` instead of `btn_clk`).

### 3. Track Important Conversions

Set up goals for key conversions like:
- Signups
- Purchases
- Form submissions
- Downloads

### 4. Monitor Regularly

Check your analytics regularly to:
- Identify trends
- Spot issues
- Optimize performance

### 5. Use UTM Parameters

Add UTM parameters to your marketing links to track campaign performance.

## Troubleshooting

### No Data Showing

1. Verify the tracking code is installed correctly
2. Check browser console for JavaScript errors
3. Ensure the API URL in the tracking code is correct
4. Verify your site is active

### Incorrect Data

1. Check for duplicate tracking code installations
2. Verify your site domain matches what you registered
3. Check for bot traffic (filter if needed)

### Tracking Code Not Working

1. Ensure JavaScript is enabled in your browser
2. Check for ad-blockers that might block the tracking script
3. Verify the API endpoint is accessible

## Support

For issues or questions:
- Check the [API Documentation](API.md)
- Review the [Installation Guide](INSTALLATION.md)
- Open an issue on GitHub
