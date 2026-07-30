from collections import deque
from threading import Lock
from typing import Generic, TypeVar

T = TypeVar("T")


class ThreadSafeCircularBuffer(Generic[T]):
    """Buffer circular genérico protegido para acceso concurrente."""

    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError("La capacidad debe ser mayor que cero")

        self._capacity = capacity
        self._items: deque[T] = deque(maxlen=capacity)
        self._lock = Lock()

    @property
    def capacity(self) -> int:
        """Devuelve la capacidad máxima del buffer."""
        return self._capacity

    def append(self, item: T) -> None:
        """Agrega un elemento y descarta el más antiguo si está lleno."""
        with self._lock:
            self._items.append(item)

    def snapshot(self) -> tuple[T, ...]:
        """Devuelve una copia inmutable del contenido actual."""
        with self._lock:
            return tuple(self._items)

    def __len__(self) -> int:
        """Devuelve la cantidad actual de elementos."""
        with self._lock:
            return len(self._items)
