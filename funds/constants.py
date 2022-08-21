"""Dashboard constants."""


# need for define columns in GS, order is important
REPRESENT_PATTERNS = [
    "frequency",
    "ticker_name",
    "AI_ri_up",
    "AF_up",
    "AI_ri_dn",
    "AF_dn",
    "Cross",
    "Cross_s",
    "score_up_points",
    "score_dn_points",
    "score_gen_points",
]

PATTERNS = [
    "AF_up",
    "AF_dn",
    "AI_ri_dn",
    "AI_ri_up",
    "Cross",
    "Cross_s",
    "score_up_points",
    "score_dn_points",
    "score_gen_points",
]

# probabilities_patterns = {
#     "Cross_up": 0.9,
#     "Cross_dn": 0.9,
#     "AI_r2_dn": 0.1,
#     "AI_r1_dn": 0.2,
#     "AI_r0_dn": 0.7,
#     "AI_r2_up": 0.1,
#     "AI_r1_up": 0.2,
#     "AI_r0_up": 0.7,
# }

PATTERN_SCORES = {
    "Cross_up": 1,
    "Cross_dn": -1,
    "Cross_s_up":1,
    "Cross_s_dn":-1,
    "AI_r2_dn": -0.5,
    "AI_r1_dn": -1,
    "AI_r0_dn": -2,
    "AI_r2_up": 0.5,
    "AI_r1_up": 1,
    "AI_r0_up": 2,
    "AF_up":5,
    "AF_dn":-5
}

TICKERS = [
    # "US100",
    # "TSLA",
    # "FB",
    # "MSFT",
    # "GOOGL",
    # "MSTR",
    "BTCUSDT",
    "ETHUSDT"
    # "USDRUB"
]

# TIMEFRAME_EXPIRATION = {"60": 70, "30": 40, "15": 20, "5": 5, "1": 2}
TIMEFRAME_EXPIRATION = {"1440": 1440, "240": 1440, "60": 1440, "30": 60, "15": 60, "5":  60, "1": 60, "15S": 5}
