import json

import pytest

from semana1.uart_driver.parsers import ModbusParser, NMEAParser


def test_modbus_recognizes_valid_rtu_frame() -> None:
    """Debe reconocer una trama Modbus RTU completa."""
    parser: ModbusParser = ModbusParser()
    frame: bytes = bytes.fromhex("01 03 00 00 00 0A C5 CD")

    assert parser.can_parse(frame) is True


def test_modbus_parses_valid_rtu_frame() -> None:
    """Debe convertir una trama Modbus RTU válida en datos estructurados."""
    parser: ModbusParser = ModbusParser()
    frame: bytes = bytes.fromhex("01 03 00 00 00 0A C5 CD")

    result: dict[str, object] = parser.parse(frame)

    assert result == {
        "address": 1,
        "function": 3,
        "data": "0000000a",
    }
    json.dumps(result)


def test_modbus_rejects_frame_with_invalid_crc() -> None:
    """Debe rechazar una trama Modbus RTU cuyo CRC sea incorrecto."""
    parser: ModbusParser = ModbusParser()
    valid_frame: bytes = bytes.fromhex("01 03 00 00 00 0A C5 CD")
    invalid_frame: bytes = valid_frame[:-2] + bytes(
        [valid_frame[-2] ^ 0x01, valid_frame[-1]]
    )

    with pytest.raises(ValueError, match=r"(?i)crc"):
        parser.parse(invalid_frame)


def test_nmea_recognizes_gpgga_sentence() -> None:
    """Debe reconocer una sentencia NMEA del tipo GPGGA."""
    parser: NMEAParser = NMEAParser()
    sentence: bytes = (
        b"$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,"
        b"545.4,M,46.9,M,,*47\r\n"
    )

    assert parser.can_parse(sentence) is True


def test_nmea_parses_valid_gpgga_sentence() -> None:
    """Debe convertir una sentencia GPGGA válida en datos estructurados."""
    parser: NMEAParser = NMEAParser()
    sentence: bytes = (
        b"$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,"
        b"545.4,M,46.9,M,,*47\r\n"
    )

    result: dict[str, object] = parser.parse(sentence)

    assert result["type"] == "GPGGA"
    assert result["utc_time"] == "123519"
    assert result["latitude"] == pytest.approx(48.1173)
    assert result["longitude"] == pytest.approx(11.516666666666667)
    assert result["fix_quality"] == 1
    assert result["satellites"] == 8
    assert result["altitude_m"] == pytest.approx(545.4)
    json.dumps(result)


def test_nmea_rejects_sentence_with_invalid_checksum() -> None:
    """Debe rechazar una sentencia GPGGA cuyo checksum sea incorrecto."""
    parser: NMEAParser = NMEAParser()
    invalid_sentence: bytes = (
        b"$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,"
        b"545.4,M,46.9,M,,*46\r\n"
    )

    with pytest.raises(ValueError, match=r"(?i)checksum"):
        parser.parse(invalid_sentence)


def test_modbus_recognizes_address_36_as_rtu_frame() -> None:
    """Debe distinguir la dirección Modbus 36 del prefijo NMEA."""
    parser = ModbusParser()
    frame = bytes.fromhex("24 03 00 00 00 0A C2 F8")

    assert parser.can_parse(frame) is True
    assert parser.parse(frame)["address"] == 36