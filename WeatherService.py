from dataclasses import dataclass
from typing import Optional, Dict, Any, Union, Tuple
import requests
from datetime import datetime

from TimeZoneService import TimezoneService
from KeyManagerUtils import KeyManager


@dataclass
class WeatherConfig:
    """Configuration for weather service"""
    base_url: str = "https://api.openweathermap.org/data/2.5"
    owm_key_file: str = 'private_owm_key.txt'
    temp_precision: int = 1
    celsius_symbol: str = "°C"
    fahrenheit_symbol: str = "°F"

    @property
    def own_api_key_path(self):
        return self.owm_key_file



class Temperature:
    """Class for handling temperature conversions and formatting"""

    def __init__(self, kelvin: float):
        self.kelvin = float(kelvin)

    @property
    def celsius(self) -> float:
        """Convert Kelvin to Celsius"""
        return self.kelvin - 273.15

    @property
    def fahrenheit(self) -> float:
        """Convert Kelvin to Fahrenheit"""
        return (self.celsius * 9 / 5) + 32

    def format(self, precision: int = 1) -> Dict[str, str]:
        """Format temperature in both Celsius and Fahrenheit"""
        return {
            'celsius': f"{self.celsius:.{precision}f}",
            'fahrenheit': f"{self.fahrenheit:.{precision}f}"
        }


class WeatherData:
    """Class for parsing and storing weather data"""

    def __init__(self, data: Dict[str, Any]):
        self.raw_data = data
        self.temperature = Temperature(data['main']['temp'])
        self.feels_like = Temperature(data['main']['feels_like'])
        self.condition = data['weather'][0]['main']
        self.description = data['weather'][0]['description']
        self.city_name = data['name']
        self.humidity = data['main'].get('humidity')
        self.pressure = data['main'].get('pressure')
        self.wind_speed = data['wind'].get('speed')

    def format_temperatures(self, precision: int = 1) -> Tuple[Dict[str, str], Dict[str, str]]:
        """Format both actual and feels-like temperatures"""
        return (
            self.temperature.format(precision),
            self.feels_like.format(precision)
        )


class OpenWeatherMapAPI:
    """Handler for OpenWeatherMap API requests"""

    def __init__(
            self,
            config: Optional[WeatherConfig] = None,
            key_manager: Optional[KeyManager] = None,
            timezone_service: Optional[TimezoneService] = None
    ):
        """Initialize the API handler"""
        self.config = config or WeatherConfig()
        self.key_manager = key_manager or KeyManager()
        self.timezone_service = timezone_service or TimezoneService()
        self._api_key = self.key_manager.get_key(self.config.owm_key_file)

    def get_current_weather(self, city_name: str) -> WeatherData:
        """
        Get current weather for a city

        Args:
            city_name: Name of the city

        Returns:
            WeatherData object

        Raises:
            ValueError: If city not found or invalid response
            TypeError: If invalid input types
        """
        if not isinstance(city_name, str):
            raise TypeError("City name must be a string")

        url = f"{self.config.base_url}/weather"
        params = {
            'q': city_name,
            'appid': self._api_key
        }

        response = requests.get(url, params=params)

        if response.status_code == 404:
            raise ValueError(f"City not found: {city_name}")

        response.raise_for_status()
        return WeatherData(response.json())

    def format_weather_response(self, weather_data: WeatherData) -> str:
        """Format weather data into a readable message"""
        current_time = self.timezone_service.get_current_time(weather_data.city_name)
        temps, feels = weather_data.format_temperatures(self.config.temp_precision)

        return (
            f"At {current_time} in {weather_data.city_name} current temperature is "
            f"{temps['celsius']}{self.config.celsius_symbol} / "
            f"{temps['fahrenheit']}{self.config.fahrenheit_symbol} "
            f"(feels like {feels['celsius']}{self.config.celsius_symbol} / "
            f"{feels['fahrenheit']}{self.config.fahrenheit_symbol}). "
            f"The weather is {weather_data.condition} ({weather_data.description})"
        )

    def get_formatted_weather(self, city_name: str) -> str:
        """
        Get formatted weather report for a city

        Args:
            city_name: Name of the city

        Returns:
            Formatted weather report string
        """
        try:
            weather_data = self.get_current_weather(city_name)
            return self.format_weather_response(weather_data)
        except ValueError as e:
            return "City not found. Please, try again."
        except Exception as e:
            return f"Error getting weather data: {str(e)}"


# Create default instance for backward compatibility
_default_api = OpenWeatherMapAPI()
weather_request = _default_api.get_formatted_weather

if __name__ == '__main__':
    # Example usage
    api = OpenWeatherMapAPI()

    # Basic weather request
    try:
        print(api.get_formatted_weather("London"))
    except Exception as e:
        print(f"Error: {e}")

    # Detailed weather data
    try:
        weather_data = api.get_current_weather("Paris")
        print(f"Temperature: {weather_data.temperature.celsius:.1f}°C")
        print(f"Humidity: {weather_data.humidity}%")
        print(f"Wind Speed: {weather_data.wind_speed} m/s")
    except Exception as e:
        print(f"Error: {e}")