class InvalidThresholdError(ValueError):
    """Indica que los umbrales proporcionados son inválidos."""


class AnomalyThresholds:
    """Mantiene los umbrales máximos de temperatura y humedad."""

    def __init__(self) -> None:
        self.temperature = 35.0
        self.humidity = 80.0

    def update(
        self,
        temperature: float,
        humidity: float,
    ) -> None:
        if isinstance(temperature, bool) or not isinstance(
            temperature,
            (int, float),
        ):
            raise InvalidThresholdError(
                "El umbral de temperatura debe ser numérico."
            )

        if isinstance(humidity, bool) or not isinstance(
            humidity,
            (int, float),
        ):
            raise InvalidThresholdError(
                "El umbral de humedad debe ser numérico."
            )

        if not 0.0 <= humidity <= 100.0:
            raise InvalidThresholdError(
                "El umbral de humedad debe estar entre 0 y 100."
            )

        self.temperature = float(temperature)
        self.humidity = float(humidity)