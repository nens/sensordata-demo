import datetime
import logging
import os

import requests

URL = os.environ.get("FROST_URL", "")

logger = logging.getLogger(__name__)

if not URL:
    logger.error("Environment variable 'FROST_URL' not defined.")


def find_sensor(device_name: str) -> int | None:
    """Return id of sensor, if found"""
    url = f"{URL}Sensors?$filter=name eq '{device_name}'"
    r = requests.get(url)
    r.raise_for_status()
    search_result = r.json()
    if not search_result["value"]:
        return
    # {
    #     "value": [
    #         {
    #             "@iot.selfLink": "https://sensordata-demo-frost.staging.lizard.net/FROST-Server/v1.1/Sensors(1)",
    #             "@iot.id": 1,
    #             "name": "ls2135023",
    #             "description": "ls2135023",
    #             "encodingType": "application/pdf",
    #             "metadata": "example.org/test.pdf",
    #             "properties": {"deviceInfo.devEui": "3531383150308b12"},
    #             "Datastreams@iot.navigationLink": "https://sensordata-demo-frost.staging.lizard.net/FROST-Server/v1.1/Sensors(1)/Datastreams",
    #         }
    #     ]
    # }

    # Just take the first (and hopefully only) one.
    found_sensor = search_result["value"][0]
    self_link = found_sensor["@iot.selfLink"]
    id = found_sensor["@iot.id"]
    logger.info(f"Found sensor id={id} for name '{device_name}': {self_link}")
    return id


def find_observed_property(property_name: str) -> int | None:
    """Return id of observed property, if found"""
    url = f"{URL}ObservedProperties?$filter=name eq '{property_name}'"
    r = requests.get(url)
    r.raise_for_status()
    search_result = r.json()
    if not search_result["value"]:
        return
    # Just take the first (and hopefully only) one.
    found_observed_property = search_result["value"][0]
    self_link = found_observed_property["@iot.selfLink"]
    id = found_observed_property["@iot.id"]
    logger.info(
        f"Found observed_property id={id} for name '{property_name}': {self_link}"
    )
    return id


def find_datastream(sensor_id: int, observed_property_id: int) -> int | None:
    url = f"{URL}Datastreams?$filter=ObservedProperty/id eq {observed_property_id} and Sensor/id eq {sensor_id}"
    r = requests.get(url)
    r.raise_for_status()
    search_result = r.json()
    if not search_result["value"]:
        return
    # Just take the first (and hopefully only) one.
    found_datastream = search_result["value"][0]
    self_link = found_datastream["@iot.selfLink"]
    id = found_datastream["@iot.id"]
    logger.info(
        f"Found datastream id={id} for sensor_id={sensor_id} and observed_property_id={observed_property_id}: {self_link}"
    )
    return id


def add_datastream_value(
    device_name: str, property_name: str, timestamp: datetime.datetime, value: float
):
    sensor_id = find_sensor(device_name=device_name)
    if not sensor_id:
        logger.warning(f"Sensor '{device_name}' not found in FROST")
        return
    observed_property_id = find_observed_property(property_name=property_name)
    if not observed_property_id:
        logger.warning(f"Observed property '{property_name}' not found in FROST")
        return
    datastream_id = find_datastream(
        sensor_id=sensor_id, observed_property_id=observed_property_id
    )
    if not datastream_id:
        logger.warning("Matching datastream not found in FROST")
        return

    url = URL + f"Datastreams({datastream_id})/Observations"
    payload = {"phenomenonTime": timestamp.isoformat(), "result": value}
    r = requests.post(url=url, json=payload)
    r.raise_for_status()
    logger.info(f"Added value ({value}) to datestream, timestamp={timestamp}")


if __name__ == "__main__":
    # Temp debug script only.
    logging.basicConfig(level=logging.INFO)
    find_sensor("aaa")
    sensor_id = find_sensor("ls2135023")
    find_observed_property("aaa")
    observed_property_id = find_observed_property("grondwaterdruk")
    find_datastream(sensor_id=sensor_id, observed_property_id=observed_property_id)
