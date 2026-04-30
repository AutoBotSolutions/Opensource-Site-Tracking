# OpenSite Analytics - Self-Hosted Site Tracking System

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/AutoBotSolutions/Opensource-Site-Tracking/blob/main/LICENSE.md)
[![Python](https://img.shields.io/badge/Python-3.9%2B-green.svg)](https://www.python.org/downloads/)
[![Node.js](https://img.shields.io/badge/Node.js-18%2B-brightgreen.svg)](https://nodejs.org/)
[![Docker](https://img.shields.io/badge/Docker-Supported-blue.svg)](https://www.docker.com/)

A powerful, open-source, self-hosted analytics platform for tracking website performance across multiple domains. Real-time analytics, multi-domain support, user authentication, and easy integration with a simple JavaScript SDK.

## 🌟 Features

- 📈 **Real-time Analytics** - Track page views, events, and user sessions in real-time with WebSocket support
- 🌐 **Multi-Domain Support** - Monitor multiple websites from a single dashboard
- 🛡️ **Self-Hosted & Private** - Your data stays on your own server
- 🔑 **User Authentication** - Secure login system with JWT tokens
- 💻 **Responsive Dashboard** - Beautiful, modern UI built with Next.js and TailwindCSS
- ⚡ **Easy Integration** - Simple JavaScript SDK similar to Google Analytics
- � **Event & Goal Tracking** - Custom events and conversion goals
- 👁️ **User Analytics** - Unique visitors, sessions, and behavior tracking
- 📊 **Detailed Reports** - Page views, bounce rates, session duration, and more
- 🗺️ **Geographic Data** - Automatic IP-based location detection
- 📌 **UTM Tracking** - Campaign parameter tracking for marketing analytics
- ♻️ **Data Retention** - Automated cleanup of old data
- 🐳 **Docker Support** - Easy deployment with Docker and Docker Compose

## 📚 Documentation

For comprehensive documentation, see the [docs](docs/) directory:

### Core Documentation
- [API Documentation](docs/API.md) - Complete API reference and endpoints
- [Installation Guide](docs/INSTALLATION.md) - Detailed installation instructions
- [Configuration Guide](docs/CONFIGURATION.md) - System configuration options
- [User Guide](docs/USER_GUIDE.md) - End-user documentation
- [Deployment Guide](docs/DEPLOYMENT.md) - Production deployment instructions
- [Development Guide](docs/DEVELOPMENT.md) - Developer setup and contribution

### Project Information
- [Contributing](docs/CONTRIBUTING.md) - How to contribute to the project
- [Changelog](docs/CHANGELOG.md) - Version history and changes
- [License](docs/LICENSE.md) - License information

### Additional Resources
- [Wiki](https://github.com/AutoBotSolutions/Opensource-Site-Tracking/wiki) - Community wiki with detailed guides
- [License Options](docs/license/README.md) - Commercial licensing information

## 🚀 Live Demo

View the live site at: **https://autobotsolutions.github.io/Opensource-Site-Tracking/**

## Project Structure

```
opensource-site-tracking/
├── backend/                 # FastAPI backend server
│   ├── main.py            # API endpoints and tracking script
│   ├── models.py          # Database models
│   ├── schemas.py         # Pydantic schemas
│   ├── database.py        # Database connection
│   ├── utils.py           # Helper functions
│   ├── config.py          # Configuration
│   ├── init_db.py         # Database initialization
│   ├── requirements.txt   # Python dependencies
│   └── .env              # Environment variables
├── frontend/              # Next.js dashboard
│   ├── src/
│   │   ├── app/          # Next.js app directory
│   │   ├── components/   # React components
│   │   └── lib/         # Utilities and API client
│   ├── package.json      # Node dependencies
│   ├── tsconfig.json     # TypeScript config
│   ├── tailwind.config.ts # Tailwind config
│   └── .env.local       # Frontend environment
├── examples/            # Integration examples
│   ├── html/            # HTML/JavaScript examples
│   ├── python-flask/    # Flask integration
│   └── node-express/    # Express integration
├── README.md            # This file
└── INTEGRATION.md      # Integration guide
```

## Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- pip (Python package manager)
- npm (Node package manager)

### Installation

1. **Navigate to the project directory:**
```bash
cd /home/robbie/Desktop/opensource-site-tracking
```

2. **Install backend dependencies:**
```bash
cd backend
pip3 install -r requirements.txt
```

3. **Install frontend dependencies:**
```bash
cd frontend
npm install
```

4. **Initialize the database:**
```bash
cd backend
python init_db.py
```
This will create an SQLite database and a sample site with credentials.

5. **Start the backend server:**
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

6. **Start the frontend dashboard (in a new terminal):**
```bash
cd frontend
npm run dev
```

7. **Open your browser:**
- Dashboard: http://localhost:3000
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## Getting Started with Analytics

1. **Initialize the database** (first time only):
```bash
cd backend
python init_db.py
```
This creates a default user (admin@example.com / admin123)

2. **Open the dashboard** at http://localhost:3000
3. **Login** with the default credentials or register a new account
4. **Create a new site** by clicking "New Site" and entering your website's name and domain
5. **Copy the integration code** from the site's analytics page
6. **Add the code** to your website (before the closing `</body>` tag)
7. **Visit your website** to start tracking analytics
8. **View analytics** in the dashboard

## Integration

For detailed integration instructions, see [INTEGRATION.md](INTEGRATION.md)

### Quick Frontend Integration

Add this snippet to your website's HTML (replace `YOUR_SITE_KEY` and `YOUR_API_KEY`):

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

### Custom Event Tracking

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
```

## API Documentation

Interactive API documentation available at http://localhost:8000/docs

### Main Endpoints

- `POST /api/track/pageview` - Track a page view
- `POST /api/track/event` - Track a custom event
- `GET /api/sites` - List all sites
- `POST /api/sites` - Create a new site
- `GET /api/sites/{id}` - Get site details
- `GET /api/analytics/{site_id}` - Get analytics for a site
- `GET /tracking-script.js` - JavaScript tracking SDK

## Dashboard Features

- **Real-time visitor tracking** - See visitors as they browse your site
- **Page view analytics** - Track which pages are most popular
- **Event tracking** - Monitor custom events and user actions
- **Referrer analysis** - Know where your traffic comes from
- **Device/browser breakdown** - Understand your visitors' technology
- **Geographic data** - See where your visitors are located
- **Custom date ranges** - View analytics for any time period
- **Multi-domain support** - Track multiple websites from one dashboard

## Configuration

### Backend Configuration

Edit `backend/config.py` to customize:
- Database settings
- CORS origins
- Rate limiting
- Data retention policies
- Server host and port

### Environment Variables

Create or edit `backend/.env`:
```
DATABASE_URL=sqlite:///./analytics.db
SECRET_KEY=your-secret-key-change-in-production
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
```

### Frontend Configuration

Edit `frontend/.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Security

- **API key authentication** - All tracking requests require valid API keys
- **JWT authentication** - Dashboard access requires login with JWT tokens
- **Rate limiting** - Prevent abuse with configurable rate limits
- **CORS protection** - Control which domains can access the API
- **SQL injection prevention** - Parameterized queries protect against SQL injection
- **Input validation** - All inputs are validated using Pydantic schemas
- **IP hashing** - IP addresses are hashed for GDPR compliance
- **Password hashing** - User passwords are hashed using bcrypt

## Examples

Check the `examples/` directory for integration examples:
- `examples/html/` - Plain HTML/JavaScript integration
- `examples/python-flask/` - Flask backend integration
- `examples/node-express/` - Express backend integration

## Production Deployment

### Docker Deployment (Recommended)

The easiest way to deploy is using Docker:

```bash
# Build and start all services
docker-compose up -d

# For development with hot reload
docker-compose -f docker-compose.dev.yml up -d
```

### Backend

For production, consider:
- Use PostgreSQL instead of SQLite
- Set up a reverse proxy (nginx)
- Enable HTTPS
- Use a process manager (systemd, supervisor)
- Set strong SECRET_KEY in environment
- Configure proper CORS origins

### Docker

The Docker setup includes:
- Backend API with auto-restart
- Frontend dashboard with production build
- Persistent volume for database
- Network isolation

### Frontend

For production:
```bash
cd frontend
npm run build
npm start
```

Or deploy to Vercel, Netlify, or any Node.js hosting platform.

## Troubleshooting

### Database locked error
- Ensure only one backend process is running
- Use PostgreSQL for production instead of SQLite

### CORS errors
- Add your domain to CORS_ORIGINS in backend/.env
- Check that the frontend API URL is correct

### No data appearing
- Verify site_key and api_key are correct
- Check browser console for errors
- Ensure tracking script URL is accessible
- Check backend logs for errors

## License

This project is available under multiple licensing options to suit different use cases.

### Open Source License
- **MIT License** - Free for all uses with attribution required
  - See [LICENSE.md](LICENSE.md) for full terms
  - Perfect for personal projects, open source projects, and internal use

### Commercial Licenses
For commercial use without attribution, enterprise deployments, or redistribution, we offer several commercial license options:

- **Standard Commercial License** ($499/year) - Commercial use without attribution
- **Enterprise License** ($2,499/year) - Enterprise deployments with priority support
- **OEM License** ($9,999/year) - Redistribution and embedding rights
- **White Label License** ($19,999/year) - Rebranding and resale rights

For detailed license information, pricing, and terms, see the [License Documentation](docs/license/README.md).

### License Owner
**Robert Trenaman | Auto Bot Solution (Software Customs) | Flushing MI**

### Contact
- **Sales:** sales@opensite-analytics.com
- **Legal:** legal@opensite-analytics.com
- **Support:** support@opensite-analytics.com

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please open an issue on the repository.
