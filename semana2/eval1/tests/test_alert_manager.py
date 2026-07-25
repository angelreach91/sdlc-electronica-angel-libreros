import inspect
import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from semana2.eval1.alert_manager import (
    AlertManager,
    AlertStrategy,
    ConsoleAlertStrategy,
    FileAlertStrategy,
)
from semana2.eval1.anomaly_alerts import AnomalyAlert
from semana2.eval1.anomaly_detector import Anomaly

READING_TIME = datetime(2026, 7, 24, 18, 30, tzinfo=timezone.utc)


def make_alert(sensor_id: str = "sensor-1") -> AnomalyAlert:
    return AnomalyAlert(
        sensor_id=sensor_id,
        received_at=READING_TIME,
        anomalies=(
            Anomaly(
                variable="temperature",
                value=36.0,
                threshold=35.0,
            ),
            Anomaly(
                variable="humidity",
                value=81.0,
                threshold=80.0,
            ),
        ),
    )


def expected_record(sensor_id: str = "sensor-1") -> dict[str, object]:
    return {
        "sensor_id": sensor_id,
        "received_at": READING_TIME.isoformat(),
        "anomalies": [
            {
                "variable": "temperature",
                "value": 36.0,
                "threshold": 35.0,
            },
            {
                "variable": "humidity",
                "value": 81.0,
                "threshold": 80.0,
            },
        ],
    }


def test_alert_strategy_is_abstract() -> None:
    assert inspect.isabstract(AlertStrategy)


def test_console_strategy_displays_alert_as_json(
    capsys: pytest.CaptureFixture[str],
) -> None:
    strategy = ConsoleAlertStrategy()

    strategy.publish(make_alert())

    captured = capsys.readouterr()
    assert json.loads(captured.out) == expected_record()


def test_file_strategy_creates_jsonl_file(
    tmp_path: Path,
) -> None:
    alerts_file = tmp_path / "alerts.jsonl"
    strategy = FileAlertStrategy(alerts_file)

    strategy.publish(make_alert())

    stored_record = json.loads(alerts_file.read_text(encoding="utf-8"))
    assert stored_record == expected_record()


def test_file_strategy_appends_without_overwriting(
    tmp_path: Path,
) -> None:
    alerts_file = tmp_path / "alerts.jsonl"
    strategy = FileAlertStrategy(alerts_file)

    strategy.publish(make_alert("sensor-1"))
    strategy.publish(make_alert("sensor-2"))

    stored_records = [
        json.loads(line)
        for line in alerts_file.read_text(encoding="utf-8").splitlines()
    ]

    assert stored_records == [
        expected_record("sensor-1"),
        expected_record("sensor-2"),
    ]


def test_alert_manager_uses_console_and_file_strategies(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    alerts_file = tmp_path / "alerts.jsonl"
    manager = AlertManager(
        strategies=(
            ConsoleAlertStrategy(),
            FileAlertStrategy(alerts_file),
        )
    )

    manager.publish(make_alert())

    captured = capsys.readouterr()
    stored_record = json.loads(alerts_file.read_text(encoding="utf-8"))

    assert json.loads(captured.out) == expected_record()
    assert stored_record == expected_record()


def test_alert_manager_continues_when_file_strategy_fails(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    manager = AlertManager(
        strategies=(
            FileAlertStrategy(tmp_path),
            ConsoleAlertStrategy(),
        )
    )

    manager.publish(make_alert())

    captured = capsys.readouterr()

    assert json.loads(captured.out) == expected_record()
    assert "Error al guardar la alerta" in captured.err