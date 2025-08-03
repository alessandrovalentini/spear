import os
import sys
from unittest.mock import patch
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pdu_io.read_serial import Plug
from main import app

client = TestClient(app)
plug1 = Plug(id=1, voltage=230, power=100, current=500, active=True, description="Plug 1")
plug2 = Plug(id=2, voltage=240, power=150, current=600, active=False, description="Plug 2")


@patch("pdu_io.read_serial.ArduinoSerial.get_measurements")
def test_metrics(mock_get_measurements):
    mock_get_measurements.return_value = ({1: plug1}, 123)

    response = client.get("/metrics")
    assert response.status_code == 200
    text = response.text
    assert "plug_voltage" in text
    assert "plug_current" in text
    assert "plug_power" in text
    assert "plug_active" in text
    assert "measure_time" in text


@patch("pdu_io.read_serial.ArduinoSerial.get_measurements")
def test_list_plugs(mock_get_measurements):
    mock_get_measurements.return_value = ({1: plug1, 2: plug2}, 100)

    response = client.get("/plugs")
    assert response.status_code == 200
    json_data = response.json()
    assert isinstance(json_data, list)
    assert len(json_data) == 2
    assert json_data[0]["id"] == 1
    assert json_data[1]["active"] is False


@patch("pdu_io.read_serial.ArduinoSerial.get_measurements")
def test_get_plug_found(mock_get_measurements):
    mock_get_measurements.return_value = ({1: plug1}, 100)

    response = client.get("/plugs/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["voltage"] == 230


@patch("pdu_io.read_serial.ArduinoSerial.get_measurements")
def test_get_plug_not_found(mock_get_measurements):
    mock_get_measurements.return_value = ({1: plug1}, 100)

    response = client.get("/plugs/2")
    assert response.status_code == 404
    assert response.json()["detail"] == "Plug 2 not found"


def test_healthz():
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "alive"}
