from abc import ABC, abstractmethod


ParsedMessage = dict[str, object]


def _calculate_modbus_crc(data: bytes) -> int:
    """Calcula el CRC-16 Modbus para una secuencia de bytes."""
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x0001:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
    return crc


def _calculate_nmea_checksum(content: str) -> int:
    """Calcula mediante XOR el checksum del contenido de una sentencia NMEA."""
    checksum = 0
    for character in content:
        checksum ^= ord(character)
    return checksum


def _nmea_coordinate_to_decimal(value: str, hemisphere: str) -> float:
    """Convierte una coordenada NMEA a grados decimales con signo."""
    if hemisphere in {"N", "S"}:
        degree_digits = 2
        maximum_degrees = 90
    elif hemisphere in {"E", "W"}:
        degree_digits = 3
        maximum_degrees = 180
    else:
        raise ValueError(f"Hemisferio NMEA inválido: {hemisphere!r}.")

    if len(value) <= degree_digits:
        raise ValueError(f"Coordenada NMEA incompleta: {value!r}.")

    try:
        degrees = int(value[:degree_digits])
        minutes = float(value[degree_digits:])
    except ValueError as error:
        raise ValueError(f"Coordenada NMEA inválida: {value!r}.") from error

    if not 0 <= minutes < 60:
        raise ValueError(
            f"Minutos fuera de rango en coordenada NMEA: {value!r}."
        )

    if degrees > maximum_degrees or (
        degrees == maximum_degrees and minutes != 0
    ):
        raise ValueError(
            f"Grados fuera de rango en coordenada NMEA: {value!r}."
        )

    decimal_degrees = degrees + minutes / 60
    if hemisphere in {"S", "W"}:
        decimal_degrees = -decimal_degrees

    return decimal_degrees


class MessageParser(ABC):
    """Contrato común para los parsers de mensajes UART."""

    @abstractmethod
    def can_parse(self, frame: bytes) -> bool:
        """Indica si la trama parece pertenecer al protocolo."""

    @abstractmethod
    def parse(self, frame: bytes) -> ParsedMessage:
        """Valida la trama y devuelve sus datos estructurados."""


class ModbusParser(MessageParser):
    """Parser de tramas binarias Modbus RTU."""

    def can_parse(self, frame: bytes) -> bool:
        """Reconoce una posible trama Modbus RTU."""
        return (
            len(frame) >= 4
            and 1 <= frame[0] <= 247
            and not frame.startswith(b"$GPGGA,")
        )

    def parse(self, frame: bytes) -> ParsedMessage:
        """Valida el CRC e interpreta una trama Modbus RTU."""
        if len(frame) < 4:
            raise ValueError(
                "La trama Modbus RTU debe contener al menos cuatro bytes."
            )

        address = frame[0]
        if not 1 <= address <= 247:
            raise ValueError(f"Dirección Modbus fuera de rango: {address}.")

        if frame.startswith(b"$GPGGA,"):
            raise ValueError(
                "La trama recibida no corresponde a Modbus RTU."
            )

        received_crc = int.from_bytes(frame[-2:], byteorder="little")
        calculated_crc = _calculate_modbus_crc(frame[:-2])

        if received_crc != calculated_crc:
            raise ValueError(
                "CRC Modbus inválido: "
                f"se recibió 0x{received_crc:04x} "
                f"y se calculó 0x{calculated_crc:04x}."
            )

        return {
            "address": address,
            "function": frame[1],
            "data": frame[2:-2].hex(),
        }


class NMEAParser(MessageParser):
    """Parser de sentencias NMEA del tipo GPGGA."""

    def can_parse(self, frame: bytes) -> bool:
        """Reconoce una posible sentencia NMEA GPGGA."""
        return frame.startswith(b"$GPGGA,")

    def parse(self, frame: bytes) -> ParsedMessage:
        """Valida el checksum e interpreta una sentencia GPGGA."""
        normalized_frame = frame.removesuffix(b"\r\n").rstrip(b" ")

        try:
            sentence = normalized_frame.decode("ascii")
        except UnicodeDecodeError as error:
            raise ValueError(
                "La sentencia NMEA debe estar codificada en ASCII."
            ) from error

        if not sentence.startswith("$GPGGA,"):
            raise ValueError("La sentencia NMEA no es del tipo GPGGA.")

        content_with_prefix, separator, received_checksum_text = (
            sentence.partition("*")
        )

        if not separator:
            raise ValueError(
                "Falta el checksum en la sentencia NMEA GPGGA."
            )

        if len(received_checksum_text) != 2 or any(
            character not in "0123456789abcdefABCDEF"
            for character in received_checksum_text
        ):
            raise ValueError(
                "El checksum NMEA tiene un formato hexadecimal inválido."
            )

        content = content_with_prefix[1:]
        received_checksum = int(received_checksum_text, 16)
        calculated_checksum = _calculate_nmea_checksum(content)

        if received_checksum != calculated_checksum:
            raise ValueError(
                "Checksum NMEA inválido: "
                f"se recibió 0x{received_checksum:02x} "
                f"y se calculó 0x{calculated_checksum:02x}."
            )

        fields = content.split(",")

        if len(fields) < 10:
            raise ValueError(
                "La sentencia GPGGA no contiene los campos necesarios."
            )

        required_fields = fields[1:8] + [fields[9]]
        if any(field == "" for field in required_fields):
            raise ValueError(
                "La sentencia GPGGA contiene campos necesarios vacíos."
            )

        latitude = _nmea_coordinate_to_decimal(fields[2], fields[3])
        longitude = _nmea_coordinate_to_decimal(fields[4], fields[5])

        try:
            fix_quality = int(fields[6])
            satellites = int(fields[7])
            altitude_m = float(fields[9])
        except ValueError as error:
            raise ValueError(
                "La sentencia GPGGA contiene valores numéricos inválidos."
            ) from error

        return {
            "type": "GPGGA",
            "utc_time": fields[1],
            "latitude": latitude,
            "longitude": longitude,
            "fix_quality": fix_quality,
            "satellites": satellites,
            "altitude_m": altitude_m,
        }


class CANParser(MessageParser):
    """Parser para un formato CAN simplificado con fines educativos."""

    def can_parse(self, frame: bytes) -> bool:
        """Reconoce una posible trama del formato CAN simplificado."""
        return len(frame) >= 6 and frame.startswith(b"CAN")

    def parse(self, frame: bytes) -> ParsedMessage:
        """Valida e interpreta una trama del formato CAN simplificado."""
        if len(frame) < 6:
            raise ValueError(
                "La trama CAN simplificada está incompleta: "
                "debe contener al menos seis bytes."
            )

        if not frame.startswith(b"CAN"):
            raise ValueError(
                "La trama no corresponde al formato CAN simplificado."
            )

        identifier = int.from_bytes(frame[3:5], byteorder="big")
        if identifier > 0x7FF:
            raise ValueError(
                f"Identificador CAN fuera de rango: 0x{identifier:04x}."
            )

        dlc = frame[5]
        if dlc > 8:
            raise ValueError(f"DLC CAN fuera de rango: {dlc}.")

        payload = frame[6:]
        if len(payload) != dlc:
            raise ValueError(
                "La longitud de la carga útil CAN no coincide con el DLC: "
                f"se esperaban {dlc} bytes y se recibieron {len(payload)}."
            )

        return {
            "type": "CAN",
            "identifier": identifier,
            "dlc": dlc,
            "data": payload.hex(),
        }
