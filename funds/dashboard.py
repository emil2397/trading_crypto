"""Module Dashboard."""
import datetime
import itertools
import json
import warnings
from copy import deepcopy

import gspread
import pandas as pd
from dateutil.relativedelta import relativedelta

from .constants import (GOOGLE_KEY, PATTERN_SCORES, PATTERNS,
                        REPRESENT_PATTERNS, TICKERS, TIMEFRAME_EXPIRATION)

warnings.filterwarnings("ignore")


# now_date = datetime.datetime.now().strftime("%d %b %Y %X")
# now_date = datetime.datetime.strptime(now_date, "%d %b %Y %X")


class Dashboard:
    """Google Sheets Dashboard."""
    def __init__(self):
        """Creates connection to GS and initializes data."""
        self.connect_to_google_sheet()
        self.create_data()


    def connect_to_google_sheet(self):
        """Connects to GS using gspread."""
        with open("./local_data/google_key.json", "w", encoding="utf-8") as outfile:
            json.dump(GOOGLE_KEY, outfile)

        creds = gspread.service_account(filename="./local_data/google_key.json")
        sh = creds.open("trade_dashb_ngrok")

        self._primary_worksheet = sh.get_worksheet(0)
        self._secondary_worksheet = sh.get_worksheet(1)


    def create_data(self):
        # creating tickers sample
        self._dashboard = {
            ticker: {
                timeframe: {
                    pattern: 0
                    for pattern in PATTERNS
                }
                # for timeframe in TIMEFRAME_EXPIRATION.keys()
                for timeframe in TIMEFRAME_EXPIRATION
            }
            for ticker in TICKERS
        }

        # self._dashboard_timer = create_dashbord_timer()
        self._dashboard_timer = {
            ticker: {
                timeframe: {
                    pattern: datetime.datetime.now() + relativedelta(years=1)
                    for pattern in list(PATTERN_SCORES.keys())
                }
                # for timeframe in TIMEFRAME_EXPIRATION.keys()
                for timeframe in TIMEFRAME_EXPIRATION
            } # Зачем нужен?
            for ticker in TICKERS
        }

        # that is for log of last time active signal ("BTCUSDT", "5", "Cross_dn")
        # self._all_combs = list(set(itertools.product(*[TICKERS, TIMEFRAME_EXPIRATION.keys(),
        #                                                list(PATTERN_SCORES.keys())])))
        self._all_combs = list(set(itertools.product(*[TICKERS, TIMEFRAME_EXPIRATION.keys(),
                                                       PATTERN_SCORES.keys()])))


    def fill_dashboard(self, new_data):
        """Sets new data to the dashboard."""
        # Берет тикер монеты, время, поведение монеты - три элемента
        for ticker, timeframe, pattern in new_data:

            self._dashboard_timer[ticker][timeframe][pattern] = datetime.datetime.now()

            key = pattern

            # Этот блок берет паттерн типа "AI_r", AI_ri_up, "AI_ri_dn" - и задает проверку и заполняет DashBoard
            # if str(pattern).__contains__("AI_r"):
            if "AI_r" in str(pattern):
                key = "AI_ri_" + pattern.split("_")[-1]
            # if str(pattern).__contains__("Cross"):
            if "Cross" in str(pattern):
                key = "Cross"
            # if str(pattern).__contains__("Cross_s"):
            if "Cross_s" in str(pattern):
                key = "Cross_s" #+ pattern.split("_")[-1]

            print(f"filling {key}")
            print(pattern.split("_")[-1])

            self._dashboard[ticker][timeframe][key] = pattern
            self._dashboard[ticker][timeframe]["score_" + pattern.split("_")[-1] + "_points"] += PATTERN_SCORES[pattern]
    # self._dashboard[ticker][timeframe]["score_gen_points"] = self._dashboard[ticker][timeframe]["score_up_points"] + \
    #                                                          self._dashboard[ticker][timeframe]["score_dn_points"]
            self._dashboard[ticker][timeframe]["score_gen_points"] += PATTERN_SCORES[pattern]


    def post_to_gs(self, now_date):
        def post_to_google_sheets(dashboard_df):

            self._primary_worksheet.update([dashboard_df[REPRESENT_PATTERNS].columns.values.tolist()] +
                               dashboard_df[REPRESENT_PATTERNS].sort_values(by="ticker_name",
                                                                            ascending=False).values.tolist())

            self._secondary_worksheet.update([dashboard_df[REPRESENT_PATTERNS].columns.values.tolist()] +
                                dashboard_df[REPRESENT_PATTERNS].sort_values(by=["score_gen_points", "ticker_name"],
                                                                             ascending=False).values.tolist())
            print("Add it to Google sheets")


        #https://stackoverflow.com/questions/3232943/update-value-of-a-nested-dictionary-of-varying-depth

        def find_expired_indicators(now_date): # now_date

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

                print(f"substracting {pattern}")

                d[tc][tf][pattern] = 0
                d[tc][tf]["score_up_points"] -= PATTERN_SCORES[pt]
                d[tc][tf]["score_dn_points"] -= PATTERN_SCORES[pt]
                d[tc][tf]["score_gen_points"] = d[tc][tf]["score_up_points"] + d[tc][tf]["score_dn_points"]

            # 1 важен порядок, сначала обновляем время
            # 2. временной фиксатор содержит информацию о всех паттернах, просто дашборд содержит
            # удобное визуальное представление

            # [

            # (update_time(self._dashboard_timer, tc, tf, pt),
            # update_score(self._dashboard, tc, tf, pt)
            # )

            # for tc, tf, pt in self._all_combs

            # if (now_date - self._dashboard_timer[tc][tf][pt]).total_seconds() / 60
            # > TIMEFRAME_EXPIRATION[tf]

            # ]
            for tc, tf, pt in self._all_combs:
                if (now_date - self._dashboard_timer[tc][tf][pt]).total_seconds() / 60 > TIMEFRAME_EXPIRATION[tf]:
                    update_time(self._dashboard_timer, tc, tf, pt)
                    update_score(self._dashboard, tc, tf, pt)

        find_expired_indicators(now_date)

        dashboard_df = pd.DataFrame.from_dict(self._dashboard, orient="index")

        # dashboard_df = pd.DataFrame.from_dict({(i,j): dashboard_df[i][j]
        #                                                   for i in dashboard_df.keys()
        #                                                   for j in dashboard_df[i].keys()},
        #                                       orient="index")
        dashboard_df = pd.DataFrame.from_dict({(i,j): val_j for i, val_i in dashboard_df.items()
                                                            for j, val_j in val_i.items()},
                                              orient="index")

        dashboard_df = dashboard_df.reset_index().reset_index().rename(columns={"level_0":
                                                            "frequency","level_1":"ticker_name"})

        post_to_google_sheets(dashboard_df)
