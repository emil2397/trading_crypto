"""Module Dashboard."""
import datetime
import itertools
import os

import bson
import gspread
import pandas as pd
from dateutil.relativedelta import relativedelta

from .constants import (PATTERN_SCORES, PATTERNS, REPRESENT_PATTERNS, TICKERS,
                        TIMEFRAME_EXPIRATION)


class Dashboard:
    """Google Sheets Dashboard."""

    def __init__(self,
                 google_key_path,
                 saved_state_path,
                 google_sheet_name,
                 primary_sheet_id,
                 secondary_sheet_id):
        """Creates connection to GS and initializes data."""
        self.saved_state_path = saved_state_path

        self.connect_to_google_sheet(google_key_path=google_key_path,
                                     google_sheet_name=google_sheet_name,
                                     primary_sheet_id=primary_sheet_id,
                                     secondary_sheet_id=secondary_sheet_id)
        self.load()

    def connect_to_google_sheet(self,
                                google_key_path,
                                google_sheet_name,
                                primary_sheet_id,
                                secondary_sheet_id):
        """Connects to GS using gspread."""
        creds = gspread.service_account(filename=google_key_path)
        sh = creds.open(google_sheet_name)

        self._primary_worksheet = sh.get_worksheet(primary_sheet_id)
        self._secondary_worksheet = sh.get_worksheet(secondary_sheet_id)

    def load(self):
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
            "all_combs": list(set(itertools.product(TICKERS, TIMEFRAME_EXPIRATION.keys(),
                                                    PATTERN_SCORES.keys())))
        }

    def save(self):
        with open(self.saved_state_path, "wb") as state_file:
            state_file.write(bson.BSON.encode(self.data))

    def _pattern_to_column_name(self, pattern):
        column_name = pattern

        if "AI_r" in str(pattern):
            column_name = f"AI_ri_{pattern.split('_')[-1]}"
        if "Cross" in str(pattern):
            column_name = "Cross"
        if "Cross_s" in str(pattern):
            column_name = "Cross_s"

        return column_name

    def update_data(self, new_data):
        """Sets new data to the dashboard."""
        current_time = datetime.datetime.now()

        for ticker, timeframe, pattern in new_data:
            saved_time = self.data["dashboard_timer"][ticker][timeframe][pattern]

            self.data["dashboard_timer"][ticker][timeframe][pattern] = current_time

            column_name = self._pattern_to_column_name(pattern)

            row = self.data["dashboard"][ticker][timeframe]
            row[column_name] = pattern

            if saved_time < current_time:
                continue

            row[f"score_{pattern.split('_')[-1]}_points"] += PATTERN_SCORES[pattern]
            row["score_gen_points"] += PATTERN_SCORES[pattern]

            print(f"Added {ticker} {pattern}.")

        self._remove_expired_indicators(current_time)
        self.save()

    def reset_time(self, ticker, timeframe, pattern):
        self.data["dashboard_timer"][ticker][timeframe][pattern] = datetime.datetime.now() + relativedelta(years=1)

    def reset_score(self, ticker, timeframe, pattern):
        column_name = self._pattern_to_column_name(pattern)

        row = self.data["dashboard"][ticker][timeframe]

        row[column_name] = 0
        row[f"score_{pattern.split('_')[-1]}_points"] -= PATTERN_SCORES[pattern]
        row["score_gen_points"] -= PATTERN_SCORES[pattern]

        print(f"Substracted {ticker} {pattern}.")

    def _remove_expired_indicators(self, alert_time):  # current_time
        # 1 важен порядок, сначала обновляем время
        # 2. временной фиксатор содержит информацию о всех паттернах, просто дашборд содержит
        # удобное визуальное представление
        for ticker, timeframe, pattern in self.data["all_combs"]:
            saved_time = self.data["dashboard_timer"][ticker][timeframe][pattern]
            if (alert_time - saved_time).total_seconds() / 60 > TIMEFRAME_EXPIRATION[timeframe]:
                self.reset_time(ticker, timeframe, pattern)
                self.reset_score(ticker, timeframe, pattern)

        self.save()

    def _push_to_google_sheets(self, dashboard_df):
        self._primary_worksheet.update([dashboard_df[REPRESENT_PATTERNS].columns.values.tolist()] +
                                       dashboard_df[REPRESENT_PATTERNS].sort_values(by="ticker_name",
                                                                                    ascending=False).values.tolist())

        self._secondary_worksheet.update([dashboard_df[REPRESENT_PATTERNS].columns.values.tolist()] +
                                         dashboard_df[REPRESENT_PATTERNS].sort_values(by=["score_gen_points",
                                                                                          "ticker_name"],
                                                                                      ascending=False).values.tolist())

    def update_google_sheets(self):
        #https://stackoverflow.com/questions/3232943/update-value-of-a-nested-dictionary-of-varying-depth
        dashboard_df = pd.DataFrame.from_dict(self.data["dashboard"], orient="index")

        dashboard_df = pd.DataFrame.from_dict({(i,j): val_j for i, val_i in dashboard_df.items()
                                                            for j, val_j in val_i.items()},
                                              orient="index")

        dashboard_df = dashboard_df.reset_index().reset_index().rename(columns={"level_0": "frequency",
                                                                                "level_1": "ticker_name"})

        self._push_to_google_sheets(dashboard_df)
