from enum import StrEnum


class AlertStatus(StrEnum):
    """Estados permitidos durante el ciclo de vida de una alerta."""

    OPEN = "open"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"
