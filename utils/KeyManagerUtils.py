from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Dict
import os
import json
from functools import lru_cache
from models.KeyKonfig import KeyConfig


class KeyManager:
    """Manages secure access to private keys"""

    def __init__(self, config: Optional[KeyConfig] = None):
        """Initialize key manager with configuration"""
        self.config = config or KeyConfig()
        self._keys_path = Path(self.config.keys_directory)
        self._validate_keys_directory()

    def _validate_keys_directory(self) -> None:
        """Ensure keys directory exists and has proper permissions"""
        if not self._keys_path.exists():
            raise FileNotFoundError(
                f"Keys directory not found: {self._keys_path}"
            )

        # Check directory permissions (on Unix-like systems)
        if os.name == 'posix':
            stat = self._keys_path.stat()
            mode = stat.st_mode & 0o777
            if mode != self.config.directory_mode:
                # Instead of raising error, fix permissions
                try:
                    os.chmod(self._keys_path, self.config.directory_mode)
                except Exception as e:
                    print(f"Warning: Could not set directory permissions: {e}")

    @lru_cache(maxsize=32)
    def get_key(self, filename: str, strip: bool = True) -> str:
        """
        Get private key from environment variable or file

        Args:
            filename: Name of the key file
            strip: Whether to strip whitespace from the key

        Returns:
            Key string

        Raises:
            FileNotFoundError: If key file doesn't exist
            PermissionError: If key file has incorrect permissions
            ValueError: If key file is empty or invalid
        """
        # Map filenames to environment variable names
        env_vars = {
            'private_telegram_key.txt': 'TELEGRAM_BOT_TOKEN',
            'private_owm_key.txt': 'OPENWEATHER_API_KEY',
            'private_api_ninjas_key.txt': 'API_NINJAS_KEY'
        }

        # Check environment variable first
        env_var = env_vars.get(filename)
        if env_var and os.environ.get(env_var):
            return os.environ[env_var]

        # Fallback to file
        key_path = self._resolve_key_path(filename)
        self._validate_key_file(key_path)

        try:
            key = key_path.read_text(encoding=self.config.encoding)
            return key.strip() if strip else key
        except Exception as e:
            raise ValueError(f"Failed to read key file: {filename}") from e
    def _resolve_key_path(self, filename: str) -> Path:
        """Resolve full path to key file"""
        if os.path.isabs(filename):
            return Path(filename)
        return self._keys_path / filename  # _keys_path already includes private_keys

    def _validate_key_file(self, key_path: Path) -> None:
        """Validate key file existence and permissions"""
        if not key_path.is_file():
            raise FileNotFoundError(f"Key file not found: {key_path}")

        if os.name == 'posix':
            stat = key_path.stat()
            mode = stat.st_mode & 0o777
            if mode != self.config.file_mode:
                # Instead of raising error, fix permissions
                try:
                    os.chmod(key_path, self.config.file_mode)
                except Exception as e:
                    print(f"Warning: Could not set file permissions: {e}")

        if key_path.stat().st_size == 0:
            raise ValueError(f"Key file is empty: {key_path}")

    def save_key(
            self,
            filename: str,
            key: str,
            overwrite: bool = False
    ) -> None:
        """
        Save key to file with secure permissions

        Args:
            filename: Name of the key file
            key: Key string to save
            overwrite: Whether to overwrite existing key

        Raises:
            FileExistsError: If key file exists and overwrite is False
            PermissionError: If unable to set secure permissions
        """
        key_path = self._resolve_key_path(filename)

        if key_path.exists() and not overwrite:
            raise FileExistsError(
                f"Key file already exists: {key_path}. "
                "Set overwrite=True to replace"
            )

        # Create directory if it doesn't exist
        key_path.parent.mkdir(parents=True, exist_ok=True)

        # Set directory permissions
        if os.name == 'posix':
            os.chmod(key_path.parent, 0o700)

        # Write key with secure permissions
        if os.name == 'posix':
            # Create with restricted permissions from the start
            fd = os.open(key_path, os.O_WRONLY | os.O_CREAT, 0o600)
            with os.fdopen(fd, 'w') as f:
                f.write(key)
        else:
            # On non-POSIX systems, do our best
            key_path.write_text(key, encoding=self.config.encoding)

    def list_keys(self) -> Dict[str, str]:
        """
        List all available keys and their files

        Returns:
            Dictionary of key names and their file paths
        """
        return {
            path.name: str(path)
            for path in self._keys_path.glob("*.txt")
            if path.is_file()
        }


# Create default instance for backward compatibility
_default_manager = KeyManager()


def get_private_key(filename: str) -> str:
    """
    Backward compatible function for getting private keys

    Args:
        filename: Name of the key file

    Returns:
        Key string
    """
    return _default_manager.get_key(filename)


if __name__ == '__main__':
    # Example usage
    key_manager = KeyManager()

    # List available keys
    print("Available keys:", key_manager.list_keys())

    # Read a key
    try:
        telegram_key = key_manager.get_key('private_telegram_key.txt')
        print("Successfully read key")
    except Exception as e:
        print(f"Error reading key: {e}")

    # Save a new key (example)
    try:
        key_manager.save_key(
            'new_api_key.txt',
            'my-secret-key-123',
            overwrite=False
        )
        print("Successfully saved new key")
    except Exception as e:
        print(f"Error saving key: {e}")