from dataclasses import dataclass
from typing import Optional
from pathlib import Path
from telegram import Update
from datetime import datetime

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

