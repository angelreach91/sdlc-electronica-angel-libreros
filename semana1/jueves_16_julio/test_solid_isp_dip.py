from semana1.jueves_16_julio.solid_isp_dip import (
    Calibratable,
    DataProcessor,
    InMemoryRepository,
    Readable,
    SensorReading,
    Writable,
)


class ReadOnlySensor:
    """Sensor que solamente produce lecturas."""

    def __init__(self, reading: SensorReading) -> None:
        self._reading = reading

    def read(self) -> SensorReading:
        return self._reading


class WriteOnlyOutput:
    """Salida que solamente recibe valores."""

    def __init__(self) -> None:
        self.values: list[float] = []

    def write(self, value: float) -> None:
        self.values.append(value)


class CalibrationOnlyDevice:
    """Dispositivo que solamente permite calibración y restablecimiento."""

    def __init__(self) -> None:
        self.is_calibrated = False

    def calibrate(self) -> None:
        self.is_calibrated = True

    def reset(self) -> None:
        self.is_calibrated = False


class RecordingRepository:
    """Repositorio alternativo para comprobar la inyección."""

    def __init__(self) -> None:
        self.saved_readings: list[SensorReading] = []
        self.requested_sensor_ids: list[str] = []

    def save(self, reading: SensorReading) -> None:
        self.saved_readings.append(reading)

    def get_latest(self, sensor_id: str) -> SensorReading | None:
        self.requested_sensor_ids.append(sensor_id)

        for reading in reversed(self.saved_readings):
            if reading.sensor_id == sensor_id:
                return reading

        return None


def test_readable_does_not_require_unrelated_operations() -> None:
    """Un consumidor de lectura solo debe exigir el método read."""
    expected = SensorReading(sensor_id="sensor-1", value=21.5)
    sensor = ReadOnlySensor(expected)
    readable: Readable = sensor

    assert readable.read() == expected
    assert not hasattr(sensor, "write")
    assert not hasattr(sensor, "calibrate")


def test_writable_does_not_require_reading_or_calibration() -> None:
    """Un consumidor de escritura solo debe exigir el método write."""
    output = WriteOnlyOutput()
    writable: Writable = output

    writable.write(3.3)

    assert output.values == [3.3]
    assert not hasattr(output, "read")
    assert not hasattr(output, "calibrate")


def test_calibratable_uses_only_calibration_operations() -> None:
    """La calibración debe depender únicamente de su interfaz específica."""
    device = CalibrationOnlyDevice()
    calibratable: Calibratable = device

    calibratable.calibrate()
    assert device.is_calibrated is True

    calibratable.reset()
    assert device.is_calibrated is False

    assert not hasattr(device, "read")
    assert not hasattr(device, "write")


def test_data_processor_uses_injected_in_memory_repository() -> None:
    """DataProcessor debe almacenar y consultar mediante la dependencia."""
    repository = InMemoryRepository()
    processor = DataProcessor(repository)
    reading = SensorReading(sensor_id="sensor-1", value=25.0)

    processor.process(reading)

    assert processor.get_latest("sensor-1") == reading
    assert processor.get_latest("sensor-inexistente") is None


def test_data_processor_accepts_alternative_repository() -> None:
    """DataProcessor debe aceptar cualquier repositorio compatible."""
    repository = RecordingRepository()
    processor = DataProcessor(repository)
    reading = SensorReading(sensor_id="sensor-2", value=18.75)

    processor.process(reading)
    result = processor.get_latest("sensor-2")

    assert repository.saved_readings == [reading]
    assert repository.requested_sensor_ids == ["sensor-2"]
    assert result == reading