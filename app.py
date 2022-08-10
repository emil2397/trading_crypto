"""Main Flask script."""
import datetime
import warnings

from flask import Flask, request
from werkzeug.serving import run_simple

from funds.dashboard import Dashboard

warnings.filterwarnings("ignore")


dashboard = Dashboard()
app = Flask(__name__)


@app.route("/", methods=["POST"])
def hello():
    """Runs full pipeline."""
    data = request.get_data(cache=True, as_text=True, parse_form_data=True)
    now_date = datetime.datetime.now()
    request_data = data.split(",")[1:]
    def final(request_data):
        request_data = [request_data]
        print("New alert: ", request_data)
        dashboard.fill_dashboard(request_data)
        dashboard.post_to_gs(now_date)
    final(request_data)
    return data


if __name__ == "__main__":
    run_simple("localhost", 80, app)
#   app.run(host="0.0.0.0", port=80)

# https://docs.google.com/spreadsheets/d/1Qi0GCCCTr2NBMbw9poXRsdWbywQGGosXOiqoDDn_i0w/edit#gid=0
# user = "trading.view.alerts777@gmail.com"
# pwd = "syvxuc-vivxYq-2kuhfa"
