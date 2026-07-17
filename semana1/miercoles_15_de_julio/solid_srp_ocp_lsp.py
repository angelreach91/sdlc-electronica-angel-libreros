from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SensorReading:
    """Lectura inmutable producida por un sensor."""

    # frozen=True evita modificar una lectura despues de crearla.
    sensor_id: str
    value: float


# ---------- S: Single Responsibility Principle ----------
# MAL: una clase mezcla lectura y almacenamiento.


class BadSensorManager:
    """Lee sensores y guarda datos en la misma clase."""

    def __init__(self, sensor_id: str, values: list[float]) -> None:
        self.sensor_id = sensor_id
        # Se copia la lista para no modificar la lista original recibida.
        self._values = values.copy()
        self.saved_readings: list[SensorReading] = []

    def read(self) -> SensorReading:
        reading = SensorReading(self.sensor_id, self._values.pop(0))
        # Este guardado automatico es el problema: leer tambien almacena.
        self.saved_readings.append(reading)
        return reading


# BIEN: leer y almacenar son responsabilidades separadas.


class SensorReader:
    """Lee datos simulados de un sensor."""

    def __init__(self, sensor_id: str, values: list[float]) -> None:
        self.sensor_id = sensor_id
        self._values = values.copy()

    def read(self) -> SensorReading:
        # Aqui leer solo devuelve el dato; no decide donde guardarlo.
        return SensorReading(self.sensor_id, self._values.pop(0))


class DataLogger:
    """Guarda lecturas de sensores."""

    def __init__(self) -> None:
        self.saved_readings: list[SensorReading] = []

    def log(self, reading: SensorReading) -> None:
        self.saved_readings.append(reading)


# ---------- O: Open/Closed Principle ----------
# MAL: los tipos de alerta se deciden con condicionales.


class BadAnomalyDetector:
    """Detecta anomalías y elige la alerta con condicionales."""

    def __init__(self, threshold: float, alert_type: str, file_path: Path | None = None) -> None:
        self.threshold = threshold
        self.alert_type = alert_type
        self.file_path = file_path

    def check(self, reading: SensorReading) -> bool:
        if reading.value <= self.threshold:
            return False

        message = f"Anomalía en {reading.sensor_id}"
        # Agregar otro tipo de alerta obligaria a editar esta cadena de if/elif.
        if self.alert_type == "console":
            print(message)
        elif self.alert_type == "file":
            if self.file_path is None:
                raise ValueError("file_path is required for file alerts")
            self.file_path.write_text(message + "\n", encoding="utf-8")
        else:
            raise ValueError(f"Unsupported alert type: {self.alert_type}")

        return True


# BIEN: las alertas se extienden con estrategias.


class AlertStrategy(ABC):
    """Contrato para enviar alertas."""

    @abstractmethod
    def send(self, message: str) -> None:
        """Envía un mensaje de alerta."""


class ConsoleAlert(AlertStrategy):
    """Alerta de consola capturable en pruebas."""

    def send(self, message: str) -> None:
        print(message)


class FileAlert(AlertStrategy):
    """Alerta que escribe mensajes en un archivo."""

    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path

    def send(self, message: str) -> None:
        # append mantiene alertas anteriores y evita simular el archivo con listas.
        with self.file_path.open("a", encoding="utf-8") as file:
            file.write(message + "\n")


class AnomalyDetector:
    """Detecta anomalías y delega el envío de alertas."""

    def __init__(self, threshold: float, alert: AlertStrategy) -> None:
        self.threshold = threshold
        self.alert = alert

    def check(self, reading: SensorReading) -> None:
        if reading.value <= self.threshold:
            return

        # El detector no sabe si la alerta va a consola, archivo u otro destino.
        self.alert.send(f"Anomalía en {reading.sensor_id}")


# ---------- L: Liskov Substitution Principle ----------
# MAL: una subclase rompe el contrato de BaseSensor.


class BaseSensor(ABC):
    """Contrato común: read() debe devolver una SensorReading válida."""

    @abstractmethod
    def read(self) -> SensorReading:
        """Devuelve una SensorReading válida."""


class BadUnavailableSensor(BaseSensor):
    """Rompe el contrato porque no entrega una lectura usable."""

    def read(self) -> SensorReading:
        # Aunque la firma coincide, esta subclase no puede procesarse igual.
        raise RuntimeError("sensor offline")


# BIEN: las subclases respetan el contrato de BaseSensor.


class TemperatureSensor(BaseSensor):
    """Sensor de temperatura procesable como BaseSensor."""

    def __init__(self, sensor_id: str, value: float) -> None:
        self.sensor_id = sensor_id
        self.value = value

    def read(self) -> SensorReading:
        return SensorReading(self.sensor_id, self.value)


class HumiditySensor(BaseSensor):
    """Sensor de humedad procesable como BaseSensor."""

    def __init__(self, sensor_id: str, value: float) -> None:
        self.sensor_id = sensor_id
        self.value = value

    def read(self) -> SensorReading:
        return SensorReading(self.sensor_id, self.value)


def process_sensor(sensor: BaseSensor) -> SensorReading:
    """Procesa cualquier sensor que respete BaseSensor."""

    return sensor.read()
