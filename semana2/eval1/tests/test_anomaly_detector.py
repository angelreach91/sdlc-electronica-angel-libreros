from datetime import datetime, timezone

import pytest

from semana2.eval1.anomaly_detector import AnomalyDetector
from semana2.eval1.anomaly_thresholds import AnomalyThresholds
from semana2.eval1.readings import SensorReading


def make_reading(
    temperature: float,
    humidity: float,
) -> SensorReading:
    return SensorReading(
        sensor_id="sensor-1",
        temperature=temperature,
        humidity=humidity,
        received_at=datetime.now(timezone.utc),
    )


@pytest.mark.parametrize(
    ("temperature", "humidity", "expected_variable"),
    [
        (36.0, 70.0, "temperature"),
        (30.0, 81.0, "humidity"),
    ],
)
def test_detects_only_the_variable_above_its_threshold(
    temperature: float,
    humidity: float,
    expected_variable: str,
) -> None:
    detector = AnomalyDetector(AnomalyThresholds())

    result = detector.analyze(make_reading(temperature, humidity))

    assert len(result.anomalies) == 1
    assert result.anomalies[0].variable == expected_variable


def test_detects_both_variables_above_their_thresholds() -> None:
    detector = AnomalyDetector(AnomalyThresholds())

    result = detector.analyze(make_reading(36.0, 81.0))

    assert {anomaly.variable for anomaly in result.anomalies} == {
        "temperature",
        "humidity",
    }


def test_preserves_values_and_thresholds_used() -> None:
    thresholds = AnomalyThresholds()
    thresholds.update(temperature=30.0, humidity=70.0)
    detector = AnomalyDetector(thresholds)

    result = detector.analyze(make_reading(31.0, 71.0))

    anomalies = {
        anomaly.variable: anomaly
        for anomaly in result.anomalies
    }

    assert anomalies["temperature"].value == 31.0
    assert anomalies["temperature"].threshold == 30.0
    assert anomalies["humidity"].value == 71.0
    assert anomalies["humidity"].threshold == 70.0


@pytest.mark.parametrize(
    ("temperature", "humidity"),
    [
        (35.0, 80.0),
        (34.0, 79.0),
    ],
)
def test_reports_no_anomalies_for_values_at_or_below_thresholds(
    temperature: float,
    humidity: float,
) -> None:
    detector = AnomalyDetector(AnomalyThresholds())

    result = detector.analyze(make_reading(temperature, humidity))

    assert result.anomalies == ()