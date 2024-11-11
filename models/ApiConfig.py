from dataclasses import dataclass
from typing import Dict

from KeyManagerUtils import get_private_key


@dataclass
class ApiConfig:
    """Configuration for API endpoints and keys"""
    base_url: str = "https://api.api-ninjas.com/v1"
    api_key_file: str = 'private_api_ninjas_key.txt'

    @property
    def api_utils_key_path(self):
        return self.api_key_file

    @property
    def headers(self) -> Dict[str, str]:
        """Get default API headers with authentication"""
        return {'X-Api-Key': get_private_key(self.api_utils_key_path)}

    def get_url(self, endpoint: str) -> str:
        """Construct full URL for given endpoint"""
        return f"{self.base_url}/{endpoint}"
