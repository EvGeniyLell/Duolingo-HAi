"""Support for Duolingo streak sensors."""
import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_ATTRIBUTION
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from propcache import cached_property

from . import DuolingoDataUpdateCoordinator
from .const import (
    DOMAIN, ATTR_DUO_DATA_PROVIDER, ATTR_DUO_USERNAME, ATTR_DUO_COURSE_ID,
    ATTR_DUO_NAME,
)
from .dto import UserDto
from .entity import DuolingoEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
        hass: HomeAssistant,
        entry: ConfigEntry,
        async_add_devices: AddEntitiesCallback,
) -> None:
    """Set up sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    if not isinstance(coordinator, DuolingoDataUpdateCoordinator):
        _LOGGER.error(
            "Coordinator is not of type DuolingoDataUpdateCoordinator"
        )
        return

    sensors: list[SensorEntity] = [
        DuolingoStreakLengthSensor(coordinator, entry),
        DuolingoTotalXPSensor(coordinator, entry),
    ]

    user_dto = UserDto.from_ha(coordinator.data)
    for course_id in user_dto.courses_xp.keys():
        sensors.append(
            DuolingoCourseXPSensor(coordinator, entry, course_id)
        )

    async_add_devices(sensors)


class DuolingoStreakLengthSensor(DuolingoEntity, SensorEntity):
    """Implementation of the Duolingo Streak Length sensor."""

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return f"{super().name} Streak Length"

    @cached_property
    def unique_id(self) -> str:
        """Return a unique ID to use for this entity."""
        return f"{super().unique_id}_streak_length"

    @property
    def native_value(self) -> int:
        """Return the state of the sensor."""
        return self.user_dto.streak_length

    @property
    def native_unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return "days"

    @property
    def icon(self) -> str:
        """Return the icon to use in the frontend."""
        return "mdi:calendar"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        return {
            ATTR_ATTRIBUTION: ATTR_DUO_DATA_PROVIDER,
            ATTR_DUO_USERNAME: self.user_dto.username,
        }


class DuolingoTotalXPSensor(DuolingoEntity, SensorEntity):
    """Implementation of the Duolingo Total XP sensor."""

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return f"{super().name} XP"

    @property
    def unique_id(self) -> str:
        """Return a unique ID to use for this entity."""
        return f"{super().unique_id}_xp"

    @property
    def native_value(self) -> int:
        """Return the state of the sensor."""
        return self.user_dto.total_xp

    @property
    def native_unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return "XP"

    @property
    def icon(self) -> str:
        """Return the icon to use in the frontend."""
        return "mdi:star"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        return {
            ATTR_ATTRIBUTION: ATTR_DUO_DATA_PROVIDER,
            ATTR_DUO_USERNAME: self.user_dto.username,
        }


class DuolingoCourseXPSensor(DuolingoEntity, SensorEntity):
    """Implementation of the Duolingo Course XP sensor."""

    def __init__(self, coordinator, config_entry, course_id: str):
        super().__init__(coordinator, config_entry)
        self.course_id = course_id

    @property
    def course_name(self) -> str:
        """Return the translated course name."""
        return f"{self.course_id}"

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return f"{super().name} {self.course_name} XP"

    @property
    def unique_id(self) -> str:
        """Return a unique ID to use for this entity."""
        return f"{super().unique_id}_{self.course_id}_xp"

    @property
    def native_value(self) -> int:
        """Return the state of the sensor."""
        return self.user_dto.courses_xp.get(self.course_id, 0)

    @property
    def native_unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return "XP"

    @property
    def icon(self) -> str:
        """Return the icon to use in the frontend."""
        return "mdi:star"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        return {
            ATTR_ATTRIBUTION: ATTR_DUO_DATA_PROVIDER,
            ATTR_DUO_NAME: self.user_dto.name,
            ATTR_DUO_USERNAME: self.user_dto.username,
            ATTR_DUO_COURSE_ID: self.course_id,
        }
