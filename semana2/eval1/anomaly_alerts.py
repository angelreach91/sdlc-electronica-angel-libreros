from dataclasses import dataclass
from datetime import datetime

from semana2.eval1.anomaly_detector import AnalysisResult, Anomaly
from semana2.eval1.readings import SensorReading
#imporaciones 

@dataclass(frozen=True)
class AnomalyAlert:
    """Representa una alerta generada para una lectura anómala."""

    sensor_id: str
    received_at: datetime
    anomalies: tuple[Anomaly, ...]


class AlertGenerator:
    """Genera una alerta cuando una lectura contiene anomalías."""

    @staticmethod
    def create(
        reading: SensorReading,
        analysis: AnalysisResult,
    ) -> AnomalyAlert | None:
        if not analysis.anomalies:
            return None

        return AnomalyAlert(
            sensor_id=reading.sensor_id,
            received_at=reading.received_at,
            anomalies=analysis.anomalies,
        )
