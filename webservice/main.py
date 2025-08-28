import argparse

from pathlib import Path
from fastapi import FastAPI, HTTPException
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST, CollectorRegistry
from fastapi.responses import Response

from pdu_io.read_serial import Plug, ArduinoSerial
from utils.setup import load_settings
from utils.stub import mock_read

parser = argparse.ArgumentParser()
parser.add_argument('--demo', action='store_true', help='Start SPEAR with random generator')
args, _ = parser.parse_known_args()

BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "config.yaml"
settings = load_settings(CONFIG_PATH)

_arduino_instance = None


def get_arduino():
    global _arduino_instance
    if _arduino_instance is None:
        _arduino_instance = ArduinoSerial(
            settings.serial.port,
            settings.serial.baud_rate,
            timeout=settings.serial.timeout
        )
    return _arduino_instance


if args.demo:
    print("[DEMO MODE] Data will be randomly generated and not read from serial.")
    ArduinoSerial.__init__ = lambda self, *a, **kw: None
    ArduinoSerial.read = mock_read

# --- Prometheus custom registry ---
custom_registry = CollectorRegistry()

plug_voltage = Gauge("plug_voltage", "Voltage per plug", ["plug_id", "description"], registry=custom_registry)
plug_current = Gauge("plug_current", "Current per plug", ["plug_id", "description"], registry=custom_registry)
plug_power = Gauge("plug_power", "Power per plug", ["plug_id", "description"], registry=custom_registry)
plug_active = Gauge("plug_active", "Active status of plug", ["plug_id", "description"], registry=custom_registry)
measure_time = Gauge("measure_time", "Time required to measure", registry=custom_registry)


def update_metrics():
    plugs, time = get_arduino().get_measurements()
    for plug in plugs.values():
        labels = {"plug_id": str(plug.id), "description": plug.description}
        plug_voltage.labels(**labels).set(plug.voltage)
        plug_current.labels(**labels).set(plug.current)
        plug_power.labels(**labels).set(plug.power)
        plug_active.labels(**labels).set(1 if plug.active else 0)
    measure_time.set(time)


app = FastAPI()


@app.get("/metrics")
def metrics():
    update_metrics()
    return Response(generate_latest(custom_registry), media_type=CONTENT_TYPE_LATEST)


@app.get("/plugs", response_model=list[Plug])
def list_plugs():
    plugs, time = get_arduino().get_measurements()
    return plugs.values()


@app.get("/plugs/{plug_id}", response_model=Plug)
def get_plug(plug_id: int) -> Plug:
    plugs, time = get_arduino().get_measurements()
    if plug_id <= len(plugs):
        return plugs.get(plug_id)
    else:
        raise HTTPException(status_code=404, detail=f"Plug {plug_id} not found")


@app.get("/healthz")
def liveness():
    return {"status": "alive"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000)
