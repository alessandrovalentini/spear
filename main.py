from fastapi import FastAPI, HTTPException, status
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST, CollectorRegistry
from fastapi.responses import Response
import logging
import uvicorn

from pdu_io.read_serial import Plug, ArduinoSerial, SerialCommunicationError
from utils.setup import load_settings

settings = load_settings("config.yaml")
arduino = ArduinoSerial(settings.serial.port, settings.serial.baud_rate, timeout=settings.serial.timeout)
ready = False

# use custom registry to hide default python metrics
custom_registry = CollectorRegistry()

plug_voltage = Gauge("plug_voltage", "Voltage per plug", ["plug_id", "description"], registry=custom_registry)
plug_current = Gauge("plug_current", "Current per plug", ["plug_id", "description"], registry=custom_registry)
plug_power = Gauge("plug_power", "Power per plug", ["plug_id", "description"], registry=custom_registry)
plug_active = Gauge("plug_active", "Active status of plug", ["plug_id", "description"], registry=custom_registry)
measure_time = Gauge("measure_time", "Time required to measure", registry=custom_registry)

app = FastAPI()


def update_metrics():
    plugs, time = arduino.get_measurements()
    for plug in plugs.values():
        labels = {"plug_id": str(plug.id), "description": plug.description}
        plug_voltage.labels(**labels).set(plug.voltage)
        plug_current.labels(**labels).set(plug.current)
        plug_power.labels(**labels).set(plug.power)
        plug_active.labels(**labels).set(1 if plug.active else 0)
    measure_time.set(time)


@app.get("/metrics")
def metrics():
    update_metrics()
    return Response(generate_latest(custom_registry), media_type=CONTENT_TYPE_LATEST)


@app.get("/plugs", response_model=list[Plug])
def list_plugs():
    plugs, time = arduino.get_measurements()
    return plugs.values()


@app.get("/plugs/{plug_id}", response_model=Plug)
def get_plug(plug_id: int) -> Plug:
    plugs, time = arduino.get_measurements()
    if plug_id <= len(plugs):
        return plugs.get(plug_id)
    else:
        raise HTTPException(status_code=404, detail=f"Plug {plug_id} not found")


@app.get("/healthz")
def liveness():
    return {"status": "alive"}


@app.get("/readyz")
def readiness(response: Response):
    if ready:
        return {"status": "ready"}
    response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return {"status": "not ready"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
