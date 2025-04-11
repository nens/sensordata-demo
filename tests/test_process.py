import json
from pathlib import Path

import pytest

from process import extract_groundwater_measurements

test_dir = Path(__file__).parent


@pytest.fixture
def groundwater_data() -> list:
    example_file = test_dir / "groundwaterlevel-example.json"
    return json.loads(example_file.read_text())


def test_extract_groundwater_measurements1():
    assert extract_groundwater_measurements([]) == []


def test_extract_groundwater_measurements2(groundwater_data):
    assert len(extract_groundwater_measurements(groundwater_data)) == 7
