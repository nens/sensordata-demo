import logging
import os

import sentry_sdk
from flask import Flask, redirect, render_template, url_for
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash

USERS = {
    # from werkzeug.security import generate_password_hash
    # ^^^ Use this to create a hash.
    "reinout": "scrypt:32768:8:DUMMY-DUMMY-DUMMY",
}


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


@app.route("/historical-flood-risk-events/new/", methods=["POST"])
@auth.login_required
def new_flood_risk_event():
    # Do something
    return redirect(url_for("historical_flood_risk_events"))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    debug = os.environ.get("DEBUG", "").lower() in ("true", "1")
    app.run(host="0.0.0.0", port=8000, debug=debug)
