import os


class ConfigurationError(RuntimeError):
    """Raised when required runtime configuration is missing."""


def load_settings() -> dict[str, str]:
    value = os.getenv("INVENTORY_AGENT_ENV")
    if not value:
        raise ConfigurationError("INVENTORY_AGENT_ENV is required")
    return {"environment": value}
