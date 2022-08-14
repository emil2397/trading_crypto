"""Module Dashboard."""
import datetime
import itertools
from copy import deepcopy

import gspread
import pandas as pd
from dateutil.relativedelta import relativedelta

from .constants import (PATTERN_SCORES, PATTERNS, REPRESENT_PATTERNS, TICKERS,
                        TIMEFRAME_EXPIRATION)

GOOGLE_KEY_PATH = "./local_data/google_key.json"
PRIMARY_SHEET_ID = 0
SECONDARY_SHEET_ID = 1
GOOGLE_SHEET_NAME = "trade_dashb_ngrok"


class Dashboard:
    """Google Sheets Dashboard."""
    def __init__(self, google_key_path):
        """Creates connection to GS and initializes data."""
        self.connect_to_google_sheet(google_key_path=google_key_path)
        self.create_data()


    def connect_to_google_sheet(self,
                                google_key_path,
                                google_sheet_name=GOOGLE_SHEET_NAME,
                                primary_sheet_id=PRIMARY_SHEET_ID,
                                secondary_sheet_id=SECONDARY_SHEET_ID):
        """Connects to GS using gspread."""
        creds = gspread.service_account(filename=google_key_path)
        sh = creds.open(google_sheet_name)

        self._primary_worksheet = sh.get_worksheet(primary_sheet_id)
        self._secondary_worksheet = sh.get_worksheet(secondary_sheet_id)


    def create_data(self):
        # creating tickers sample
        self._dashboard = {
            ticker: {
                timeframe: {
                    pattern: 0
                    for pattern in PATTERNS
                }
                for timeframe in TIMEFRAME_EXPIRATION
            }
            for ticker in TICKERS
        }

        self._dashboard_timer = {
            ticker: {
                timeframe: {
                    pattern: datetime.datetime.now() + relativedelta(years=1)
                    for pattern in list(PATTERN_SCORES.keys())
                }
                for timeframe in TIMEFRAME_EXPIRATION
            } # Зачем нужен?
            for ticker in TICKERS
        }

        # this is for log of last time active signal ("BTCUSDT", "5", "Cross_dn")
        self._all_combs = list(set(itertools.product(*[TICKERS, TIMEFRAME_EXPIRATION.keys(),
                                                       PATTERN_SCORES.keys()])))


    def update_data(self, new_data):
        """Sets new data to the dashboard."""
        # Берет тикер монеты, время, поведение монеты - три элемента
        for ticker, timeframe, pattern in new_data:

            self._dashboard_timer[ticker][timeframe][pattern] = datetime.datetime.now()

            key = pattern

            # Этот блок берет паттерн типа "AI_r", AI_ri_up, "AI_ri_dn" - и задает проверку и заполняет DashBoard
            if "AI_r" in str(pattern):
                key = "AI_ri_" + pattern.split("_")[-1]
            if "Cross" in str(pattern):
                key = "Cross"
            if "Cross_s" in str(pattern):
                key = "Cross_s" #+ pattern.split("_")[-1]

            print(f"filling {key}")
            print(pattern.split("_")[-1])

            self._dashboard[ticker][timeframe][key] = pattern
            self._dashboard[ticker][timeframe]["score_" + pattern.split("_")[-1] + "_points"] += PATTERN_SCORES[pattern]
            self._dashboard[ticker][timeframe]["score_gen_points"] += PATTERN_SCORES[pattern]


    def _remove_expired_indicatore(self, alert_time):  # current_time
        def update_time(d, tc, tf, pt):

            d[tc][tf][pt] = datetime.datetime.now() + relativedelta(years=1)

        def update_score(d, tc, tf, pt):

            pattern = deepcopy(pt)

            if "AI_r" in str(pt):
                pattern = "AI_ri_" + pt.split("_")[-1]

            if "Cross" in str(pt):
                pattern = "Cross"

            if "Cross_s" in str(pt):
                pattern = "Cross_s_" + pt.split("_")[-1]

            d[tc][tf][pattern] = 0
            d[tc][tf]["score_up_points"] -= PATTERN_SCORES[pt]
            d[tc][tf]["score_dn_points"] -= PATTERN_SCORES[pt]
            d[tc][tf]["score_gen_points"] = d[tc][tf]["score_up_points"] + d[tc][tf]["score_dn_points"]

            print(f"Substracted {pattern}.")

        # 1 важен порядок, сначала обновляем время
        # 2. временной фиксатор содержит информацию о всех паттернах, просто дашборд содержит
        # удобное визуальное представление
        for tc, tf, pt in self._all_combs:
            if (alert_time - self._dashboard_timer[tc][tf][pt]).total_seconds() / 60 > TIMEFRAME_EXPIRATION[tf]:
                update_time(self._dashboard_timer, tc, tf, pt)
                update_score(self._dashboard, tc, tf, pt)


    def _push_to_google_sheets(self, dashboard_df):
        self._primary_worksheet.update([dashboard_df[REPRESENT_PATTERNS].columns.values.tolist()] +
                           dashboard_df[REPRESENT_PATTERNS].sort_values(by="ticker_name",
                                                                        ascending=False).values.tolist())

        self._secondary_worksheet.update([dashboard_df[REPRESENT_PATTERNS].columns.values.tolist()] +
                            dashboard_df[REPRESENT_PATTERNS].sort_values(by=["score_gen_points", "ticker_name"],
                                                                         ascending=False).values.tolist())
        print("Posted to Google sheets.")


    def update_google_sheets(self, alert_time):
        #https://stackoverflow.com/questions/3232943/update-value-of-a-nested-dictionary-of-varying-depth
        self._remove_expired_indicatore(alert_time)

        dashboard_df = pd.DataFrame.from_dict(self._dashboard, orient="index")

        dashboard_df = pd.DataFrame.from_dict({(i,j): val_j for i, val_i in dashboard_df.items()
                                                            for j, val_j in val_i.items()},
                                              orient="index")

        dashboard_df = dashboard_df.reset_index().reset_index().rename(columns={"level_0": "frequency",
                                                                                "level_1": "ticker_name"})

        self._push_to_google_sheets(dashboard_df)
