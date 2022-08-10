"""Dashboard constants."""


GOOGLE_KEY = {
    "type": "service_account",
    "project_id": "hazel-freehold-344516",
    "private_key_id": "a7ffa925a68d408c387e2fd844e406fe28751dbb",
    "private_key": "-----BEGIN PRIVATE KEY-----\n"
                   "MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDZnghQcWJRRCa+\n"
                   "JWF5QyL5qujyD0dvWmDnt13gjKg0YmRm29kpg8DE/mHX9C04FmrT0qajMgxe+0+y\n"
                   "sdRm32XF68DycaoHf4V1DkofZXCo4RgNQmLLCd1XoQGAUa1t5vI8pFhyvAkydmHB\n"
                   "rXgwm+mPgx0ehL3btEFMuc1BKsKddgrq00eDqBzbqghXu3RZxN9kYESB/4031vHy\n"
                   "wPySKlIYGSzn4+zDgwPloRzDmYhTi/k6l2XVxWAzLKwYZ7XM9jHWI/Wa8KxriWMf\n"
                   "dn6hYb8bKFALhdmR0sDggyQNSItsHXzyuu+yZ+5vZ95uClaDDT53iecAxF6Wkr0F\n"
                   "8ntQaKKLAgMBAAECggEAFjXfvFzDf5mDPhnw7Qrx9BBtA7OVLg4dNi52tDc26Fh4\n"
                   "eIUMu4TOdRdPeNaGPPi7a3t5oCNjXthV0Ij/gtu0dp2yt4FBV3rnmJmzl/5m9V2P\n"
                   "8l5/AyEHyGykNhVgAYe2MS6cNmLu/17/aDXiaUz9wAojkTH+x1XflPX2YdB8RMy6\n"
                   "Gdj9lMq0pJohtKFMaliL4+2y8d278YPoG+VTDJj514NUavc7SWX78zewRuSsLKPh\n"
                   "SfeyRXWO+yxXwx6q5hOx6Ucvpl4qFvlAIsxdDLQ6SJpIADis2TVSbNOOnpNLhAkX\n"
                   "vdM0I91cjpONyxUOqYPmb4DW7MaObuUOMeDz2soRnQKBgQDtivDCGRnG2cz9Hs9a\n"
                   "dOq5mi4CP9LA5+RpoVUmH+vB/ogKIbdhX1IN1XEeyxEahakBBueyghRKDBrFAH95\n"
                   "/5qd4nWnzjXsN2wv83SZVAc45zZcaY6a5I9zZ3Opop21AVY1IhLiiL2/8jsc4kQh\n"
                   "cW+Hzi/ZZtFkaJymuY14A89f9wKBgQDqhr9QHfRzPGJ9Ns3qO4QOikPBGskV88eU\n"
                   "T7U4rR6iCziJfkQ9CSSNya1pfRRqTziLMbdBsG7ggSbNVlbNh2+r7KXRBarUuaj/\n"
                   "6PqmGtrYygq9+WSlETZHRf4XeF2p2T3/lBKiznrandsCrLNueaOVefQFT5ef/4FG\n"
                   "d5lPXqqVDQKBgQDP/s3rlyD7/nBA3z5/HUr+s6M/svTult5pI6w0UtUTq7Ug8f7p\n"
                   "kxZ9KH0BkpvqVkjyrkIpCz+KyuiRwWrdv1N6lfWhtq1+pdTkc8+QBoTAbawq5P7K\n"
                   "YAG/8kDTs6FWAdKjea+Bjmxf61GZbAJuKi6XgpJhUWdd/T/VuTnHccaeZwKBgQCm\n"
                   "OfmRnJmtr8gS/ew3MBXqhF9/mC+cqpvz6AcHc9T5f8CD24YcSMWq5Z5O3YPB0gK+\n"
                   "ze8Y1SfRYlkRQzflFzC0h9gDbePmQO2i7Qvy/afN7m5stj56rNdu7xIoqnygrUS/\n"
                   "SMFoubbkCuy3WZcYH4ktojGuLfrHQb7sJkr4sZ1wZQKBgHRyvBCxJkvyTBjQck1b\n"
                   "T+8Z4j1rSKh9u8k7XjA6J907RmmU0vtSKqWh2FQ2/1IlNloF57Nl6FWN1yWgXCbP\n"
                   "FNoAYjusFfpNpY5nEkPnRX5eQYe/mSK5J7S4gnTD5uUZu0HiHsxm295zuLurjw3j\n"
                   "aFzqM9uVl+JzUKMoT/YmnVSp\n"
                   "-----END PRIVATE KEY-----\n",
    "client_email": "trader-viewer@hazel-freehold-344516.iam.gserviceaccount.com",
    "client_id": "115495437317317039318",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot"
                            "/v1/metadata/x509/trader-viewer%40hazel-freehold-344516.iam.gserviceaccount.com"
}

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
