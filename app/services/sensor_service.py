from app.models.sensor import Sensor
from app.repositories.sensor_repository import SensorRepository
from app.sensor_types import (
    EXPECTED_UNIT_BY_TYPE,
    SensorType,
    SensorUnit,
)


class SensorService:
    """Gestiona las reglas de negocio relacionadas con sensores."""

    def __init__(self, repository: SensorRepository) -> None:
        self._repository = repository

    def create_sensor(
        self,
        sensor_id: str,
        name: str,
        sensor_type: SensorType,
        unit: SensorUnit,
    ) -> Sensor:
        """Valida y registra un nuevo sensor."""

        normalized_sensor_id = self._normalize_sensor_id(sensor_id)
        normalized_name = self._normalize_name(name)

        if self._repository.get_by_id(normalized_sensor_id) is not None:
            raise ValueError(
                f"ya existe un sensor con id {normalized_sensor_id}"
            )

        self._validate_type_and_unit(sensor_type, unit)

        sensor = Sensor(
            id=normalized_sensor_id,
            name=normalized_name,
            sensor_type=sensor_type.value,
            unit=unit.value,
            is_active=True,
        )

        return self._repository.add(sensor)

    def list_sensors(
        self,
        *,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Sensor]:
        """Consulta los sensores registrados."""

        self._validate_pagination(limit, offset)

        return self._repository.list_all(
            limit=limit,
            offset=offset,
        )

    def get_by_id(self, sensor_id: str) -> Sensor | None:
        """Busca un sensor mediante su identificador."""

        normalized_sensor_id = self._normalize_sensor_id(sensor_id)
        return self._repository.get_by_id(normalized_sensor_id)

    def update_sensor(
        self,
        sensor_id: str,
        *,
        name: str | None = None,
        sensor_type: SensorType | None = None,
        unit: SensorUnit | None = None,
        is_active: bool | None = None,
    ) -> Sensor | None:
        """Actualiza parcialmente un sensor existente."""

        normalized_sensor_id = self._normalize_sensor_id(sensor_id)

        if (
            name is None
            and sensor_type is None
            and unit is None
            and is_active is None
        ):
            raise ValueError(
                "debe proporcionar al menos un valor para actualizar"
            )

        sensor = self._repository.get_by_id(normalized_sensor_id)

        if sensor is None:
            return None

        final_sensor_type = (
            sensor_type
            if sensor_type is not None
            else SensorType(sensor.sensor_type)
        )
        final_unit = (
            unit
            if unit is not None
            else SensorUnit(sensor.unit)
        )

        self._validate_type_and_unit(
            final_sensor_type,
            final_unit,
        )

        if name is not None:
            sensor.name = self._normalize_name(name)

        if sensor_type is not None:
            sensor.sensor_type = sensor_type.value

        if unit is not None:
            sensor.unit = unit.value

        if is_active is not None:
            sensor.is_active = is_active

        return self._repository.update(sensor)

    def deactivate_sensor(self, sensor_id: str) -> bool:
        """Desactiva un sensor e indica si fue encontrado."""

        normalized_sensor_id = self._normalize_sensor_id(sensor_id)
        sensor = self._repository.get_by_id(normalized_sensor_id)

        if sensor is None:
            return False

        sensor.is_active = False
        self._repository.update(sensor)

        return True

    @staticmethod
    def _normalize_sensor_id(sensor_id: str) -> str:
        normalized_sensor_id = sensor_id.strip()

        if not normalized_sensor_id:
            raise ValueError("sensor_id no puede estar vacío")

        return normalized_sensor_id

    @staticmethod
    def _normalize_name(name: str) -> str:
        normalized_name = name.strip()

        if not normalized_name:
            raise ValueError("name no puede estar vacío")

        return normalized_name

    @staticmethod
    def _validate_type_and_unit(
        sensor_type: SensorType,
        unit: SensorUnit,
    ) -> None:
        expected_unit = EXPECTED_UNIT_BY_TYPE[sensor_type]

        if unit != expected_unit:
            raise ValueError(
                f"la unidad {unit.value} no corresponde "
                f"al tipo {sensor_type.value}"
            )

    @staticmethod
    def _validate_pagination(limit: int, offset: int) -> None:
        if not 1 <= limit <= 100:
            raise ValueError("limit debe estar entre 1 y 100")

        if offset < 0:
            raise ValueError("offset no puede ser negativo")