import datetime
import os

import frost_sta_client
import requests

URL = os.environ.get("FROST_URL", "")


def service():
    return frost_sta_client.SensorThingsService(URL)


def add_datastream_value(
    datastream_id: int, timestamp: datetime.datetime, value: float
):
    url = URL + f"Datastreams({datastream_id})/Observations"
    payload = {"phenomenonTime": timestamp.isoformat(), "result": value}
    requests.post(url=url, json=payload)
