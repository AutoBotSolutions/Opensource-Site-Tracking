"""
Example Flask application with OpenSite Analytics integration
"""

from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Configuration
SITE_KEY = 'YOUR_SITE_KEY'
API_KEY = 'YOUR_API_KEY'
TRACKING_ENDPOINT = 'http://localhost:8000/api/track'

def track_pageview(url, title, referrer=None):
    """Track a page view"""
    try:
        requests.post(f'{TRACKING_ENDPOINT}/pageview', json={
            'site_id': SITE_KEY,
            'api_key': API_KEY,
            'url': url,
            'title': title,
            'referrer': referrer,
            'user_agent': request.headers.get('User-Agent')
        })
    except Exception as e:
        print(f"Tracking error: {e}")

def track_event(event_name, event_data=None, url=None):
    """Track a custom event"""
    try:
        requests.post(f'{TRACKING_ENDPOINT}/event', json={
            'site_id': SITE_KEY,
            'api_key': API_KEY,
            'event_name': event_name,
            'event_data': event_data,
            'url': url or request.url,
            'user_agent': request.headers.get('User-Agent')
        })
    except Exception as e:
        print(f"Tracking error: {e}")

@app.route('/')
def home():
    track_pageview(request.url, 'Home Page', request.referrer)
    return render_template('index.html')

@app.route('/about')
def about():
    track_pageview(request.url, 'About Page', request.referrer)
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Track form submission event
        track_event('contact_form_submit', {
            'email': request.form.get('email'),
            'subject': request.form.get('subject')
        })
        return 'Message sent!'
    
    track_pageview(request.url, 'Contact Page', request.referrer)
    return render_template('contact.html')

@app.route('/download/<filename>')
def download(filename):
    # Track download event
    track_event('file_download', {
        'filename': filename
    })
    return f'Downloading {filename}'

if __name__ == '__main__':
    app.run(debug=True, port=5000)
