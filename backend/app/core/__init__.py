"""
Core module initialization file for the SpeakPro backend application.
This module contains core functionality and configurations used throughout the application.
"""

from typing import Dict, Any

# Version information
__version__ = "1.0.0"

# Core configuration defaults
DEFAULT_CONFIG: Dict[str, Any] = {
    "APP_NAME": "SpeakPro",
    "API_VERSION": "v1",
    "DEFAULT_LANGUAGE": "en",
    "PAGINATION_DEFAULT_LIMIT": 10,
    "PAGINATION_MAX_LIMIT": 100,
}

# Module level variables
SUPPORTED_LANGUAGES = ["en", "ja", "es", "fr", "zh"]
SUPPORTED_TIMEZONES = ["UTC", "Asia/Tokyo", "America/New_York", "Europe/London"]

def get_version() -> str:
    """
    Returns the current version of the application.
    
    Returns:
        str: The version string
    """
    return __version__

def get_config() -> Dict[str, Any]:
    """
    Returns the default configuration dictionary.
    
    Returns:
        Dict[str, Any]: The default configuration dictionary
    """
    return DEFAULT_CONFIG.copy()

# Initialize any required core components
def initialize_core():
    """
    Initializes core components required for the application.
    This function should be called during application startup.
    """
    pass  # Implementation to be added as needed