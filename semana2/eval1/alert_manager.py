import json
import sys
from abc import ABC, abstractmethod
from pathlib import Path

from semana2.eval1.anomaly_alerts import AnomalyAlert


def _serialize_alert(alert: AnomalyAlert) -> str:
    record: dict[str, object] = {
        "sensor_id": alert.sensor_id,
        "received_at": alert.received_at.isoformat(),
        "anomalies": [
            {
                "variable": anomaly.variable,
                "value": anomaly.value,
                "threshold": anomaly.threshold,
            }
            for anomaly in alert.anomalies
        ],
    }

    return json.dumps(record, ensure_ascii=False)


class AlertStrategy(ABC):
    """Define el contrato común para publicar alertas."""

    @abstractmethod
    def publish(self, alert: AnomalyAlert) -> None:
        """Publica una alerta mediante una salida específica."""


class ConsoleAlertStrategy(AlertStrategy):
    """Publica alertas en la consola."""

    def publish(self, alert: AnomalyAlert) -> None:
        print(_serialize_alert(alert))


class FileAlertStrategy(AlertStrategy):
    """Almacena alertas en un archivo JSON Lines."""

    def __init__(self, alerts_file: Path) -> None:
        self._alerts_file = alerts_file

    def publish(self, alert: AnomalyAlert) -> None:
        serialized_alert = _serialize_alert(alert)

        with self._alerts_file.open(
            mode="a",
            encoding="utf-8",
        ) as alerts_stream:
            alerts_stream.write(f"{serialized_alert}\n")


class AlertManager:
    """Coordina la publicación mediante las estrategias configuradas."""

    def __init__(
        self,
        strategies: tuple[AlertStrategy, ...],
    ) -> None:
        self._strategies = strategies

    def publish(self, alert: AnomalyAlert) -> None:
        for strategy in self._strategies:
            try:
                strategy.publish(alert)
            except OSError as error:
                print(
                    f"Error al guardar la alerta: {error}",
                    file=sys.stderr,
                )