import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from semana2.eval1.alert_publisher import AlertPublisher
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


def test_displays_alert_as_json_in_console(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    publisher = AlertPublisher(tmp_path / "alerts.jsonl")

    publisher.publish(make_alert())

    captured = capsys.readouterr()
    assert json.loads(captured.out) == expected_record()


def test_creates_jsonl_file_with_equivalent_alert(
    tmp_path: Path,
) -> None:
    alerts_file = tmp_path / "alerts.jsonl"
    publisher = AlertPublisher(alerts_file)

    publisher.publish(make_alert())

    stored_record = json.loads(alerts_file.read_text(encoding="utf-8"))
    assert stored_record == expected_record()


def test_appends_alerts_without_overwriting_previous_records(
    tmp_path: Path,
) -> None:
    alerts_file = tmp_path / "alerts.jsonl"
    publisher = AlertPublisher(alerts_file)

    publisher.publish(make_alert("sensor-1"))
    publisher.publish(make_alert("sensor-2"))

    records = [
        json.loads(line)
        for line in alerts_file.read_text(encoding="utf-8").splitlines()
    ]

    assert records == [
        expected_record("sensor-1"),
        expected_record("sensor-2"),
    ]


def test_displays_alert_and_reports_storage_error(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    publisher = AlertPublisher(tmp_path)

    publisher.publish(make_alert())

    captured = capsys.readouterr()

    assert json.loads(captured.out) == expected_record()
    assert "Error al guardar la alerta" in captured.err