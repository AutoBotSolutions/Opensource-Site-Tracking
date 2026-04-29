/**
 * Example Express application with OpenSite Analytics integration
 */

const express = require('express');
const axios = require('axios');
const app = express();

// Configuration
const SITE_KEY = 'YOUR_SITE_KEY';
const API_KEY = 'YOUR_API_KEY';
const TRACKING_ENDPOINT = 'http://localhost:8000/api/track';

// Middleware to parse JSON
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Track page view function
async function trackPageview(url, title, referrer, userAgent) {
  try {
    await axios.post(`${TRACKING_ENDPOINT}/pageview`, {
      site_id: SITE_KEY,
      api_key: API_KEY,
      url,
      title,
      referrer,
      user_agent: userAgent
    });
  } catch (error) {
    console.error('Tracking error:', error.message);
  }
}

// Track event function
async function trackEvent(eventName, eventData, url, userAgent) {
  try {
    await axios.post(`${TRACKING_ENDPOINT}/event`, {
      site_id: SITE_KEY,
      api_key: API_KEY,
      event_name: eventName,
      event_data: eventData,
      url,
      user_agent: userAgent
    });
  } catch (error) {
    console.error('Tracking error:', error.message);
  }
}

// Middleware to track all page views
app.use(async (req, res, next) => {
  const userAgent = req.headers['user-agent'];
  await trackPageview(
    req.protocol + '://' + req.get('host') + req.originalUrl,
    'Express Page',
    req.get('referrer'),
    userAgent
  );
  next();
});

// Routes
app.get('/', (req, res) => {
  res.send('Home Page');
});

app.get('/about', (req, res) => {
  res.send('About Page');
});

app.post('/api/contact', async (req, res) => {
  // Track form submission event
  await trackEvent('contact_form_submit', {
    email: req.body.email,
    subject: req.body.subject
  }, req.url, req.headers['user-agent']);
  
  res.json({ message: 'Message sent!' });
});

app.post('/api/purchase', async (req, res) => {
  // Track purchase event
  await trackEvent('purchase_completed', {
    product_id: req.body.productId,
    amount: req.body.amount,
    currency: req.body.currency || 'USD'
  }, req.url, req.headers['user-agent']);
  
  res.json({ message: 'Purchase completed!' });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
