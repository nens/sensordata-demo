import datetime
import logging

from pydantic import BaseModel

GROUNDWATER_DEVICE_NAME = "LevelstickSensoren"

logger = logging.getLogger(__name__)


class GroundwaterMeasurement(BaseModel):
    device_id: str
    timestamp: datetime.datetime
    pressure: float
    temperature: float


def _is_groundwater_measurement(item: dict) -> bool:
    """Return whether it is a proper groundwater measurement including all fields

    The goal is to prevent the rest of the code from having to do too many checks
    whether dictionary fields exist.
    """
    for first in ["time"]:
        if first not in item:
            logger.debug(f"{first} not found in item")
            return False

    for first, second in [
        ["deviceInfo", "deviceProfileName"],
        ["deviceInfo", "deviceName"],
        ["object", "grondwaterdruk"],
        ["object", "grondwatertemperatuur"],
    ]:
        if first not in item:
            logger.debug(f"{first} not found in item")
            return False
        if second not in item[first]:
            logger.debug(f"{first}>{second} not found in item")
            return False

    if item["deviceInfo"]["deviceProfileName"] != GROUNDWATER_DEVICE_NAME:
        return False
    return True


def _convert_to_groundwater_measurement(item: dict) -> GroundwaterMeasurement:
    return GroundwaterMeasurement(
        device_id=item["deviceInfo"]["deviceName"],
        timestamp=item["time"],
        pressure=item["object"]["grondwaterdruk"],
        temperature=item["object"]["grondwatertemperatuur"],
    )


def extract_groundwater_measurements(data: list) -> list:
    """Return usable groundwater measurements from the incoming json data"""
    return [
        _convert_to_groundwater_measurement(item)
        for item in data
        if _is_groundwater_measurement(item)
    ]
