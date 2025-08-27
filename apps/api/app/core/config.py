"""API configuration."""

from pyshared.config import settings as shared_settings


class APISettings(shared_settings):
    """API-specific settings."""

    # API-specific overrides can be added here
    pass


settings = APISettings()