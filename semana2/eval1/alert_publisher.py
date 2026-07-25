import json
import sys
from pathlib import Path

from semana2.eval1.anomaly_alerts import AnomalyAlert


class AlertPublisher:
    """Muestra una alerta en consola y la almacena en JSON Lines."""

    def __init__(self, alerts_file: Path) -> None:
        self._alerts_file = alerts_file

    def publish(self, alert: AnomalyAlert) -> None:
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

        serialized_alert = json.dumps(record, ensure_ascii=False)
        print(serialized_alert)

        try:
            with self._alerts_file.open(
                mode="a",
                encoding="utf-8",
            ) as alerts_stream:
                alerts_stream.write(f"{serialized_alert}\n")
        except OSError as error:
            print(
                f"Error al guardar la alerta: {error}",
                file=sys.stderr,
            )