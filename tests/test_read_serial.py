import sys
import os
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pdu_io.read_serial import ArduinoSerial, Plug

# Examples
ex_plug1 = Plug(id=1, voltage=230, power=100, current=500, active=True, description="")
ex_plug2 = Plug(id=2, voltage=240, power=150, current=600, active=True, description="")
ex_time = 1234


@patch("pdu_io.read_serial.serial.Serial")
@patch.object(ArduinoSerial, "read")
def test_get_measurements(mock_read, mock_serial):
    mock_serial.return_value = MagicMock()
    mock_read.return_value = f"{ex_plug1.id},{ex_plug1.voltage},{ex_plug1.power},{ex_plug1.current};{ex_plug2.id},{ex_plug2.voltage},{ex_plug2.power},{ex_plug2.current};t{ex_time}"
    arduino = ArduinoSerial(port="/dev/null", baud_rate=9600)

    plugs, time1 = arduino.get_measurements()

    assert time1 == ex_time
    assert len(plugs) == 2
    assert plugs[1] == ex_plug1
    assert plugs[2] == ex_plug2
