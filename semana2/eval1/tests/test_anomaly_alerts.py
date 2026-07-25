from datetime import datetime, timezone

import pytest

from semana2.eval1.anomaly_alerts import AlertGenerator
from semana2.eval1.anomaly_detector import Anomaly, AnalysisResult
from semana2.eval1.readings import SensorReading


READING_TIME = datetime(2026, 7, 24, 18, 30, tzinfo=timezone.utc)


def make_reading() -> SensorReading:
    return SensorReading(
        sensor_id="sensor-1",
        temperature=36.0,
        humidity=81.0,
        received_at=READING_TIME,
    )


@pytest.mark.parametrize(
    "anomaly",
    [
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
    ],
)
def test_creates_alert_with_the_detected_anomaly(
    anomaly: Anomaly,
) -> None:
    analysis = AnalysisResult(anomalies=(anomaly,))
    generator = AlertGenerator()

    alert = generator.create(make_reading(), analysis)

    assert alert is not None
    assert alert.anomalies == (anomaly,)


def test_preserves_sensor_id_and_reading_time() -> None:
    anomaly = Anomaly(
        variable="temperature",
        value=36.0,
        threshold=35.0,
    )
    analysis = AnalysisResult(anomalies=(anomaly,))
    generator = AlertGenerator()

    alert = generator.create(make_reading(), analysis)

    assert alert is not None
    assert alert.sensor_id == "sensor-1"
    assert alert.received_at == READING_TIME


def test_groups_both_anomalies_in_one_alert() -> None:
    anomalies = (
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
    )
    analysis = AnalysisResult(anomalies=anomalies)
    generator = AlertGenerator()

    alert = generator.create(make_reading(), analysis)

    assert alert is not None
    assert alert.anomalies == anomalies


def test_returns_none_when_there_are_no_anomalies() -> None:
    analysis = AnalysisResult(anomalies=())
    generator = AlertGenerator()

    alert = generator.create(make_reading(), analysis)

    assert alert is None