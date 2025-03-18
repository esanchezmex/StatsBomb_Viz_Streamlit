"""
Configuration settings for the Footy Analytics Dashboard.
"""
from pathlib import Path

# Base URLs for Statsbomb API
STATSBOMB_OPEN_DATA_URL = "https://raw.githubusercontent.com/statsbomb/open-data/master/data"
COMPETITIONS_URL = f"{STATSBOMB_OPEN_DATA_URL}/competitions.json"
MATCHES_URL_TEMPLATE = f"{STATSBOMB_OPEN_DATA_URL}/matches/{{competition_id}}/{{season_id}}.json"
EVENTS_URL_TEMPLATE = f"{STATSBOMB_OPEN_DATA_URL}/events/{{match_id}}.json"
LINEUPS_URL_TEMPLATE = f"{STATSBOMB_OPEN_DATA_URL}/lineups/{{match_id}}.json"

# Cache settings
CACHE_DIR = Path("cache")
CACHE_EXPIRY = 3600  # Cache expiry in seconds (1 hour)

# Logging settings
LOG_FILE = "app.log"
LOG_LEVEL = "INFO"

# Data validation settings
MAX_RETRIES = 3
TIMEOUT = 10  # seconds

# Visualization settings
PLOT_HEIGHT = 600
PLOT_WIDTH = 800
DEFAULT_THEME = "streamlit"

# Session state keys
SESSION_KEYS = {
    "competition": "selected_competition",
    "season": "selected_season",
    "team": "selected_team",
    "player": "selected_player",
    "event": "selected_event"
} 