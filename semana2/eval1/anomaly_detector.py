from dataclasses import dataclass

from semana2.eval1.anomaly_thresholds import AnomalyThresholds
from semana2.eval1.readings import SensorReading


@dataclass(frozen=True)
class Anomaly:
    """Representa una variable que superó su umbral."""

    variable: str
    value: float
    threshold: float


@dataclass(frozen=True)
class AnalysisResult:
    """Contiene las anomalías detectadas en una lectura."""

    anomalies: tuple[Anomaly, ...]


class AnomalyDetector:
    """Detecta condiciones ambientales anómalas."""

    def __init__(self, thresholds: AnomalyThresholds) -> None:
        self._thresholds = thresholds

    def analyze(self, reading: SensorReading) -> AnalysisResult:
        anomalies: list[Anomaly] = []

        if reading.temperature > self._thresholds.temperature:
            anomalies.append(
                Anomaly(
                    variable="temperature",
                    value=reading.temperature,
                    threshold=self._thresholds.temperature,
                )
            )

        if reading.humidity > self._thresholds.humidity:
            anomalies.append(
                Anomaly(
                    variable="humidity",
                    value=reading.humidity,
                    threshold=self._thresholds.humidity,
                )
            )

        return AnalysisResult(anomalies=tuple(anomalies))