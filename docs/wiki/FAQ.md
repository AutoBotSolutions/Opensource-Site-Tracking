# Frequently Asked Questions

General questions and answers about OpenSite Analytics.

## General

### What is OpenSite Analytics?

OpenSite Analytics is a self-hosted, privacy-focused web analytics platform that allows you to track website performance without sharing data with third-party services. It provides real-time analytics, multi-domain support, and custom event tracking.

### Is OpenSite Analytics free?

Yes, OpenSite Analytics is open-source and free to use. You can host it on your own server without any licensing fees.

### What are the system requirements?

- Python 3.13 or higher
- Node.js 18 or higher
- SQLite (included) or PostgreSQL/MySQL (optional)
- 1GB RAM minimum (2GB+ recommended)
- 10GB disk space minimum

### Can I use OpenSite Analytics for commercial purposes?

Yes, OpenSite Analytics is released under the MIT License, which allows commercial use.

## Installation & Setup

### How do I install OpenSite Analytics?

See the [Installation Guide](../INSTALLATION.md) for detailed installation instructions.

### Can I run this on shared hosting?

It's not recommended. OpenSite Analytics requires:
- Python and Node.js support
- Ability to run background processes
- Database access
- WebSocket support

Consider VPS or dedicated hosting instead.

### Can I use Docker for deployment?

Yes, Docker deployment is recommended. See the [Deployment Guide](../DEPLOYMENT.md) for Docker instructions.

### How do I update to the latest version?

1. Backup your database
2. Pull latest changes:
```bash
git pull origin main
```
3. Update dependencies:
```bash
cd backend && pip3 install -r requirements.txt
cd ../frontend && npm install
```
4. Run any database migrations
5. Restart services

## Features

### What data does OpenSite Analytics collect?

OpenSite Analytics collects:
- Page views and URLs
- Referrer information
- User agent (browser, OS, device)
- IP address (for location detection)
- Custom events
- Session data

### Is my data private?

Yes, all data is stored on your own server. You have full control over your data and can delete it at any time.

### Does OpenSite Analytics support real-time analytics?

Yes, real-time analytics are supported via WebSocket connections. You can see live page views and events as they happen.

### Can I track multiple websites?

Yes, you can add multiple sites to your dashboard and track them all from a single account.

### Does OpenSite Analytics support UTM parameters?

Yes, UTM parameters are automatically tracked and can be viewed in the referrer analytics.

### Can I track custom events?

Yes, you can track custom events using the JavaScript SDK:
```javascript
OpenSite('trackEvent', 'button_click', {
  button: 'signup',
  location: 'homepage'
});
```

### What is the data retention policy?

By default, data is retained for 90 days. You can configure this in the backend `.env` file:
```env
DATA_RETENTION_DAYS=90
```

## Tracking

### How do I add the tracking code to my website?

1. Create a site in your dashboard
2. Copy the tracking code provided
3. Paste it into the `<head>` section of your website
4. Replace `YOUR_SITE_KEY` and `YOUR_API_KEY` with your actual keys

### Where should I place the tracking code?

Place the tracking code in the `<head>` section of your HTML for the most accurate tracking.

### Does the tracking code affect page load time?

The tracking code is asynchronous and has minimal impact on page load time (< 50ms).

### Can I track single-page applications (SPAs)?

Yes, the tracking SDK supports SPAs. You can manually track page views:
```javascript
OpenSite('trackPageview', '/new-page');
```

### Does OpenSite Analytics respect Do Not Track (DNT)?

Currently, DNT is not enforced. You can implement DNT checking in your tracking code if needed.

### Can I exclude my own visits?

Yes, you can filter by IP address or create a browser extension to disable tracking for your own visits.

### How accurate is the geographic data?

Geographic data is based on IP address lookup and is generally accurate at the country level. City-level accuracy varies.

## Security

### Is OpenSite Analytics secure?

OpenSite Analytics includes:
- JWT-based authentication
- Password hashing with bcrypt
- Rate limiting
- CORS protection
- SQL injection prevention

However, you must:
- Use strong passwords
- Keep dependencies updated
- Use HTTPS in production
- Configure firewall rules

### Should I change the default admin password?

Yes, change the default password immediately after installation. The default credentials are:
- Email: `admin@example.com`
- Password: `admin123`

### How do I secure my installation?

1. Change default credentials
2. Generate strong SECRET_KEY
3. Use HTTPS
4. Configure firewall
5. Keep dependencies updated
6. Regular backups

See the [Security Guide](SECURITY.md) for more details.

### Can I use OpenSite Analytics behind a corporate firewall?

