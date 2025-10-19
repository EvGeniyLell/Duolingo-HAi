"""Support for Duolingo streak sensors."""

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_ATTRIBUTION
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.duolingo.entity import DuolingoEntity
from .const import (
    DOMAIN, ATTR_DUO_DATA_PROVIDER, ATTR_DUO_USERNAME, ATTR_DUO_COURSE_ID,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
        hass: HomeAssistant,
        entry: ConfigEntry,
        async_add_devices: AddEntitiesCallback,
) -> None:
    """Set up sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    sensors: list[SensorEntity] = [
        DuolingoStreakLengthSensor(coordinator, entry),
        DuolingoXPSensor(coordinator, entry),
    ]

    courses = coordinator.data.get("courses", [])
    for course in courses:
        sensors.append(
            DuolingoCourseXPSensor(coordinator, entry, course["id"])
        )

    async_add_devices(sensors)


class DuolingoStreakLengthSensor(DuolingoEntity, SensorEntity):
    """Implementation of the Duolingo streak sensor."""

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return f"{DOMAIN}_{self.user_dto.username}_streak_length"

    @property
    def unique_id(self) -> str:
        """Return a unique ID to use for this entity."""
        return f"{DOMAIN}_{self.user_dto.username}_streak_length"

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


class DuolingoXPSensor(DuolingoEntity, SensorEntity):
    """Implementation of the Duolingo XP sensor."""

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return f"{DOMAIN}_{self.user_dto.username}_xp"

    @property
    def unique_id(self) -> str:
        """Return a unique ID to use for this entity."""
        return f"{DOMAIN}_{self.user_dto.username}_xp"

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
        self._course_id = course_id

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return f"{DOMAIN}_{self.user_dto.username}_{self._course_id}_xp"

    @property
    def unique_id(self) -> str:
        """Return a unique ID to use for this entity."""
        return f"{DOMAIN}_{self.user_dto.username}_{self._course_id}_xp"

    @property
    def native_value(self) -> int:
        """Return the state of the sensor."""
        return self.user_dto.courses_xp.get(self._course_id, 0)

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
            ATTR_DUO_COURSE_ID: self._course_id,
        }
