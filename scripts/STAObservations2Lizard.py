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
locList = []
if res.status_code == 200:
    for loc in res.json()["results"]:
        locList.append(
            {"loc_uuid": loc["uuid"], "loc_code": loc["code"], "timeseries": []}
        )
locCnt = 0
for loc in locList:
    res = requests.get(
        url=LIZARD_BASE_URL + "timeseries/?location__uuid={}".format(loc["loc_uuid"]),
        headers=liz_headers,
    )
    if res.status_code == 200:
        for ts in res.json()["results"]:
            locList[locCnt]["timeseries"].append(
                {
                    "ts_uuid": ts["uuid"],
                    "ts_obstype": ts["observation_type"]["code"],
                    "ts_end": ts["end"],
                }
            )
    locCnt += 1

### Find corresponding STA Datastreams based on FeatureOfInterest and ObservedProperty
locCnt = 0
for loc in locList:
    res = requests.get(
        url=STA_BASE_URL
        + "/Things?$filter=name%20eq%20%27{}%27".format(loc["loc_code"]),
        headers=sta_headers,
    )
    thingId = res.json()["value"][0]["@iot.id"]
    locList[locCnt].update({"thing_id": thingId})
    tsCnt = 0
    for ts in loc["timeseries"]:
        res = requests.get(
            url=STA_BASE_URL
            + "/ObservedProperties?$filter=name%20eq%20%27{}%27".format(
                ts["ts_obstype"]
            ),
            headers=sta_headers,
        )
        ObsPropId = res.json()["value"][0]["@iot.id"]
        locList[locCnt]["timeseries"][tsCnt].update({"obsprop_id": ObsPropId})
        tsCnt += 1
    locCnt += 1


### Collect Observations from STA Datastreams and POST to Lizard
for loc in locList:
    for ts in loc["timeseries"]:
        url = (
            STA_BASE_URL
            + "/Datastreams?$filter=ObservedProperty/"
            + f"id%20eq%20{ts['obsprop_id']}%20and%20Thing/id%20eq%20{loc['thing_id']}"
        )

        res = requests.get(
            url=url,
            headers=sta_headers,
        )
        dsList = []
        for ds in res.json()["value"]:
            dsList.append(ds["@iot.id"])
        ### GET Observations
        url = STA_BASE_URL + "/Observations?$filter=Datastream/id%20in%20("
        dsCnt = 0
        for ds in dsList:
            url += f"{ds}"
            if dsCnt < len(dsList) - 1:
                url += ",%20"
            dsCnt += 1
        url += ")"
        if ts["ts_end"]:
            url += "%20and%20phenomenonTime%20gt%20{}".format(ts["ts_end"])
        # print(url)
        res = requests.get(url=url, headers=sta_headers)
        liz_events = []
        for value in res.json()["value"]:
            liz_events.append(
                {"time": value["phenomenonTime"], "value": value["result"]}
            )
        ### POST Observations to Lizard Timeseries objects
        url = LIZARD_BASE_URL + "timeseries/{}/events/".format(ts["ts_uuid"])
        res = requests.post(url=url, headers=liz_headers, data=json.dumps(liz_events))
        print(
            f"Timeseries with UUID {ts['ts_uuid']} updated with {len(liz_events)} events."
        )
