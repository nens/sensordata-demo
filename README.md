# Demo for sensordata/lora

Goal: figuring out applicability of two OGC standards for NL use cases. This repo is for [Nelen & Schuurmans](https://www.nelen-schuurmans.nl) to run tests based on Rotterdam's groundwater data. The groundwater measurements are send via LORA to [chirpstack](https://www.chirpstack.io/), which will send it to us.


## External servers/services

We implemented the "sensorthings" standard as there's a good open source server for it,
[Frauenhofer's FROST](https://fraunhoferiosb.github.io/FROST-Server/). We installed it with "docker compose". The server is available as https://sensordata-demo-frost.staging.lizard.net/FROST-Server/ with anonymous access enabled.

The open source project suggested in the project documentation for the "connected systems" standard is a github branch of an existing project that last saw work two years ago. But... there is an up-to-date version specifically for connected systems at https://github.com/52North/connected-systems-pygeoapi . We tried getting that to work based on the project's suggested "docker compose" approach, but the resulting site was not functional. We've submitted [a detailed bug report](https://github.com/52North/connected-systems-pygeoapi/issues/7) and received answer that the public docker images haven't been updated and that the current version is faulty. That's why we haven't included "connected systems" in our actual demo.

The sensorthings standard has quite some useful documentation on how to use it and how the data is structured.

Regarding messages received from chirpstack: http+json *seems* the easiest way. If a protobuf binary message is send, apparently the full schema must be known+validated on our side. With json, we can just extract the fields we need. http+json was also Rotterdam's preferred approach. So we created a simple web app (see `app.py` below) with a URL where Rotterdam could send their messages to.

Chirpstack allows extra http headers to be configured on the outgoing messages. This is a flexible scheme that allows all sorts of authentication schemes. We're using "http basic auth" which simply means user/password. An extra header `Authorization` with a value like `Basic abcbase64encoded123=` is quickly added to the chirpstack configuration for our URL.


## Code structure in `src/`

- `app.py`: [flask](https://flask.palletsprojects.com) app, mostly for providing an API url to receive chirpstack messages.
- `process.py`: process the incoming chirpstack messages and extract the info we want from them. This means filtering messages: which have measurements and which are just administration? A message can contain multiple values at the same time, so it is split into separate "measurements".
- `frost.py`: query the FROST sensorthings api and post new measurements to datastreams. For every measurement, we look for a matching sensorthings `sensor` based on name. Likewise for an `observed property`. Then we query for a `datastream` based on the ID of the sensor and observed property. Lastly we add the measurement's value to the datastream.

The `scripts/` directory contains the script we use to upload data from FROST to our [lizard datawarehouse](https://nxt3.staging.lizard.net/viewer/favourites/86542561-3feb-4035-aa39-299bfc80a6930).


## Local dev setup

Install `uv` and call `uv sync`. Enable the virtualenv with `source .venv/bin/activate`.

Testing and formatting happens with `pre-commit run --all`.

Run the app with `python src/app.py` (assuming you've activated the virtualenv of course).


## Deploy notes

(Only interesting for N&S). Regular ansible provision/deploy stuff. As this is an open source repo, the `provision.yml` and `inventory.txt` aren't stored here, they're only on Reinout's computer for now.

Add `etc/htpasswd` file on the server.

Environment variables are handled in the `.env` file.

- `SENTRY_DSN` for traceback logging.
- `API_USER` and `API_USER_HASH` for the user/password for the POST url.
- `FROST_URL` with the base url for the FROST sensorthings server (Like `https://user:pass@frost-server-url/FROST-Server/v1.1/`, note the trailing slash).
