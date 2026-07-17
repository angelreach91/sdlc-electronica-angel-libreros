from pathlib import Path

import pytest

from solid_srp_ocp_lsp import (
    AnomalyDetector,
    BadAnomalyDetector,
    BadSensorManager,
    BadUnavailableSensor,
    ConsoleAlert,
    DataLogger,
    FileAlert,
    HumiditySensor,
    SensorReader,
    SensorReading,
    TemperatureSensor,
    process_sensor,
)


def test_s_bad_example_mixes_reading_and_storage() -> None:
    sensor = BadSensorManager("temp-1", [24.5])

    reading = sensor.read()

    assert reading == SensorReading("temp-1", 24.5)
    assert sensor.saved_readings == [reading]


def test_s_good_example_separates_reader_and_logger() -> None:
    reader = SensorReader("temp-1", [24.5])
    logger = DataLogger()

    reading = reader.read()
    logger.log(reading)

    assert reading == SensorReading("temp-1", 24.5)
    assert logger.saved_readings == [reading]


def test_o_bad_example_uses_conditionals_for_alerts(tmp_path: Path) -> None:
    alert_file = tmp_path / "alerts.txt"
    detector = BadAnomalyDetector(30.0, "file", alert_file)

    triggered = detector.check(SensorReading("temp-1", 35.0))

    assert triggered is True
    assert alert_file.read_text(encoding="utf-8") == "Anomalía en temp-1\n"


def test_o_good_example_uses_alert_strategy(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    console = ConsoleAlert()
    console_detector = AnomalyDetector(30.0, console)
    file_path = tmp_path / "alerts.txt"
    file_detector = AnomalyDetector(70.0, FileAlert(file_path))

    console_detector.check(SensorReading("temp-1", 35.0))
    file_detector.check(SensorReading("humidity-1", 75.0))

    assert capsys.readouterr().out == "Anomalía en temp-1\n"
    assert file_path.read_text(encoding="utf-8") == "Anomalía en humidity-1\n"


def test_l_bad_example_breaks_base_sensor_contract() -> None:
    with pytest.raises(RuntimeError):
        process_sensor(BadUnavailableSensor())


def test_l_good_example_accepts_temperature_and_humidity_sensors() -> None:
    temperature = TemperatureSensor("temp-1", 24.5)
    humidity = HumiditySensor("humidity-1", 55.0)

    assert process_sensor(temperature) == SensorReading("temp-1", 24.5)
    assert process_sensor(humidity) == SensorReading("humidity-1", 55.0)
