"""DuolingoEntity class."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import (
    DeviceEntryType,
    DeviceInfo,
)
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)
from propcache import cached_property

from .const import (
    NAME,
    DOMAIN,
)
from .dto import UserDto


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

    @cached_property
    def device_name(self) -> str:
        """Return a raw ID of this entity."""
        return f"{DOMAIN}_{self.user_dto.username}"

    @cached_property
    def unique_id(self) -> str:
        """Return a unique ID to use for this entity."""
        return self.config_entry.entry_id

    @cached_property
    def device_info(self) -> DeviceInfo:
        """Return device information about this entity."""
        return DeviceInfo(
            name=self.device_name,
            identifiers={(DOMAIN, self.user_dto.username)},
            manufacturer=NAME,
            entry_type=DeviceEntryType.SERVICE,
        )
