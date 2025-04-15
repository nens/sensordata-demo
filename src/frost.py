import os

import frost_sta_client

URL = os.environ.get("FROST_URL")


def service():
    return frost_sta_client.SensorThingsService(URL)
