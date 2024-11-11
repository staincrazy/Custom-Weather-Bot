from dataclasses import dataclass

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