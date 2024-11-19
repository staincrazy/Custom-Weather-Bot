import json
from pathlib import Path
from typing import Optional

from telegram import Update

from models.UserConfig import UserLogConfig, UserRequest


class UserRequestLogger:
    """Handler for logging user requests"""

    def __init__(self, config: Optional[UserLogConfig] = None):
        self.config = config or UserLogConfig()
        self._ensure_log_directory()

    def _ensure_log_directory(self) -> None:
        """Create log directory if it doesn't exist"""
        Path(self.config.log_directory).mkdir(exist_ok=True)

        if not self.config.log_path.exists():
            self.config.log_path.write_text('[]')

    def log_request(self, update: Update) -> None:
        """Log user request to file"""
        try:
            # Create request object
            request = UserRequest.from_update(update)

            # Read existing logs
            try:
                logs = json.loads(self.config.log_path.read_text())
            except json.JSONDecodeError:
                logs = []

            # Append new request
            logs.append(request.to_dict())

            # Write updated logs
            self.config.log_path.write_text(
                json.dumps(logs, indent=2, ensure_ascii=False)
            )

        except Exception as e:
            print(f"Error logging user request: {e}")

    def get_user_history(self, user_id: int) -> list[dict]:
        """Get all requests from specific user"""
        try:
            logs = json.loads(self.config.log_path.read_text())
            return [
                log for log in logs
                if log['user']['id'] == user_id
            ]
        except Exception as e:
            print(f"Error retrieving user history: {e}")
            return []