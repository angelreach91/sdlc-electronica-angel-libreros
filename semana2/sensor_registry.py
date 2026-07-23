class SensorNotFoundError(LookupError):
    """Indica que el sensor solicitado no está registrado."""


class SensorRegistry:
    """Administra los sensores registrados."""

    def get(self, sensor_id: str) -> object:
        raise SensorNotFoundError(sensor_id)