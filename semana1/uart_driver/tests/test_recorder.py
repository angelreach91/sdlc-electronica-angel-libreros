import json
from pathlib import Path

import pytest

from semana1.uart_driver.recorder import DataRecorder


def test_recorder_writes_one_json_line(tmp_path: Path) -> None:
    """Debe escribir un registro como una línea JSON válida."""
    path = tmp_path / "messages.jsonl"
    recorder = DataRecorder(path)
    data: dict[str, object] = {
        "sensor": "temperature",
        "value": 23.5,
    }

    recorder.record(data)

    assert recorder.path == path
    assert path.is_file()

    content = path.read_text(encoding="utf-8")
    assert content.endswith("\n")
    assert content.count("\n") == 1

    lines = content.splitlines()
    assert len(lines) == 1
    assert json.loads(lines[0]) == data


def test_recorder_appends_multiple_json_lines(tmp_path: Path) -> None:
    """Debe agregar nuevos registros sin reemplazar los anteriores."""
    path = tmp_path / "messages.jsonl"
    recorder = DataRecorder(path)
    first: dict[str, object] = {
        "sequence": 1,
        "value": "first",
    }
    second: dict[str, object] = {
        "sequence": 2,
        "value": "second",
    }

    recorder.record(first)
    recorder.record(second)

    lines = path.read_text(encoding="utf-8").splitlines()

    assert len(lines) == 2
    assert [json.loads(line) for line in lines] == [first, second]


def test_recorder_preserves_unicode_data(tmp_path: Path) -> None:
    """Debe conservar caracteres Unicode legibles en el archivo."""
    path = tmp_path / "unicode.jsonl"
    recorder = DataRecorder(path)
    data: dict[str, object] = {
        "country": "México",
        "measurement": "temperatura °C",
    }

    recorder.record(data)

    content = path.read_text(encoding="utf-8")

    assert "México" in content
    assert "temperatura °C" in content
    assert "\\u" not in content
    assert json.loads(content) == data


def test_recorder_rejects_non_serializable_data(tmp_path: Path) -> None:
    """Debe rechazar datos no serializables sin corromper el archivo."""
    path = tmp_path / "messages.jsonl"
    recorder = DataRecorder(path)

    valid_data: dict[str, object] = {"status": "valid"}
    invalid_data: dict[str, object] = {"invalid": object()}

    recorder.record(valid_data)
    original_content = path.read_text(encoding="utf-8")

    with pytest.raises(TypeError, match=r"(?i)serial"):
        recorder.record(invalid_data)

    assert path.read_text(encoding="utf-8") == original_content