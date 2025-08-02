from time import sleep
from typing import Tuple

import serial
from pydantic import dataclasses
from utils.logger import get_logger

logger = get_logger(__name__)

@dataclasses.dataclass
class Plug:
    id: int
    voltage: float
    power: float
    current: float
    active: bool
    voltage_unit: str = "V"
    power_unit: str = "W"
    current_unit: str = "mA"
    description: str = ""


class SerialCommunicationError(Exception):
    logger.error("Error communicating with arduino via serial port")
    pass


class ArduinoSerial:
    def __init__(self, port: str, baud_rate: int, timeout: int = 1) -> None:
        self.port = port
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.ser = None
        try:
            self.ser = serial.Serial(self.port, self.baud_rate, timeout=self.timeout)
        except serial.SerialException as e:
            raise SerialCommunicationError(f"Error connecting to serial: {e}")


    def read(self) -> str:
        try:
            return self.ser.readline().decode('utf-8').strip()
        except serial.SerialException as e:
            raise SerialCommunicationError(f"Error reading from serial: {e}")


    def close(self):
        self.ser.close()

    def get_measurements(self) -> Tuple[dict[int, Plug], int]:
        for i in range(1, 6):
            data = self.read()
            if data:
                plugs = {}
                time1 = 0
                for e in data.split(";"):
                    values = e.split(",")
                    if len(values) == 4:
                        logger.info(values)
                        plug_id, voltage, power, current = map(int, values)
                        plugs[plug_id] = Plug(plug_id, voltage, power, current, True)  # TODO return also the status
                    elif len(values) == 1 and e.startswith("t"):
                        time1 = int(e.replace("t", ""))
                    else:
                        logger.info(f"Got invalid data: {data}")
                        continue
                return plugs, time1
            else:
                logger.info(f"Waiting for data from serial attempt #{i}...")
                sleep(0.5)
        raise SerialCommunicationError("Unable to get data from serial connection")
