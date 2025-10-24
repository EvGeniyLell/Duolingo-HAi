"""DuolingoEntity class."""
import logging
import re

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import (
    DeviceEntryType,
    DeviceInfo,
)
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)
from propcache import cached_property

from . import DuolingoDataUpdateCoordinator
from .const import (
    NAME,
    DOMAIN,
    VERSION,
)
from .dto import UserDto

_LOGGER = logging.getLogger(__name__)


class DuolingoEntity(CoordinatorEntity):
    """Base entity for Duolingo integration."""

    def __init__(
            self,
            coordinator: DuolingoDataUpdateCoordinator,
            config_entry: ConfigEntry,
    ) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)
        self.coordinator = coordinator
        self.config_entry = config_entry
        _LOGGER.debug("Setup new entry: %s", config_entry)

    def translation_sensors(
            self,
            alias: str,
            data: dict[str, str]
    ) -> str | None:
        """Return the translated string for course id."""
        full_key = f"component.{DOMAIN}.common.sensors.{alias}"
        t_string = self.coordinator.translations.get(full_key)
        if not t_string:
            _LOGGER.warning(f"Translation missing for key: {full_key}")
            return None

        for key, value in data.items():
            pattern = r"\{" + re.escape(key) + r"\}"
            t_string = re.sub(pattern, str(value), t_string)
        _LOGGER.debug(f"Translated string for {alias}: {t_string}")
        return t_string

    @property
    def user_dto(self) -> UserDto:
        """Return the UserDto associated with this entity."""
        return self.coordinator.user_dto

    @cached_property
    def name(self) -> str:
        """Return the name of the sensor."""
        return f"Duo {self.user_dto.name}"

    @cached_property
    def unique_id(self) -> str:
        """Return a unique ID to use for this entity."""
        return f"{DOMAIN}_{self.user_dto.username}"

    @cached_property
    def device_info(self) -> DeviceInfo:
        """Return device information about this entity."""
        return DeviceInfo(
            name=f"Duo {self.user_dto.username} Observer",
            identifiers={(DOMAIN, self.user_dto.username)},
            model=f"User Observer {VERSION}",
            manufacturer=NAME,
            entry_type=DeviceEntryType.SERVICE,
        )
