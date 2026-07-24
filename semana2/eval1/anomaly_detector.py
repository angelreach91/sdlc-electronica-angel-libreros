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

    @staticmethod
    def _detect_anomaly(
        variable: str,
        value: float,
        threshold: float,
    ) -> Anomaly | None:
        if value <= threshold:
            return None

        return Anomaly(
            variable=variable,
            value=value,
            threshold=threshold,
        )

    def analyze(self, reading: SensorReading) -> AnalysisResult:
        anomalies: list[Anomaly] = []

        variables = (
            (
                "temperature",
                reading.temperature,
                self._thresholds.temperature,
            ),
            (
                "humidity",
                reading.humidity,
                self._thresholds.humidity,
            ),
        )

        for variable, value, threshold in variables:
            anomaly = self._detect_anomaly(
                variable=variable,
                value=value,
                threshold=threshold,
            )

            if anomaly is not None:
                anomalies.append(anomaly)

        return AnalysisResult(anomalies=tuple(anomalies))