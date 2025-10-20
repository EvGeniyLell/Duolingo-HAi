"""Constants for Duolingo."""

# Base component constants
NAME = "Duolingo Observer"
DOMAIN = "duolingo"
VERSION = "0.1.0"

ISSUE_URL = "https://github.com/EvGeniyLell/Duolingo-HAi/issues"

# Platforms
BINARY_SENSOR = "binary_sensor"
SENSOR = "sensor"
PLATFORMS = [BINARY_SENSOR, SENSOR]

# Configuration and options
CONF_USERNAME = "username"

# Attribution - extra_state_attributes
ATTR_DUO_DATA_PROVIDER = "Data provided by Duolingo"
ATTR_DUO_STREAK_LENGTH = "Streak length days"
ATTR_DUO_STREAK_TODAY = "Streak extended today"
ATTR_DUO_USERNAME = "Username"
ATTR_DUO_COURSE_ID = "Course ID"

STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""
