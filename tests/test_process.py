import datetime
import json
from pathlib import Path
from unittest import mock

import pytest

from process import (
    GroundwaterMeasurement,
    extract_groundwater_measurement,
    upload_groundwater_measurement,
)

test_dir = Path(__file__).parent


@pytest.fixture
def groundwater_data() -> list:
    example_file = test_dir / "groundwaterlevel-example.json"
    return json.loads(example_file.read_text())


def test_extract_groundwater_measurement1(groundwater_data):
    assert extract_groundwater_measurement(groundwater_data[1])


def test_extract_groundwater_measurement2(groundwater_data):
    assert extract_groundwater_measurement(groundwater_data[0]) is None


def test_upload_groundwater_measurement1():
    groundwater_measurement = GroundwaterMeasurement(
        device_id="something",
        timestamp=datetime.datetime.now(),
        pressure=0,
        temperature=0,
    )
    with mock.patch("requests.post") as mocked_post:
        upload_groundwater_measurement(groundwater_measurement)
        mocked_post.assert_not_called()


def test_upload_groundwater_measurement2():
    groundwater_measurement = GroundwaterMeasurement(
        device_id="ls1815041",
        timestamp=datetime.datetime.now(),
        pressure=10,
        temperature=20,
    )
    with mock.patch("requests.post") as mocked_post:
        upload_groundwater_measurement(groundwater_measurement)
        mocked_post.assert_called()
