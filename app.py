"""Main Flask script."""
import datetime
import warnings

from flask import Flask, request
from werkzeug.serving import run_simple

from funds.dashboard import Dashboard

warnings.filterwarnings("ignore")


GOOGLE_KEY_PATH = "./local_data/google_key.json"

dashboard = Dashboard(google_key_path=GOOGLE_KEY_PATH)
app = Flask(__name__)


@app.route("/", methods=["POST"])
def hello():
    """Runs full pipeline."""
    alert_time = datetime.datetime.now()

    data = request.get_data(cache=True, as_text=True, parse_form_data=True)
    request_data = data.split(",")[1:]
    request_data = [request_data]

    print("New alert: ", request_data)

    dashboard.update_data(request_data)
    dashboard.update_google_sheets(alert_time)

    return data


if __name__ == "__main__":
    run_simple("localhost", 80, app)
