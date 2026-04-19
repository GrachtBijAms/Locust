# =============================================================
#  config/settings.py  –  Central configuration for load tests
# =============================================================

BASE_URL = "https://saucedemo.com"

# Credentials to cycle through during the run
USERS = [
    {"username": "standard_user",    "password": "secret_sauce"},
    {"username":"performance_glitch_user", "password":"secret_sauce"},
# {"username":"ss","password":"ss"}
]

# Think-time ranges (seconds) between steps – keeps traffic realistic
THINK_TIME_MIN = 1.0
THINK_TIME_MAX = 3.0

# Playwright browser options
HEADLESS = True
DEBUG_HEADLESS = False          # Set False to watch browsers during debug runs
SLOW_MO   = 0            # ms delay between Playwright actions (useful for debug)