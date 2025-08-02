import sys
import os
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pdu_io.read_serial import ArduinoSerial

@patch("pdu_io.read_serial.serial.Serial")
@patch.object(ArduinoSerial, "read")
def test_get_measurements(mock_read, mock_serial):
    mock_serial.return_value = MagicMock()

    mock_read.return_value = "1,230,100,500;2,231,200,400;t1234"

    arduino = ArduinoSerial(port="/dev/null", baud_rate=9600)

    plugs, time1 = arduino.get_measurements()

    assert time1 == 1234
    assert len(plugs) == 2

    plug1 = plugs[1]
    assert plug1.voltage == 230
    assert plug1.power == 100
    assert plug1.current == 500
    assert plug1.active is True

    plug2 = plugs[2]
    assert plug2.voltage == 231
    assert plug2.power == 200
    assert plug2.current == 400
    assert plug2.active is True
