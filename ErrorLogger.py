from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional, Callable
import logging
import traceback
from pathlib import Path


@dataclass
class LogConfig:
    """Configuration for logger"""
    log_file: str = "error.logs"
    log_format: str = "%(asctime)s - %(levelname)s - %(message)s"
    date_format: str = "%Y-%m-%d %H:%M:%S"
    encoding: str = "utf-8"
    level: int = logging.ERROR


class EventLogger:
    """Handles logging of events and errors"""

    def __init__(self, config: Optional[LogConfig] = None):
        """Initialize logger with configuration"""
        self.config = config or LogConfig()
        self._logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        """Set up and configure logger"""
        # Create logger
        logger = logging.getLogger('WeatherBotLogger')
        logger.setLevel(self.config.level)

        # Create handlers
        file_handler = logging.FileHandler(
            self.config.log_file,
            encoding=self.config.encoding
        )
        file_handler.setLevel(self.config.level)

        # Create formatters
        formatter = logging.Formatter(
            fmt=self.config.log_format,
            datefmt=self.config.date_format
        )
        file_handler.setFormatter(formatter)

        # Add handlers to logger
        if not logger.handlers:
            logger.addHandler(file_handler)

        return logger

    def log_event(
            self,
            event: Optional[Any] = None,
            function: Optional[Callable] = None,
            user_input: Optional[Any] = None,
            level: int = logging.ERROR
    ) -> None:
        """
        Log an event with context information

        Args:
            event: The event or exception to log
            function: The function where the event occurred
            user_input: The input that caused the event
            level: Logging level (default: ERROR)
        """
        # Get function name if available
        func_name = (
            function.__name__ if hasattr(function, '__name__')
            else str(function)
        )

        # Create detailed message
        message = self._format_message(event, func_name, user_input)

        # Log with appropriate level
        if isinstance(event, Exception):
            self._logger.exception(message)
        else:
            self._logger.log(level, message)

    def _format_message(
            self,
            event: Optional[Any],
            func_name: str,
            user_input: Optional[Any]
    ) -> str:
        """Format log message with consistent structure"""
        parts = []

        # Add event information
        if event is not None:
            if isinstance(event, Exception):
                parts.append(f"Event: {type(event).__name__}: {str(event)}")
                parts.append(f"Traceback: {traceback.format_exc()}")
            else:
                parts.append(f"Event: {str(event)}")

        # Add function information
        parts.append(f"Function: {func_name}")

        # Add user input if available
        if user_input is not None:
            parts.append(f"User Input: {str(user_input)}")

        return " | ".join(parts)

    def rotate_log_file(self, max_size_mb: float = 10.0) -> None:
        """
        Rotate log file if it exceeds maximum size

        Args:
            max_size_mb: Maximum log file size in megabytes
        """
        log_path = Path(self.config.log_file)
        if log_path.exists():
            size_mb = log_path.stat().st_size / (1024 * 1024)
            if size_mb > max_size_mb:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_path = log_path.with_name(f"{log_path.stem}_{timestamp}{log_path.suffix}")
                log_path.rename(backup_path)


# Create default logger instance
_default_logger = EventLogger()


# For backward compatibility
def logEvent(
        event: Optional[Any] = None,
        function: Optional[Callable] = None,
        user_input: Optional[Any] = None
) -> None:
    """
    Backward compatible function for logging events

    Args:
        event: The event or exception to log
        function: The function where the event occurred
        user_input: The input that caused the event
    """
    _default_logger.log_event(event, function, user_input)


if __name__ == '__main__':
    # Example usage
    logger = EventLogger()

    # Example 1: Log an exception
    try:
        raise ValueError("Test error")
    except Exception as e:
        logger.log_event(e, logEvent, "test input")

    # Example 2: Log a custom event
    logger.log_event(
        "Custom event",
        lambda x: x,
        {"test": "data"},
        level=logging.INFO
    )