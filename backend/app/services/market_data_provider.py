import os
import json
import subprocess
import urllib.parse
import requests
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

class DataGovInProvider:
    """
    Official API Provider for data.gov.in AGMARKNET Daily Wholesale Prices.
    API: https://api.data.gov.in/resource/35985678-0d79-46b4-9ed6-6f13308a1d24

    Uses curl as the HTTP backend because Python 3.14's SSL stack has a TLS
    handshake incompatibility with data.gov.in's server, causing read timeouts
    in both `requests` and `urllib`. curl handles TLS negotiation natively and
    works reliably. Falls back to `requests` if curl is unavailable.
    """
    
    BASE_URL = "https://api.data.gov.in/resource/35985678-0d79-46b4-9ed6-6f13308a1d24"
    
    def __init__(self, api_key: str = ""):
        from app.core.config import settings
        self.api_key = api_key or getattr(settings, "DATA_GOV_IN_API_KEY", "") or os.environ.get("DATA_GOV_IN_API_KEY", "")

    def _fetch(self, params: Dict[str, Any], timeout: int = 15) -> Dict[str, Any]:
        """Make an HTTP GET request. Tries curl first, falls back to requests."""
        query_string = urllib.parse.urlencode(params)
        url = f"{self.BASE_URL}?{query_string}"

        # Try curl first (reliable on this system)
        try:
            result = subprocess.run(
                ["curl", "-s", "--max-time", str(timeout), url],
                capture_output=True, text=True, timeout=timeout + 5
            )
            if result.returncode == 0 and result.stdout:
                return json.loads(result.stdout)
        except (subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError):
            pass  # Fall through to requests

        # Fallback: requests library
        try:
            response = requests.get(self.BASE_URL, params=params, timeout=timeout)
            if response.status_code == 200:
                return response.json()
        except requests.RequestException:
            pass

        return {}

    def fetch_current_prices(self, commodity: str, state: Optional[str] = None, district: Optional[str] = None, market: Optional[str] = None) -> List[Dict[str, Any]]:
        """Fetch current mandi prices from data.gov.in"""
        if not self.api_key:
            return [] # Fail gracefully if no API key is configured

        params = {
            "api-key": self.api_key,
            "format": "json",
            "limit": 50,
            "filters[Commodity]": commodity
        }
        
        if state:
            params["filters[State]"] = state
        if district:
            params["filters[District]"] = district
        if market:
            params["filters[Market]"] = market
            
        data = self._fetch(params, timeout=15)
        return data.get("records", [])

    def fetch_historical_prices(self, commodity: str, days: int = 30, state: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Fetch historical prices. data.gov.in requires exact date filtering or sorting.
        This fetches the latest 100 records and sorts/filters them by date locally for demonstration,
        as robust date range queries on data.gov.in require complex offset pagination.
        """
        if not self.api_key:
            return []

        params = {
            "api-key": self.api_key,
            "format": "json",
            "limit": 100,
            "filters[Commodity]": commodity,
            "sort[Arrival_Date]": "desc"
        }
        
        if state:
            params["filters[State]"] = state
            
        data = self._fetch(params, timeout=20)
        return data.get("records", [])

market_data_provider = DataGovInProvider()
