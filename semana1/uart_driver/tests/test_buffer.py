from threading import Barrier, Thread

import pytest

from semana1.uart_driver.buffer import ThreadSafeCircularBuffer


@pytest.mark.parametrize("capacity", [0, -1])
def test_buffer_rejects_non_positive_capacity(capacity: int) -> None:
    """Debe rechazar capacidades iguales o menores que cero."""
    with pytest.raises(ValueError, match=r"(?i)capacidad"):
        ThreadSafeCircularBuffer[int](capacity)


def test_buffer_preserves_items_until_reaching_capacity() -> None:
    """Debe conservar los elementos en su orden de inserción."""
    buffer: ThreadSafeCircularBuffer[int] = ThreadSafeCircularBuffer(3)

    buffer.append(1)
    buffer.append(2)

    assert buffer.capacity == 3
    assert len(buffer) == 2
    assert buffer.snapshot() == (1, 2)


def test_buffer_discards_oldest_item_when_full() -> None:
    """Debe reemplazar el elemento más antiguo al superar la capacidad."""
    buffer: ThreadSafeCircularBuffer[int] = ThreadSafeCircularBuffer(3)

    buffer.append(1)
    buffer.append(2)
    buffer.append(3)
    buffer.append(4)

    assert len(buffer) == 3
    assert buffer.snapshot() == (2, 3, 4)


def test_buffer_snapshot_is_independent() -> None:
    """La copia obtenida no debe cambiar cuando se modifica el buffer."""
    buffer: ThreadSafeCircularBuffer[int] = ThreadSafeCircularBuffer(3)
    buffer.append(1)
    buffer.append(2)

    snapshot: tuple[int, ...] = buffer.snapshot()
    buffer.append(3)

    assert snapshot == (1, 2)
    assert buffer.snapshot() == (1, 2, 3)


def test_buffer_supports_concurrent_appends() -> None:
    """Debe admitir escrituras concurrentes sin perder elementos."""
    buffer: ThreadSafeCircularBuffer[int] = ThreadSafeCircularBuffer(1000)
    barrier: Barrier = Barrier(4)

    def worker(start: int, stop: int) -> None:
        barrier.wait()
        for value in range(start, stop):
            buffer.append(value)

    threads: list[Thread] = [
        Thread(target=worker, args=(start, start + 250))
        for start in range(0, 1000, 250)
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join(timeout=5.0)

    assert all(not thread.is_alive() for thread in threads)
    assert len(buffer) == 1000
    assert set(buffer.snapshot()) == set(range(1000))