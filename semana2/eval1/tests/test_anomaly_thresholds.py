from typing import cast

import pytest

from semana2.eval1.anomaly_thresholds import (
    AnomalyThresholds,
    InvalidThresholdError,
)


def test_uses_default_thresholds() -> None:
    thresholds = AnomalyThresholds()

    assert thresholds.temperature == 35.0
    assert thresholds.humidity == 80.0


def test_updates_thresholds_with_valid_values() -> None:
    thresholds = AnomalyThresholds()

    thresholds.update(temperature=30.0, humidity=70.0)

    assert thresholds.temperature == 30.0
    assert thresholds.humidity == 70.0


@pytest.mark.parametrize(
    ("temperature", "humidity"),
    [
        (cast(float, "high"), 70.0),
        (30.0, cast(float, "high")),
        (30.0, -1.0),
        (30.0, 101.0),
    ],
)
def test_rejects_invalid_thresholds_and_keeps_previous_values(
    temperature: float,
    humidity: float,
) -> None:
    thresholds = AnomalyThresholds()
    thresholds.update(temperature=30.0, humidity=70.0)

    with pytest.raises(InvalidThresholdError):
        thresholds.update(
            temperature=temperature,
            humidity=humidity,
        )

    assert thresholds.temperature == 30.0
    assert thresholds.humidity == 70.0


@pytest.mark.parametrize("humidity", [0.0, 100.0])
def test_accepts_humidity_limits(humidity: float) -> None:
    thresholds = AnomalyThresholds()

    thresholds.update(temperature=30.0, humidity=humidity)

    assert thresholds.humidity == humidity