import logging
import os

import sentry_sdk
from flask import Flask, render_template, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash

import process

USERS = {
    # from werkzeug.security import generate_password_hash
    # ^^^ Use this to create a hash.
    # "reinout": "scrypt:32768:8:DUMMY-DUMMY-DUMMY",
}

if "API_USER" in os.environ:
    user = os.environ["API_USER"]
    password_hash = os.environ["API_USER_HASH"]
    USERS[user] = password_hash


if "SENTRY_DSN" in os.environ:
    # Initialize sentry *before* setting up the flask app.
    sentry_sdk.init(dsn=os.environ["SENTRY_DSN"])


app = Flask(__name__, template_folder="templates")
auth = HTTPBasicAuth()
logger = logging.getLogger(__name__)


# Basic auth handling.
@auth.verify_password
def verify_password(username, password):
    logger.info(f"Verifying password for user {username}")
    if username in USERS and check_password_hash(USERS[username], password):
        return username


@app.route("/")
def index():
    return render_template(
        "index.html",
    )


@app.route("/frost-overview/")
def frost_overview():
    return render_template(
        "frost_overview.html",
    )


@app.route("/from-chirpstack/", methods=["POST"])
@auth.login_required
def handle_post_from_chirpstack():
    # First some debug logging: the auth headers we receive are not correct yet..
    # logger.debug(f"Incoming POST from chirpstack. Headers: {request.headers}")
    data = request.json
    # Log the incoming data to figure out what we can do with it :-)
    logger.info(f"Incoming data: \n{data}")
    if not isinstance(data, dict):
        logger.warning("Not a dict, rejecting it")
        return {"error": "Expecting a single item"}, 400
    measurements = process.extract_measurements(data)
    if not measurements:
        msg = "Not a proper measurement with values, ignoring it."
        logger.info(msg)
        return {"msg": msg}, 200
    logger.info(f"Extracted {len(measurements)} measurements, trying to upload them")
    for measurement in measurements:
        process.upload_measurement(measurement)
    msg = f"Received {len(measurements)} values"
    return {"msg": msg}, 201


if __name__ == "__main__":
    # Direct dev debug run.
    logging.basicConfig(level=logging.DEBUG)
    app.run(host="0.0.0.0", port=8000, debug=True)
    # ^^^ Production runs with gunicorn, so debug=True is fine here :-)


if __name__ != "__main__":
    # Probably called through gunicorn.
    gunicorn_logger = logging.getLogger("gunicorn.error")
    root_logger = logging.getLogger("")
    root_logger.handlers = gunicorn_logger.handlers
    root_logger.setLevel(gunicorn_logger.level)
