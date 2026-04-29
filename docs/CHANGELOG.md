# Changelog

All notable changes to OpenSite Analytics will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial release of OpenSite Analytics
- User authentication with JWT
- Multi-domain site tracking
- Real-time analytics dashboard
- Custom event tracking
- Goal/conversion tracking
- Geographic IP detection
- UTM parameter tracking
- Data retention cleanup
- Rate limiting
- WebSocket real-time updates
- Responsive Next.js frontend

### Fixed
- JWT token sub claim string conversion
- Analytics endpoint pageviews_over_time field
- Authentication token initialization in frontend
- Site creation authentication and ownership

## [1.0.0] - 2026-04-29

### Added
- Initial release
- Core analytics tracking (page views, sessions, events)
- User authentication system
- Multi-site management
- Real-time dashboard
- Tracking JavaScript SDK
- Geographic data
- Device and browser breakdown
- Referrer tracking
- Goal tracking
- Data retention automation

### Security
- JWT-based authentication
- Rate limiting
- CORS protection
- SQL injection prevention
- XSS protection

### Performance
- Database indexes
- Connection pooling
- Efficient queries
- Frontend code splitting

### Documentation
- Installation guide
- API documentation
- User guide
- Development guide
- Deployment guide
- Contributing guidelines
