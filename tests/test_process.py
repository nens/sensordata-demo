from process import (
    extract_measurements,
)

EXAMPLE1 = {
    "deduplicationId": "031ba2cc-b590-4b6b-9a3f-a3ebc3b07309",
    "time": "2025-04-16T09:47:45.418+00:00",
    "deviceInfo": {
        "tenantId": "d3fa89ff-5e63-4377-ac1a-45b659ce49b3",
        "tenantName": "Gemeente Rotterdam",
        "applicationId": "a6876544-453b-4586-9df2-ab165acac6f6",
        "applicationName": "VONK-testserver",
        "deviceProfileId": "4c249de3-2c37-42ed-8fdd-baf81e1e1001",
        "deviceProfileName": "Milesight EM300-SLD waterleackage sensor",
        "deviceName": "wl001a",
        "devEui": "24e124136b325190",
        "deviceClassEnabled": "CLASS_A",
        "tags": {},
    },
    "devAddr": "fe00486b",
    "adr": True,
    "dr": 5,
    "fCnt": 3358,
    "fPort": 85,
    "confirmed": False,
    "data": "A2fAAARoWQUAAA==",
    "object": {"temperatuur": 19.2, "luchtvochtigheid": 44.5, "lekstatus": 0.0},
    "rxInfo": [
        {
            "gatewayId": "8d5ecb12457ba867",
            "uplinkId": 62578,
            "gwTime": "2025-04-16T09:47:45.418+00:00",
            "nsTime": "2025-04-16T09:47:45.481539820+00:00",
            "rssi": -113,
            "snr": 1.0,
            "context": "rEUlUA==",
            "metadata": {
                "gateway_lat": "51.992680074590261",
                "gateway_name": "zesty-cloud-grasshopper",
                "gateway_h3index": "8c196bb1300b9ff",
                "gateway_long": "4.357505731116153",
                "region_config_id": "eu868",
                "regi": "EU868",
                "region_common_name": "EU868",
                "network": "helium_iot",
                "gateway_id": "11Sg64hFLNcZxRHXB2Qy3LXGzTYrR4qtg9TXRi5sdNGfr1Br11w",
            },
            "crcStatus": "CRC_OK",
        },
        {
            "gatewayId": "2f908f24073a558e",
            "uplinkId": 24131,
            "gwTime": "2025-04-16T09:47:45.412+00:00",
            "nsTime": "2025-04-16T09:47:45.424852167+00:00",
            "rssi": -106,
            "snr": 4.5,
            "context": "w8ydEw==",
            "metadata": {
                "region_common_name": "EU868",
                "gateway_id": "11S7JEoKyKuMfmoRcYNQYAFyakV1WVoCTAuo3ag9bn3mt7ANDB6",
                "gateway_lat": "51.996388486106405",
                "regi": "EU868",
                "gateway_name": "cheerful-bamboo-spider",
                "network": "helium_iot",
                "gateway_h3index": "8c196bb131ac9ff",
                "gateway_long": "4.356386771661613",
                "region_config_id": "eu868",
            },
            "crcStatus": "CRC_OK",
        },
    ],
    "txInfo": {
        "frequency": 868300000,
        "modulation": {
            "lora": {"bandwidth": 125000, "spreadingFactor": 7, "codeRate": "CR_4_5"}
        },
    },
}

