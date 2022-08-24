"""Module Dashboard."""
import datetime
import itertools
import os
from copy import deepcopy

import bson
import gspread
import pandas as pd
from dateutil.relativedelta import relativedelta

from .constants import (PATTERN_SCORES, PATTERNS, REPRESENT_PATTERNS, TICKERS,
                        TIMEFRAME_EXPIRATION)

PRIMARY_SHEET_ID = 0
SECONDARY_SHEET_ID = 1
GOOGLE_SHEET_NAME = "trade_dashb_ngrok"


class Dashboard:
    """Google Sheets Dashboard."""

    def __init__(self, google_key_path, saved_state_path):
        """Creates connection to GS and initializes data."""
        self.saved_state_path = saved_state_path

        self.connect_to_google_sheet(google_key_path=google_key_path)
        self.load()

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

    def load(self):
        # creating tickers sample
        if os.path.exists(self.saved_state_path):
            with open(self.saved_state_path, "rb") as state_file:
                self.data = bson.BSON(state_file.read()).decode()
            return

        self.data = {
            "dashboard": {
                ticker: {
                    timeframe: {
                        pattern: 0
                        for pattern in PATTERNS
                    }
                    for timeframe in TIMEFRAME_EXPIRATION
                }
                for ticker in TICKERS
            },
            "dashboard_timer": {
                ticker: {
                    timeframe: {
                        pattern: datetime.datetime.now() + relativedelta(years=1)
                        for pattern in list(PATTERN_SCORES.keys())
                    }
                    for timeframe in TIMEFRAME_EXPIRATION
                } # Зачем нужен?
                for ticker in TICKERS
            },
            # this is for log of last time active signal ("BTCUSDT", "5", "Cross_dn")
            "all_combs": list(set(itertools.product(*[TICKERS, TIMEFRAME_EXPIRATION.keys(),
                                                      PATTERN_SCORES.keys()])))
        }


    def save(self):
        with open(self.saved_state_path, "wb") as state_file:
            state_file.write(bson.BSON.encode(self.data))


    def update_data(self, new_data):
        """Sets new data to the dashboard."""
        # Берет тикер монеты, время, поведение монеты - три элемента
        for ticker, timeframe, pattern in new_data:

            self.data["dashboard_timer"][ticker][timeframe][pattern] = datetime.datetime.now()

            key = pattern

            # Этот блок берет паттерн типа "AI_r", AI_ri_up, "AI_ri_dn" - и задает проверку и заполняет DashBoard
            if "AI_r" in str(pattern):
                key = f"AI_ri_{pattern.split('_')[-1]}"
            if "Cross" in str(pattern):
                key = "Cross"
            if "Cross_s" in str(pattern):
                key = "Cross_s" #+ pattern.split("_")[-1]

            print(f"filling {key}")
            print(pattern.split("_")[-1])

            row_id = self.data["dashboard"][ticker][timeframe]
            row_id[key] = pattern
            row_id[f"score_{pattern.split('_')[-1]}_points"] += PATTERN_SCORES[pattern]
            row_id["score_gen_points"] += PATTERN_SCORES[pattern]

        self.save()


    def _remove_expired_indicators(self, alert_time):  # current_time
        def update_time(d, tc, tf, pt):

            d[tc][tf][pt] = datetime.datetime.now() + relativedelta(years=1)

        def update_score(d, tc, tf, pt):

            pattern = deepcopy(pt)

            if "AI_r" in str(pt):
                pattern = f"AI_ri_{pt.split('_')[-1]}"

            if "Cross" in str(pt):
                pattern = "Cross"

            if "Cross_s" in str(pt):
                pattern = f"Cross_s_{pt.split('_')[-1]}"

            d[tc][tf][pattern] = 0
            d[tc][tf]["score_up_points"] -= PATTERN_SCORES[pt]
            d[tc][tf]["score_dn_points"] -= PATTERN_SCORES[pt]
            d[tc][tf]["score_gen_points"] = d[tc][tf]["score_up_points"] + d[tc][tf]["score_dn_points"]

            print(f"Substracted {pattern}.")

        # 1 важен порядок, сначала обновляем время
        # 2. временной фиксатор содержит информацию о всех паттернах, просто дашборд содержит
        # удобное визуальное представление
        for tc, tf, pt in self.data["all_combs"]:
            if (alert_time - self.data["dashboard_timer"][tc][tf][pt]).total_seconds() / 60 > TIMEFRAME_EXPIRATION[tf]:
                update_time(self.data["dashboard_timer"], tc, tf, pt)
                update_score(self.data["dashboard"], tc, tf, pt)

        self.save()


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
        self._remove_expired_indicators(alert_time)

        dashboard_df = pd.DataFrame.from_dict(self.data["dashboard"], orient="index")

        dashboard_df = pd.DataFrame.from_dict({(i,j): val_j for i, val_i in dashboard_df.items()
                                                            for j, val_j in val_i.items()},
                                              orient="index")

        dashboard_df = dashboard_df.reset_index().reset_index().rename(columns={"level_0": "frequency",
                                                                                "level_1": "ticker_name"})

        self._push_to_google_sheets(dashboard_df)
