import json
from collections.abc import Mapping
from pathlib import Path


class DataRecorder:
    """Persiste mensajes procesados en formato JSON Lines."""

    def __init__(self, path: Path) -> None:
        self._path = path

    @property
    def path(self) -> Path:
        """Devuelve la ruta del archivo JSON Lines."""
        return self._path

    def record(self, data: Mapping[str, object]) -> None:
        """Agrega un mensaje serializable como una línea JSON."""
        try:
            serialized_data = json.dumps(data, ensure_ascii=False)
        except TypeError as error:
            raise TypeError(
                "Los datos no son serializables como JSON."
            ) from error

        with self._path.open("a", encoding="utf-8") as file:
            file.write(f"{serialized_data}\n")