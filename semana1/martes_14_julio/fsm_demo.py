from enum import Enum, auto


class TrafficLightState(Enum):
    RED = auto()
    YELLOW = auto()
    GREEN = auto()


class TrafficLightFSM:
    def __init__(self) -> None:
        self._state = TrafficLightState.RED
        self._cycle_count = 0

    @property
    def state(self) -> TrafficLightState:
        """Devuelve el estado actual del semáforo."""
        return self._state

    @property
    def cycle_count(self) -> int:
        """Devuelve el número de transiciones realizadas."""
        return self._cycle_count

    def transition(self) -> TrafficLightState:
        """Realiza una transición y devuelve el nuevo estado."""
        transitions = {
            TrafficLightState.RED: TrafficLightState.GREEN,
            TrafficLightState.GREEN: TrafficLightState.YELLOW,
            TrafficLightState.YELLOW: TrafficLightState.RED,
        }

        self._state = transitions[self._state]
        self._cycle_count += 1

        return self._state