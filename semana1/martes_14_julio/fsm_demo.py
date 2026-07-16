from enum import Enum, auto


class TrafficLightState(Enum):
    RED = auto()
    YELLOW = auto()
    GREEN = auto()


class TrafficLightFSM:
    def __init__(self) -> None:
        self._state = TrafficLightState.RED
        self._cycle_count = 0