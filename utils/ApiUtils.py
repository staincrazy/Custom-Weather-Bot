import random
from typing import Optional, Dict, Any

import requests
from mypy.types import names
from requests import Response

from utils.ErrorLogger import logEvent
from models.ApiConfig import ApiConfig


class ApiClient:
    """Base API client handling requests and error handling"""

    def __init__(self, config: ApiConfig):
        self.config = config

    def _make_request(
            self,
            endpoint: str,
            params: Optional[Dict[str, Any]] = None,
            extra_headers: Optional[Dict[str, str]] = None
    ) -> Response:
        """Make HTTP request with error handling"""
        headers = self.config.headers
        if extra_headers:
            headers.update(extra_headers)

        response = requests.get(
            self.config.get_url(endpoint),
            headers=headers,
            params=params
        )
        response.raise_for_status()
        return response


class CityAPI(ApiClient):
    """Handle city-related API requests"""

    def _format_city_response(self, city_data) -> Optional[str]:

        is_capital: str = 'not capital'

        if city_data is None:
            return "There is no such a city"

        if city_data['is_capital']:
            is_capital = 'capital'

        return (
            "Just some cold facts: "
            f"{city_data['name']} is {is_capital} of {city_data['country']} with "
            f"the population of {city_data['population']} (but that's not for sure, "
            f"because we're using free API :D) people and on the map can be found in "
            f"{city_data['region']}!"
        )


    def get_city_data(self, city_name: str) -> Dict[str, Any]:
        """Get comprehensive city data"""
        try:
            response = self._make_request('city', params={'name': city_name})
            return response.json()[0]
        except Exception as e:
            logEvent(e.__cause__, self.get_city_data, user_input=city_name)
            raise

    def get_coordinates(self, city_name: str) -> tuple[Optional[float], Optional[float]]:
        """Get city coordinates (latitude, longitude)"""
        try:
            city_data = self.get_city_data(city_name)
            return city_data['latitude'], city_data['longitude']
        except Exception as e:
            logEvent(e.__cause__, self.get_coordinates, user_input=city_name)
            return None, None

    def get_population_info(self, city_name: str) -> str:
        """Get formatted population information"""
        if not isinstance(city_name, str):
            raise TypeError("City name must be a string")

        try:
            city_data = self.get_city_data(city_name)
            return self._format_city_response(city_data)

        except Exception as e:
            logEvent(e.__cause__, self.get_population_info, user_input=city_name)
            return f"Something is wrong. Are you sure there is such a city? Can you check the map please?"


class HistoricalAPI(ApiClient):
    """Handle historical events API requests"""

    def get_random_event(self, year: Optional[int] = None) -> str:
        """Get random historical event, optionally for specific year"""
        if year is None:
            year = random.randint(-351, 2023)

        try:
            response = self._make_request('historicalevents', params={'year': year})
            event = response.json()[0]['event']
            return f'Did you know that in year: {year} - {event}'
        except Exception as e:
            logEvent(e.__cause__, self.get_random_event, user_input=year)
            return "Nothing to show this time"


class ImageAPI(ApiClient):
    """Handle random image API requests"""

    def get_random_image(self, category: Optional[str] = None) -> Optional[bytes]:
        """Get random image data directly"""
        try:
            params = {'category': category} if category else None
            response = self._make_request(
                endpoint='randomimage',
                params=params,
                extra_headers={'Accept': 'image/jpg'}
            )
            return response.content if response.ok else None
        except Exception as e:
            logEvent(e.__cause__, self.get_random_image)
            return None


class APIService:
    """Main service class combining all API functionality"""

    def __init__(self, config: Optional[ApiConfig] = None):
        self.config = config or ApiConfig()
        self.city_api = CityAPI(self.config)
        self.historical_api = HistoricalAPI(self.config)
        self.image_api = ImageAPI(self.config)

    def get_city_coordinates(self, city_name: str) -> tuple[Optional[float], Optional[float]]:
        return self.city_api.get_coordinates(city_name)

    def get_city_population_info(self, city_name: str) -> str:
        return self.city_api.get_population_info(city_name)

    def get_random_event(self, year: Optional[int] = None) -> str:
        return self.historical_api.get_random_event(year)

    def get_random_image(self, category: Optional[str] = None) -> bool:
        return self.image_api.get_random_image(category)


# Create a default instance for backward compatibility
_default_service = APIService()
get_city_lat = lambda city_name: _default_service.get_city_coordinates(city_name)[0]
get_city_lng = lambda city_name: _default_service.get_city_coordinates(city_name)[1]
get_city_population_info = _default_service.get_city_population_info
get_random_event = _default_service.get_random_event
get_random_image = _default_service.get_random_image

if __name__ == '__main__':
    # Example usage
    api_service = APIService()
    print(api_service.get_random_image())
    print(api_service.get_city_population_info('London'))