import datetime
import logging
import os

import requests

URL = os.environ.get("FROST_URL", "")

logger = logging.getLogger(__name__)

if not URL:
    logger.error("Environment variable 'FROST_URL' not defined.")


def add_datastream_value(
    datastream_id: int, timestamp: datetime.datetime, value: float
):
    url = URL + f"Datastreams({datastream_id})/Observations"
    payload = {"phenomenonTime": timestamp.isoformat(), "result": value}
    requests.post(url=url, json=payload)
