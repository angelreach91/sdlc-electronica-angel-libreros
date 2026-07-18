import json

import pytest

from semana1.uart_driver.parsers import CANParser


def test_can_recognizes_valid_simplified_frame() -> None:
    """Debe reconocer una trama CAN simplificada bien formada."""
    parser: CANParser = CANParser()
    frame = bytes.fromhex("43 41 4E 01 23 03 AA BB CC")

    assert parser.can_parse(frame) is True


def test_can_parses_valid_simplified_frame() -> None:
    """Debe convertir una trama CAN válida en datos estructurados."""
    parser: CANParser = CANParser()
    frame = bytes.fromhex("43 41 4E 01 23 03 AA BB CC")
    expected: dict[str, object] = {
        "type": "CAN",
        "identifier": 0x123,
        "dlc": 3,
        "data": "aabbcc",
    }

    result: dict[str, object] = parser.parse(frame)

    assert result == expected
    assert json.loads(json.dumps(result)) == expected


def test_can_rejects_identifier_out_of_range() -> None:
    """Debe rechazar identificadores superiores a 11 bits."""
    parser: CANParser = CANParser()
    frame = bytes.fromhex("43 41 4E 08 00 00")

    with pytest.raises(ValueError, match=r"(?i)identific"):
        parser.parse(frame)


def test_can_rejects_dlc_greater_than_eight() -> None:
    """Debe rechazar un DLC superior a ocho bytes."""
    parser: CANParser = CANParser()
    frame = bytes.fromhex(
        "43 41 4E 01 23 09 00 01 02 03 04 05 06 07 08"
    )

    with pytest.raises(ValueError, match=r"(?i)DLC"):
        parser.parse(frame)


def test_can_rejects_payload_length_mismatch() -> None:
    """Debe rechazar una trama cuyo DLC no coincida con los datos."""
    parser: CANParser = CANParser()
    frame = bytes.fromhex("43 41 4E 01 23 03 AA BB")

    with pytest.raises(
        ValueError,
        match=r"(?i)(longitud|cantidad de datos|carga útil)",
    ):
        parser.parse(frame)
