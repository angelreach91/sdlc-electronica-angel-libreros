from pathlib import Path

from semana2.eval1.alert_manager import (
    AlertManager,
    ConsoleAlertStrategy,
    FileAlertStrategy,
)
from semana2.eval1.anomaly_alerts import AnomalyAlert


class AlertPublisher:
    """Publica alertas mediante las estrategias de consola y archivo."""

    def __init__(self, alerts_file: Path) -> None:
        self._manager = AlertManager(
            strategies=(
                ConsoleAlertStrategy(),
                FileAlertStrategy(alerts_file),
            )
        )

    def publish(self, alert: AnomalyAlert) -> None:
        self._manager.publish(alert)