Yes, but you may need to:
- Whitelist the tracking script URL
- Configure CORS origins
- Adjust firewall rules
- Use WebSocket if needed

## Performance

### How many page views can OpenSite Analytics handle?

Performance depends on your server:
- SQLite: ~10,000 page views/day
- PostgreSQL: ~100,000+ page views/day
- With optimization: 1M+ page views/day

### How do I improve performance?

1. Use PostgreSQL instead of SQLite
2. Add database indexes
3. Implement caching
4. Use connection pooling
5. Optimize queries
6. Use read replicas for analytics

See the [Architecture Guide](ARCHITECTURE.md) for performance tips.

### Does OpenSite Analytics use caching?

Currently, caching is not implemented. You can add Redis caching for improved performance.

### How much disk space does OpenSite Analytics use?

Approximate usage:
- 1,000 page views: ~1MB
- 100,000 page views: ~100MB
- 1,000,000 page views: ~1GB

This varies based on data retention and event complexity.

## Integration

### Can I integrate OpenSite Analytics with other tools?

Yes, you can:
- Use the REST API
- Export data (feature coming soon)
- Set up webhooks (feature coming soon)
- Use custom integrations

### Does OpenSite Analytics have an API?

Yes, see the [API Documentation](../API.md) for complete API reference.

### Can I use OpenSite Analytics with WordPress?

Yes, you can add the tracking code to WordPress via:
- Custom plugin
- Theme functions.php
- Page builder integration

### Can I use OpenSite Analytics with React/Vue/Angular?

Yes, the tracking SDK works with all JavaScript frameworks. For SPAs, use manual page view tracking.

### Does OpenSite Analytics support mobile apps?

Currently, web tracking only. Mobile app support can be added using the REST API.

## Troubleshooting

### Why is my tracking not working?

Common issues:
1. Tracking code not installed correctly
2. Wrong site_key or api_key
3. Site not active
4. Backend not running
5. CORS issues

Check the [Troubleshooting Guide](TROUBLESHOOTING.md) for detailed solutions.

### Why are my analytics showing 0?

1. Verify tracking code is installed
2. Check browser console for errors
3. Test tracking endpoint directly
4. Ensure site is active
5. Check data retention settings

### How do I reset my password?

Currently, password reset is not implemented. You can:
1. Reinitialize database (loses all data)
2. Manually update password in database
3. Use the API to update password (if authenticated)

### Why is the dashboard loading slowly?

Possible causes:
1. Large dataset
2. Slow database queries
3. Network latency
4. Server resources

See the [Troubleshooting Guide](TROUBLESHOOTING.md) for solutions.

## Comparison

### How does OpenSite Analytics compare to Google Analytics?

**OpenSite Analytics:**
- Self-hosted, data stays on your server
- No data sharing with third parties
- Privacy-focused
- Customizable
- No vendor lock-in

**Google Analytics:**
- Cloud-hosted
- Data shared with Google
- More features
- Free tier available
- Easier setup

### How does OpenSite Analytics compare to Matomo?

Both are self-hosted analytics platforms:
- OpenSite Analytics: Modern stack (FastAPI + Next.js), simpler setup
- Matomo: PHP-based, more mature, more features

### Can I migrate from Google Analytics?

You can:
1. Install OpenSite Analytics
2. Add tracking code alongside GA
3. Compare data
4. Remove GA when satisfied

Data import from GA is not currently supported.

## Support

### Where can I get help?

- Documentation: Check the docs folder
- GitHub Issues: Report bugs and request features
- Discussions: Ask questions and share ideas

### Is commercial support available?

Currently, commercial support is not available. Community support is available through GitHub.

### How do I report a bug?

Create a GitHub issue with:
- Description of the bug
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details
- Logs/screenshots

### How do I request a feature?

Create a GitHub issue with:
- Feature description
- Use case
- Proposed implementation (optional)
- Priority

## Licensing

### What license is OpenSite Analytics released under?

MIT License. See [LICENSE.md](../LICENSE.md) for details.

### Can I modify the code?

Yes, the MIT License allows modification. You can:
- Fork the repository
- Make changes
- Distribute your version
- Use it commercially

### Can I remove the attribution?

Yes, the MIT License does not require attribution. However, attribution is appreciated.

## Future Plans

### What features are planned?

- User roles and permissions
- Team collaboration
- Email reports
- Data export
- Webhooks
- Mobile app tracking
- A/B testing
- Funnel analysis
- Heatmaps
- Session recordings

### When will feature X be released?

Check the GitHub issues and milestones for feature roadmaps. Community contributions are welcome!

### How can I contribute?

See the [Contributing Guide](../CONTRIBUTING.md) for details on how to contribute to OpenSite Analytics.
