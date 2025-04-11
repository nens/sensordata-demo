from process import extract_groundwater_measurements


def test_extract_groundwater_measurements():
    assert extract_groundwater_measurements([]) == []
