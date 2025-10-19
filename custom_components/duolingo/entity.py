"""DuolingoEntity class."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)
from propcache import cached_property

from custom_components.duolingo.dto import UserDto


class DuolingoEntity(CoordinatorEntity):
    """Base entity for Duolingo integration."""

    def __init__(
            self,
            coordinator: DataUpdateCoordinator,
            config_entry: ConfigEntry,
    ) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)
        self.config_entry = config_entry

    @cached_property
    def user_dto(self) -> UserDto:
        """Convert coordinator data to UserDto."""
        return UserDto.from_ha(self.coordinator.data)

    @property
    def unique_id(self) -> str:
        """Return a unique ID to use for this entity."""
        return self.config_entry.entry_id

    # @property
    # def _username(self) -> str:
    #     """Return the username of the Duolingo account."""
    #     return self.coordinator.data.get("username", "")
    #
    # @property
    # def _streak_extended_today(self) -> bool:
    #     """Return true if the streak extended today."""
    #     return self.coordinator.data.get("streak_extended_today", False)
    #
    # @property
    # def _site_streak(self) -> int:
    #     """Return the number of days of site streak."""
    #     return self.coordinator.data.get("site_streak", 0)
    #
    # @property
    # def _total_xp(self) -> int:
    #     """Return the number of days of site streak."""
    #     return self.coordinator.data.get("total_xp", 0)
    #
    # @property
    # def _courses(self) -> dict[str: int]:
    #     """Return the courses dict."""
    #     return self.coordinator.data.get("courses", [])
    #
    # def _course_xp(self, course_id: str) -> int:
    #     """Return the xp value for course id."""
    #     return self._courses.get(course_id, 0)
