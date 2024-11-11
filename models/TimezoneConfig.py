from dataclasses import dataclass

@dataclass
class TimezoneConfig:
    """Configuration for timezone service"""
    default_time_format: str = "%H-%M"
    default_timezone: str = "UTC"