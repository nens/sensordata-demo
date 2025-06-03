import base64
import json
import os
import sys

import requests

STA_BASE_URL = "https://sensordata-demo-frost.staging.lizard.net/FROST-Server/v1.1"
LIZARD_BASE_URL = "https://nxt3.staging.lizard.net/api/v4/"
LIZARD_ORG_UUID = "5387079c-5cb0-4286-9d7b-425c6d6592cf"

# Passwords from environment variables
LIZARD_PASSWORD = os.environ.get("LIZARD_PASSWORD")
STA_PASSWORD = os.environ.get("STA_PASSWORD")
if not LIZARD_PASSWORD and STA_PASSWORD:
    sys.exit("Set both LIZARD_PASSWORD and STA_PASSWORD environment variables")

liz_headers = {
    "username": "__key__",
    "password": LIZARD_PASSWORD,
    "Content-Type": "application/json",
}

sta_headers = {
    "Authorization": "Basic "
    + base64.b64encode(f"admin:{STA_PASSWORD}".encode()).decode(),
    "Content-Type": "application/json",
}

### Collect Lizard Locations and Timeseries
res = requests.get(
    url=LIZARD_BASE_URL + f"locations/?organisation__uuid={LIZARD_ORG_UUID}",
    headers=liz_headers,
)
locations = []
res.raise_for_status()

for location in res.json()["results"]:
    locations.append(
        {
            "loc_uuid": location["uuid"],
            "loc_code": location["code"],
            "timeseries": [],
        }
    )

print(f"Found {len(locations)} locations")

for location in locations:
    res = requests.get(
        url=LIZARD_BASE_URL
        + "timeseries/?location__uuid={}".format(location["loc_uuid"]),
        headers=liz_headers,
    )
    res.raise_for_status()
    for timeserie in res.json()["results"]:
        location["timeseries"].append(
            {
                "ts_uuid": timeserie["uuid"],
                "ts_obstype": timeserie["observation_type"]["code"],
                "ts_end": timeserie["end"],
            }
        )

### Find corresponding STA Datastreams based on FeatureOfInterest and ObservedProperty
for location in locations:
    res = requests.get(
        url=STA_BASE_URL
        + "/Things?$filter=name%20eq%20%27{}%27".format(location["loc_code"]),
        headers=sta_headers,
    )
    res.raise_for_status()
    thingId = res.json()["value"][0]["@iot.id"]
    location.update({"thing_id": thingId})
    for timeserie in location["timeseries"]:
        res = requests.get(
            url=STA_BASE_URL
            + "/ObservedProperties?$filter=name%20eq%20%27{}%27".format(
                timeserie["ts_obstype"]
            ),
            headers=sta_headers,
        )
        res.raise_for_status()
        ObsPropId = res.json()["value"][0]["@iot.id"]
        timeserie["obsprop_id"] = ObsPropId


### Collect Observations from STA Datastreams and POST to Lizard
for location in locations:
    for timeserie in location["timeseries"]:
        url = (
            STA_BASE_URL
            + "/Datastreams?$filter=ObservedProperty/"
            + f"id%20eq%20{timeserie['obsprop_id']}%20and%20Thing/id%20eq%20{location['thing_id']}"
        )

        res = requests.get(
            url=url,
            headers=sta_headers,
        )
        res.raise_for_status()
        datastream_ids = [
            str(datastream["@iot.id"]) for datastream in res.json()["value"]
        ]
        ### GET Observations
        url = STA_BASE_URL + "/Observations?$filter=Datastream/id%20in%20("
        url += ",%20".join(datastream_ids)
        url += ")"
        if timeserie["ts_end"]:
            url += "%20and%20phenomenonTime%20gt%20{}".format(timeserie["ts_end"])
        # print(url)
        res = requests.get(url=url, headers=sta_headers)
        liz_events = []
        for value in res.json()["value"]:
            liz_events.append(
                {"time": value["phenomenonTime"], "value": value["result"]}
            )
        ### POST Observations to Lizard Timeseries objects
        url = LIZARD_BASE_URL + "timeseries/{}/events/".format(timeserie["ts_uuid"])
        res = requests.post(url=url, headers=liz_headers, data=json.dumps(liz_events))
        print(f"liz_events: {liz_events}")
        res.raise_for_status()
        print(
            f"Timeseries with UUID {timeserie['ts_uuid']} updated with {len(liz_events)} events."
        )
