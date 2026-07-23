class SensorNotFoundError(LookupError):
    """Indica que el sensor solicitado no está registrado."""


class SensorRegistry:
    """Administra los sensores registrados."""

    def __init__(self) -> None:
        self._sensors: set[str] = set()

    def register(self, sensor_id: str) -> None:
        if not sensor_id:
            raise ValueError("El identificador no puede estar vacío.")

        if sensor_id in self._sensors:
            raise ValueError(f"El sensor '{sensor_id}' ya está registrado.")

        self._sensors.add(sensor_id)

    def get(self, sensor_id: str) -> str:
        if sensor_id not in self._sensors:
            raise SensorNotFoundError(sensor_id)

        return sensor_id