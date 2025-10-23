"""Duolingo API client."""
import logging
from datetime import datetime
from zoneinfo import ZoneInfo

import requests

from .dto import UserDto

_LOGGER = logging.getLogger(__name__)


class DuolingoApiClient:
    """Client for communicating with Duolingo API."""

    TIMEOUT: int = 10
    BASE_URL: str = "https://www.duolingo.com/2017-06-30"
    HEADERS: dict[str, str] = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/91.0.4472.124 Safari/537.36"
        )
    }

    @classmethod
    def get_user_id(cls, username: str) -> int | None:
        """Get user ID from username."""
        url = f"{cls.BASE_URL}/users?username={username}"

        response = requests.get(url, headers=cls.HEADERS, timeout=cls.TIMEOUT)
        response.raise_for_status()

        json_data = response.json()

        users = json_data.get("users", [])
        if not users:
            _LOGGER.error(f"No user found with username: {username}")
            return None

        user_data = users[0]
        return user_data.get("id")

    def __init__(self, user_id: int, timezone: str) -> None:
        """Duolingo API Client."""
        self._user_id = user_id
        self._timezone = timezone

    def get_user_data(self) -> dict[str, object]:
        """Get data for the configured user."""
        url = f"{self.BASE_URL}/users/{self._user_id}"

        response = requests.get(url, headers=self.HEADERS, timeout=self.TIMEOUT)
        response.raise_for_status()

        user_data = response.json()
        if user_data is None:
            msg = f"Failed to retrieve data for user: {self._user_id}"
            raise ValueError(msg)

        # Use Home Assistant's configured timezone
        # Duolingo API returns dates in user's timezone
        tz = ZoneInfo(self._timezone)
        today = datetime.now(tz)

        return _user_data_to_ha(user_data, today)


def _user_data_to_ha(data: dict, today: datetime) -> dict[str, object]:
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
        id=data.get("id", 0),
        name=data.get("name", ""),
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
