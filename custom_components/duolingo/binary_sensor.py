"""Support for a Duolingo data sensor."""
import logging

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_ATTRIBUTION
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import DuolingoDataUpdateCoordinator
from .const import (
    DOMAIN, ATTR_DUO_DATA_PROVIDER, ATTR_DUO_STREAK_TODAY,
    ATTR_DUO_STREAK_LENGTH,
)
from .entity import DuolingoEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
        hass: HomeAssistant,
        entry: ConfigEntry,
        async_add_devices: AddEntitiesCallback,
) -> None:
    """Set up binary_sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    if not isinstance(coordinator, DuolingoDataUpdateCoordinator):
        _LOGGER.error(
            "Coordinator is not of type DuolingoDataUpdateCoordinator"
        )
        return

    async_add_devices([DuolingoStreakTodaySensor(coordinator, entry)])


class DuolingoStreakTodaySensor(DuolingoEntity, BinarySensorEntity):
    """Implementation of the Duolingo binary sensor."""

    @property
    def name(self) -> str:
        """Return the name of the binary_sensor."""
        return self.translation_sensors("streak_today", {
            "name": self.user_dto.name,
        })

    @property
    def unique_id(self) -> str:
        """Return a unique ID to use for this entity."""
        return f"{super().unique_id}_streak_today"

    @property
    def is_on(self) -> bool:
        """Return true if the binary sensor is on."""
        return self.user_dto.streak_today

    @property
    def icon(self) -> str:
        """Return the icon to use in the frontend."""
        return "mdi:fire"

    @property
    def extra_state_attributes(self) -> dict[str, object]:
        """Return the state attributes."""
        return {
            ATTR_ATTRIBUTION: ATTR_DUO_DATA_PROVIDER,
            ATTR_DUO_STREAK_TODAY: self.user_dto.streak_today,
            ATTR_DUO_STREAK_LENGTH: self.user_dto.streak_length,
        }
