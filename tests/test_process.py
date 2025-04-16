import json
from pathlib import Path

import pytest

from process import extract_groundwater_measurement

test_dir = Path(__file__).parent


@pytest.fixture
def groundwater_data() -> list:
    example_file = test_dir / "groundwaterlevel-example.json"
    return json.loads(example_file.read_text())


def test_extract_groundwater_measurement1(groundwater_data):
    assert extract_groundwater_measurement(groundwater_data[1])


def test_extract_groundwater_measurement2(groundwater_data):
    assert extract_groundwater_measurement(groundwater_data[0]) is None
