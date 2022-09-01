"""Main Flask script."""
import datetime
import warnings

from flask import Flask, request
from werkzeug.serving import run_simple

from funds.dashboard import Dashboard

warnings.filterwarnings("ignore")


GOOGLE_KEY_PATH = "./local_data/google_key.json"
SAVED_STATE_PATH = "./local_data/dashboard.json"
ALERT_FORMAT = ["alert", "ticker", "timeframe", "pattern", "time"]

dashboard = Dashboard(google_key_path=GOOGLE_KEY_PATH, saved_state_path=SAVED_STATE_PATH)
app = Flask(__name__)


@app.route("/", methods=["POST"])
def hello():
    """Runs full pipeline."""
    alert_time = datetime.datetime.now()

    data = request.get_data(cache=True, as_text=True, parse_form_data=True)
    request_data = dict(zip(format, data.split(",")))
    request_data = [[request_data["ticker"], request_data["timeframe"], request_data["patter"]]]

    print("New alert: ", request_data)

    dashboard.update_data(request_data)
    dashboard.update_google_sheets(alert_time)

    return data


if __name__ == "__main__":
    run_simple("localhost", 80, app)
