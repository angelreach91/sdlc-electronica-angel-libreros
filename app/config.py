import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AppConfig:
    """Configuración no sensible de la aplicación."""

    app_name: str
    app_version: str
    log_level: str


def get_app_config() -> AppConfig:
    """Lee la configuración actual desde variables de entorno."""

    return AppConfig(
        app_name=os.getenv("APP_NAME", "SensorHub"),
        app_version=os.getenv("APP_VERSION", "0.6.0"),
        log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
    )
