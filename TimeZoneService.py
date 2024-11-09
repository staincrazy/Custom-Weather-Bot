from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Tuple
from zoneinfo import ZoneInfo
from timezonefinder import TimezoneFinder
from ApiUtils import APIService


@dataclass
class TimezoneConfig:
    """Configuration for timezone service"""
    default_time_format: str = "%H-%M"
    default_timezone: str = "UTC"


class TimezoneService:
    """Service for handling timezone and time calculations"""

    def __init__(
            self,
            config: Optional[TimezoneConfig] = None,
            api_service: Optional[APIService] = None
    ):
        """
        Initialize timezone service

        Args:
            config: Configuration for timezone handling
            api_service: Service for API calls (coordinates lookup)
        """
        self.config = config or TimezoneConfig()
        self.api_service = api_service or APIService()
        self.timezone_finder = TimezoneFinder()

    def get_coordinates(self, city_name: str) -> Optional[Tuple[float, float]]:
        """
        Get coordinates for a city

        Args:
            city_name: Name of the city

        Returns:
            Tuple of (latitude, longitude) or None if not found
        """
        lat, lng = self.api_service.get_city_coordinates(city_name)
        if lat is None or lng is None:
            return None
        return lat, lng

    def get_timezone(self, city_name: str) -> Optional[str]:
        """
        Get timezone for a city

        Args:
            city_name: Name of the city

        Returns:
            Timezone string or None if not found
        """
        coordinates = self.get_coordinates(city_name)
        if not coordinates:
            return None

        lat, lng = coordinates
        return self.timezone_finder.timezone_at(lat=lat, lng=lng)

    def get_current_time(
            self,
            city_name: str,
            time_format: Optional[str] = None
    ) -> str:
        """
        Get current time for a city

        Args:
            city_name: Name of the city
            time_format: Optional custom time format

        Returns:
            Formatted time string
        """
        format_str = time_format or self.config.default_time_format
        timezone_str = self.get_timezone(city_name)

        try:
            if timezone_str:
                timezone = ZoneInfo(timezone_str)
            else:
                timezone = ZoneInfo(self.config.default_timezone)

            return datetime.now(tz=timezone).strftime(format_str)

        except Exception as e:
            # Fallback to system time if there's any error
            return datetime.now().strftime(format_str)


# Create default instance for backward compatibility
_default_service = TimezoneService()
get_time_for_timezone = _default_service.get_current_time


class TimezoneFormatter:
    """Utility class for formatting timezone-related information"""

    @staticmethod
    def format_time_difference(
            source_city: str,
            target_city: str,
            timezone_service: Optional[TimezoneService] = None
    ) -> str:
        """
        Format time difference between two cities

        Args:
            source_city: Source city name
            target_city: Target city name
            timezone_service: Optional timezone service instance

        Returns:
            Formatted string with time difference
        """
        service = timezone_service or TimezoneService()

        source_tz = service.get_timezone(source_city)
        target_tz = service.get_timezone(target_city)

        if not (source_tz and target_tz):
            return "Unable to determine time difference - timezone not found"

        now = datetime.now(ZoneInfo("UTC"))
        source_time = now.astimezone(ZoneInfo(source_tz))
        target_time = now.astimezone(ZoneInfo(target_tz))

        diff_hours = (target_time.utcoffset() - source_time.utcoffset()).total_seconds() / 3600

        return (
            f"Time difference between {source_city} and {target_city}: "
            f"{abs(diff_hours):.1f} hours {'ahead' if diff_hours > 0 else 'behind'}"
        )


if __name__ == '__main__':
    # Example usage
    service = TimezoneService()

    # Basic time lookup
    print(f"London time: {service.get_current_time('London')}")
    print(f"Tokyo time: {service.get_current_time('Tokyo')}")

    # Time difference example
    formatter = TimezoneFormatter()
    print(formatter.format_time_difference('London', 'Tokyo'))

    # Custom format example
    print(
        service.get_current_time(
            'New York',
            time_format='%Y-%m-%d %H:%M:%S %Z'
        )
    )