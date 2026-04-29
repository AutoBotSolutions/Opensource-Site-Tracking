import requests
from typing import Optional, Dict
from config import settings


class GeoIPService:
    """Service for geographic IP lookup"""
    
    def __init__(self):
        self.api_url = "http://ip-api.com/json/"
    
    def get_location(self, ip_address: str) -> Dict[str, Optional[str]]:
        """
        Get geographic location for an IP address
        Using free IP-API service (limited to 45 requests per minute)
        
        For production, consider:
        - Using a paid service like MaxMind GeoIP2
        - Running a local GeoIP database
        - Implementing caching
        """
        try:
            # Don't lookup private IPs
            if ip_address in ('127.0.0.1', 'localhost', 'unknown', ''):
                return {
                    'country': None,
                    'city': None
                }
            
            response = requests.get(
                f"{self.api_url}{ip_address}",
                timeout=2
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'country': data.get('country'),
                    'city': data.get('city')
                }
        except Exception as e:
            # Fail silently - don't block tracking if geo lookup fails
            pass
        
        return {
            'country': None,
            'city': None
        }


# Singleton instance
geoip_service = GeoIPService()
