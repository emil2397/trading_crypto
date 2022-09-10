"""Main Flask script."""
import datetime
import warnings

from flask import Flask, request
from werkzeug.serving import run_simple

from funds.dashboard import Dashboard

warnings.filterwarnings("ignore")


GOOGLE_KEY_PATH = "./local_data/google_key.json"
SAVED_STATE_PATH = "./local_data/dashboard.json"
PRIMARY_SHEET_ID = 0
SECONDARY_SHEET_ID = 1
GOOGLE_SHEET_NAME = "trade_dashb_ngrok"
ALERT_FORMAT = ["alert", "ticker", "timeframe", "pattern", "time"]

dashboard = Dashboard(google_key_path=GOOGLE_KEY_PATH,
                      saved_state_path=SAVED_STATE_PATH,
                      google_sheet_name=GOOGLE_SHEET_NAME,
                      primary_sheet_id=PRIMARY_SHEET_ID,
                      secondary_sheet_id=SECONDARY_SHEET_ID)
app = Flask(__name__)


@app.route("/", methods=["POST"])
def get_alert():
    """Runs full pipeline."""
    alert_time = datetime.datetime.now()

    data = request.get_data(cache=True, as_text=True, parse_form_data=True).split(",")
    alert_format = ALERT_FORMAT[:len(data)]
    request_data = dict(zip(alert_format, data))
    request_data = [[request_data["ticker"], request_data["timeframe"], request_data["pattern"]]]

    print(f"New alert: {request_data}.")

    dashboard.update_data(request_data)
    dashboard.update_google_sheets()

    return "Done."


if __name__ == "__main__":
    run_simple("localhost", 80, app)
