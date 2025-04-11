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
    if username in USERS and check_password_hash(USERS[username], password):
        return username


@app.route("/")
def index():
    return render_template(
        "index.html",
    )


@app.route("/from-chirpstack/", methods=["POST"])
@auth.login_required
def handle_post_from_chirpstack():
    # First some debug logging.
    logger.info("Incoming POST from chirpstack. Headers:")
    logger.info(request.headers)
    data = request.json
    # For now, just log the data.
    logger.info(data)
    if not isinstance(data, list):
        return {"error": "Expecting a list of items"}, 400
    groundwater_measurements = process.extract_groundwater_measurements(data)
    logger.info(groundwater_measurements)

    return {"dummy", "just logging for now"}, 201


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app.run(host="0.0.0.0", port=8000, debug=True)
    # ^^^ Production runs with gunicorn, so debug=True is fine here :-)