EXAMPLE2 = {
    "deduplicationId": "37cc04d6-a35b-4e54-8fdf-16236e639b41",
    "time": "2024-12-05T08:21:51.125+00:00",
    "deviceInfo": {
        "tenantId": "d3fa89ff-5e63-4377-ac1a-45b659ce49b3",
        "tenantName": "Gemeente Rotterdam",
        "applicationId": "b2d7c3ae-cab8-4b59-8b26-17d9565adfa2",
        "applicationName": "010-Levelstick-skynet",
        "deviceProfileId": "82ea7afa-b31e-4752-8fa0-fd87ba973072",
        "deviceProfileName": "LevelstickSensoren",
        "deviceName": "ls2135023",
        "devEui": "3531383150308b12",
        "deviceClassEnabled": "CLASS_A",
        "tags": {},
    },
    "devAddr": "fe004811",
    "adr": True,
    "dr": 5,
    "fCnt": 2483,
    "fPort": 1,
    "confirmed": False,
    "data": "AbQ1BPA=",
    "object": {"grondwaterdruk": 111669, "grondwatertemperatuur": 12.64},
    "rxInfo": [
        {
            "gatewayId": "7276ff000b030916",
            "uplinkId": 10895,
            "nsTime": "2024-12-05T08:21:51.223052730+00:00",
            "timeSinceGpsEpoch": "1417422129.125s",
            "rssi": -123,
            "snr": -7.2,
            "channel": 1,
            "board": 1,
            "location": {
                "latitude": 51.97224426269531,
                "longitude": 4.133676052093506,
                "altitude": 33,
            },
            "context": "3cK/ww==",
            "metadata": {"region_config_id": "eu868", "region_common_name": "EU868"},
            "crcStatus": "CRC_OK",
        },
        {
            "gatewayId": "6a1e3b228ae2a90c",
            "uplinkId": 47141,
            "gwTime": "2024-12-05T08:21:51.169+00:00",
            "nsTime": "2024-12-05T08:21:51.189278059+00:00",
            "rssi": -122,
            "snr": -6.8,
            "context": "ySV9BQ==",
            "metadata": {
                "gateway_name": "breezy-pineapple-sawfish",
                "region_common_name": "EU868",
                "gateway_long": "4.133624655108791",
                "gateway_h3index": "8c196bb9072edff",
                "network": "helium_iot",
                "regi": "EU868",
                "gateway_id": "112vksk3PA36iqE6x6LHTrQU5Y2hWjXG4mRQpc8EehdNNDHAZyCJ",
                "gateway_lat": "51.976991314096999",
                "region_config_id": "eu868",
            },
            "crcStatus": "CRC_OK",
        },
        {
            "gatewayId": "dcd1b5dcb5c53623",
            "uplinkId": 33448,
            "gwTime": "2024-12-05T08:21:51.147+00:00",
            "nsTime": "2024-12-05T08:21:51.162296315+00:00",
            "rssi": -106,
            "snr": 3.5,
            "context": "lPU1cg==",
            "metadata": {
                "network": "helium_iot",
                "gateway_h3index": "8c196bb908a95ff",
                "region_config_id": "eu868",
                "gateway_long": "4.144536626723536",
                "gateway_name": "strong-cornflower-parrot",
                "gateway_id": "11k9dRJMxFdPu1tMJiMz8et5jitVQ9kXbtC4cBvUsDoUNSV1DCM",
                "regi": "EU868",
                "region_common_name": "EU868",
                "gateway_lat": "51.985135248530611",
            },
            "crcStatus": "CRC_OK",
        },
        {
            "gatewayId": "1a53471331289857",
            "uplinkId": 10895,
            "nsTime": "2024-12-05T08:21:51.226635542+00:00",
            "timeSinceGpsEpoch": "1417422129.125s",
            "rssi": -123,
            "snr": -7.2,
            "channel": 1,
            "board": 1,
            "context": "3cK/ww==",
            "metadata": {
                "region_common_name": "EU868",
                "thingsix_airtime_ms": "51",
                "thingsix_gateway_id": "0x95774ed044fe8e0a78bbda718389488672f7a11591fe4aaa3ea1f12c5eca573d",
                "region_config_id": "eu868",
                "thingsix_owner": "0x9b04F074773E64F9c0412376c5d60f94E38193Bc",
            },
            "crcStatus": "CRC_OK",
        },
    ],
    "txInfo": {
        "frequency": 867300000,
        "modulation": {
            "lora": {"bandwidth": 125000, "spreadingFactor": 7, "codeRate": "CR_4_5"}
        },
    },
}

EXAMPLE3 = {
    "time": "2024-12-05T08:21:51.125+00:00",
    "deviceInfo": {
        "tenantId": "d3fa89ff-5e63-4377-ac1a-45b659ce49b3",
        "tenantName": "Gemeente Rotterdam",
        "applicationId": "b2d7c3ae-cab8-4b59-8b26-17d9565adfa2",
        "applicationName": "010-Levelstick-skynet",
        "deviceProfileId": "82ea7afa-b31e-4752-8fa0-fd87ba973072",
        "deviceProfileName": "LevelstickSensoren",
        "deviceName": "ls2135023",
        "devEui": "3531383150308b12",
        "deviceClassEnabled": "CLASS_A",
        "tags": {},
    },
    "level": "WARNING",
    "code": "UPLINK_F_CNT_RETRANSMISSION",
    "description": "Uplink was flagged as re-transmission / frame-counter did not increment",
    "context": {"deduplication_id": "420cad7a-01fa-419e-96b2-4b486446f058"},
}


def test_extract_measurement1():
    assert len(extract_measurements(EXAMPLE1)) == 3


def test_extract_measurement2():
    measurements = extract_measurements(EXAMPLE2)
    assert sorted([measurement.property_name for measurement in measurements]) == [
        "grondwaterdruk",
        "grondwatertemperatuur",
    ]


def test_extract_measurement3():
    assert extract_measurements(EXAMPLE3) is None


# def test_upload_groundwater_measurement1():
#     groundwater_measurement = GroundwaterMeasurement(
#         device_id="something",
#         timestamp=datetime.datetime.now(),
#         pressure=0,
#         temperature=0,
#     )
#     with mock.patch("requests.post") as mocked_post:
#         upload_groundwater_measurement(groundwater_measurement)
#         mocked_post.assert_not_called()


# def test_upload_groundwater_measurement2():
#     groundwater_measurement = GroundwaterMeasurement(
#         device_id="ls1815041",
#         timestamp=datetime.datetime.now(),
#         pressure=10,
#         temperature=20,
#     )
#     with mock.patch("requests.post") as mocked_post:
#         upload_groundwater_measurement(groundwater_measurement)
#         mocked_post.assert_called()
