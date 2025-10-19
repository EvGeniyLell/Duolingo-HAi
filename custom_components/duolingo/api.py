"""Duolingo API client."""

import logging
from datetime import datetime
from typing import Any, Dict
from zoneinfo import ZoneInfo

import requests

from custom_components.duolingo.dto import UserDto

_LOGGER: logging.Logger = logging.getLogger(__package__)


class DuolingoApiClient:
    """Client for communicating with Duolingo API."""

    TIMEOUT: int = 10
    BASE_URL: str = "https://www.duolingo.com/2017-06-30"
    HEADERS: Dict[str, str] = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/91.0.4472.124 Safari/537.36"
        )
    }

    def __init__(self, username: str, timezone: str) -> None:
        """Duolingo API Client."""
        self._username = username
        self._timezone = timezone

    def get_user_data(self) -> dict[str, Any]:
        """Get data for the configured user."""
        url = f"{self.BASE_URL}/users?username={self._username}"

        response = requests.get(url, headers=self.HEADERS, timeout=self.TIMEOUT)
        response.raise_for_status()

        json_data = response.json()
        users = json_data.get("users", [])

        if not users:
            msg = f"No user found with username: {self._username}"
            raise ValueError(msg)

        user_data = users[0]
        if user_data is None:
            msg = f"Failed to retrieve data for user: {self._username}"
            raise ValueError(msg)

        # Use Home Assistant's configured timezone
        # Duolingo API returns dates in user's timezone
        tz = ZoneInfo(self._timezone)
        today = datetime.now(tz)

        return _user_data_to_ha(user_data, today)


def _user_data_to_ha(data: dict, today: datetime) -> dict[str, Any]:
    current_streak = data.get("streakData", {}).get("currentStreak")
    if current_streak:
        streak_today = (
                today.strftime("%Y-%m-%d") == current_streak.get("endDate", "")
        )
        streak_length = current_streak.get("length", 0)
    else:
        streak_today = False
        streak_length = 0

    dto = UserDto(
        username=data.get("username", ""),
        total_xp=data.get("totalXp", 0),
        courses_xp={
            c.get("id", ""): c.get("xp", 0)
            for c in data.get("courses", [])
            if c.get("id", "")  # Skip courses with empty IDs
        },
        streak_today=streak_today,
        streak_length=streak_length,
    )

    return dto.to_ha
