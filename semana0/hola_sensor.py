class Sensor:
    def __init__(self, sensor_id: str) -> None:
        self.sensor_id = sensor_id
        
    def read(self) -> float:
        return 23.5
    