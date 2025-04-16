# Demo for sensordata/lora

Goal: figuring out applicability of two OGC standards for NL use cases. This repo is for [Nelen & Schuurmans](https://www.nelen-schuurmans.nl) to run tests based on Rotterdam's groundwater data. The groundwater measurements are send via LORA to [chirpstack](https://www.chirpstack.io/), which will send it to us.

First steps:

- [x] We have to recieve those measurements,
- [x] convert them to one of the two standards (sensorthings for now)
- [x] and recieve them in an OGC-compatible app.


## Work-in-progress comments

*Reinout using this section for some what-am-I-working-on comments and some initial impressions. This is not intended to be permanent.*

For the moment, I'm aiming at the "sensorthings" standard as there's a good open source server for it, [Frauenhofer's FROST](https://fraunhoferiosb.github.io/FROST-Server/).

The open source project suggested in the project documentation for the "connected systems" standard is a github branch of an existing project that last saw work two years ago. But... there is an up-to-date version specifically for connected systems at https://github.com/52North/connected-systems-pygeoapi .

Likewise, the sensorthings standard had quite some useful documentation on how to use it and how the data is structured. The connected systems documentation seemed to be a collection of urls meant to check the conformability to the spec, but not the actual spec. I probably haven't.

Regarding messages received from chirpstack: http+json *seems* the easiest way. If a protobuf binary message is send, apparently the full schema must be known+validated on our side. With json, se can just extract the fields we need.


## TODO

- [x] Deploy the "hello world" version.
- [x] Add POST url to receive messages from chirpstack (initially just for logging those messages and to get the communication set up).
- [x] Add docker-compose file with FROST-server.
- [x] Actually send messages towards FROST.
- [ ] Try to add the connected-systems app, too.

## Code structure

- `app.py`: [flask](https://flask.palletsprojects.com) app, mostly for providing an API url to receive chirpstack messages.
- `process.py`: process the incoming chirpstack messages and extract the info we want from them.


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
- TODO: `FROST_URL`.
