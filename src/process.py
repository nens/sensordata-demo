import datetime
import logging

from pydantic import BaseModel

from frost import add_datastream_value

GROUNDWATER_DEVICE_NAME = "LevelstickSensoren"

# Hardcoded sensor ID, coupled with the two "datastream" IDs for the two properties.
CONFIGURED_DEVICE_ID = "ls1815041"
PRESSURE_ID = 2
TEMPERATURE_ID = 3

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
            logger.debug(f"'{first}' not found in item")
            return False

    for first, second in [
        ["deviceInfo", "deviceProfileName"],
        ["deviceInfo", "deviceName"],
        ["object", "grondwaterdruk"],
        ["object", "grondwatertemperatuur"],
    ]:
        if first not in item:
            logger.debug(f"'{first}' not found in item")
            return False
        if second not in item[first]:
            logger.debug(f"'{first}>{second}' not found in item")
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


def extract_groundwater_measurement(data: dict) -> GroundwaterMeasurement | None:
    """Return usable groundwater measurements from the incoming json data"""
    if not _is_groundwater_measurement(data):
        return None
    return _convert_to_groundwater_measurement(data)


def upload_groundwater_measurement(groundwater_measurement: GroundwaterMeasurement):
    if groundwater_measurement.device_id != CONFIGURED_DEVICE_ID:
        logger.debug("Device id is not the single hardcoded one: ignoring it")
        return
    add_datastream_value(
        datastream_id=PRESSURE_ID,
        timestamp=groundwater_measurement.timestamp,
        value=groundwater_measurement.pressure,
    )
    add_datastream_value(
        datastream_id=TEMPERATURE_ID,
        timestamp=groundwater_measurement.timestamp,
        value=groundwater_measurement.temperature,
    )
