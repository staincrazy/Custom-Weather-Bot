from dataclasses import dataclass
from pathlib import Path
import logging

@dataclass
class LogConfig:
    """Configuration for logger"""
    base_logs_folder: str = 'error_logs'
    log_file: str = "error.logs"
    log_format: str = "%(asctime)s - %(levelname)s - %(message)s"
    date_format: str = "%Y-%m-%d %H:%M:%S"
    encoding: str = "utf-8"
    level: int = logging.ERROR

    @property
    def error_logs_path(self) -> str:
        return str(Path(self.base_logs_folder)/self.log_file)