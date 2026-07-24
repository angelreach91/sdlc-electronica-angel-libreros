class InvalidThresholdError(ValueError):
    """Indica que los umbrales proporcionados son inválidos."""


class AnomalyThresholds:
    """Mantiene los umbrales máximos de temperatura y humedad."""

    def __init__(self) -> None:
        self.temperature = 35.0
        self.humidity = 80.0

    @staticmethod
    def _require_numeric(
        value: object,
        threshold_name: str,
    ) -> int | float:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise InvalidThresholdError(
                f"El umbral de {threshold_name} debe ser numérico."
            )

        return value

    def update(
        self,
        temperature: float,
        humidity: float,
    ) -> None:
        numeric_temperature = self._require_numeric(
            temperature,
            "temperatura",
        )
        numeric_humidity = self._require_numeric(
            humidity,
            "humedad",
        )

        if not 0.0 <= numeric_humidity <= 100.0:
            raise InvalidThresholdError(
                "El umbral de humedad debe estar entre 0 y 100."
            )

        self.temperature = float(numeric_temperature)
        self.humidity = float(numeric_humidity)