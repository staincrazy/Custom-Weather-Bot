from dataclasses import dataclass
from datetime import datetime
from itertools import chain
from pathlib import Path
from typing import Optional
import json
from telegram import Update

@dataclass
class UserLogConfig:
    """Configuration for user request logging"""
    log_directory: str = "logs"
    user_log_file: str = 'user_requests.json'
    date_format: str = "%Y-%m-%d %H:%M:%S"

    @property
    def log_path(self) -> Path:
        return Path(self.log_directory) / self.user_log_file


@dataclass
class UserRequest:
    """Data model for user request information"""
    timestamp: str
    user_id: int
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    chat_id: int
    message_text: str
    chat_type: str

    @classmethod
    def from_update(cls, update: Update):
        """ Create UserRequest from telegram Update """
        now = datetime.now()
        user = update.effective_user
        chat = update.effective_chat

        return cls(
            timestamp=now.strftime(UserLogConfig.date_format),
            user_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            chat_id=chat.id,
            message_text=update.message.text,
            chat_type=chat.type
        )

    def to_dict(self) -> dict:
        """Convert request to dictionary for serialization"""
        return {
            'timestamp': self.timestamp,
            'user': {
                'id': self.user_id,
                'username': self.username,
                'first_name': self.first_name,
                'last_name': self.last_name
            },
            'chat': {
                'id': self.chat_id,
                'type': self.chat_type
            },
            'message': {
                'text': self.message_text
            }
        }


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