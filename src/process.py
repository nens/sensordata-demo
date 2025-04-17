import datetime
import logging

from pydantic import BaseModel

from frost import add_datastream_value

# Hardcoded sensor ID, coupled with the two "datastream" IDs for the two properties.
CONFIGURED_DEVICE_ID = "ls1815041"
PRESSURE_ID = 2
TEMPERATURE_ID = 3
# Key: hardcoded sensor ID.
# Value: dict of variable name (from GroundWaterMeasurement) and datastream ID.
CONFIGURED_DEVICES = {
    "ls1815041": {"pressure": 2, "temperature": 3},
}


logger = logging.getLogger(__name__)


class Measurement(BaseModel):
    device_name: str
    timestamp: datetime.datetime
    property_name: str
    value: float  # At the moment we just hardcode it to floats...


def _is_measurement(item: dict) -> bool:
    """Return whether it is a proper measurement including all fields we need

    The goal is to prevent the rest of the code from having to do too many checks
    whether dictionary fields exist.
    """
    for first in ["time", "object"]:
        if first not in item:
            logger.info(f"'{first}' not found in item")
            return False

    for first, second in [
        ["deviceInfo", "deviceName"],
    ]:
        if first not in item:
            logger.info(f"'{first}' not found in item")
            return False
        if second not in item[first]:
            logger.info(f"'{first}>{second}' not found in item")
            return False

    if not item["object"]:
        logger.info("'object' key is empty, ignoring it")
        return False
    return True


def extract_measurements(data: dict) -> list[Measurement] | None:
    """Return usable groundwater measurements from the incoming json data"""
    if not _is_measurement(data):
        return None
    result = []
    device_name = data["deviceInfo"]["deviceName"]
    timestamp = data["time"]
    properties = data["object"]
    for property_name in properties:
        value = properties[property_name]
        result.append(
            Measurement(
                device_name=device_name,
                timestamp=timestamp,
                property_name=property_name,
                value=value,
            )
        )
    return result


def upload_measurement(measurement: Measurement):
    add_datastream_value(
        device_name=measurement.device_name,
        property_name=measurement.property_name,
        timestamp=measurement.timestamp,
        value=measurement.value,
    )
