from dataclasses import dataclass

@dataclass
class KeyConfig:
    """Configuration for key management"""
    keys_directory: str = "private_keys"
    encoding: str = "utf-8"
    cache_size: int = 32
    directory_mode: int = 0o700  # Expected directory permissions
    file_mode: int = 0o600      # Expected file permissions
