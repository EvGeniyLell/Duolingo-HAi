"""Constants for Duolingo."""

JWT_TOKEN = "jwt_token"

# Base component constants
NAME = "Duolingo Observer"
DOMAIN = "duolingo"
VERSION = "0.1.2"

ISSUE_URL = "https://github.com/EvGeniyLell/Duolingo-HAi/issues"

# Platforms
BINARY_SENSOR = "binary_sensor"
SENSOR = "sensor"
PLATFORMS = [BINARY_SENSOR, SENSOR]

# Attribution - extra_state_attributes
ATTR_DUO_STREAK_LENGTH = "streak_length"
ATTR_DUO_STREAK_TODAY = "streak_today"
ATTR_DUO_NAME = "name"
ATTR_DUO_USERNAME = "username"
ATTR_DUO_COURSE_ID = "course_id"
ATTR_DUO_XP_YESTERDAY = "xp_yesterday"
ATTR_DUO_XP_TODAY_GAIN = "xp_today_gain"

# Config Entry Data
CONFIG_ENTRY_XP_SNAPSHOT_KEY = "xp_snapshot"
CONFIG_ENTRY_SNAPSHOT_DATE_KEY = "snapshot_date"


STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""
