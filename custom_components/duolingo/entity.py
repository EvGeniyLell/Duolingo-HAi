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
    DOMAIN, VERSION,
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
        self.coordinator.async_add_listener(self._handle_coordinator_update)

    def _handle_coordinator_update(self) -> None:
        """Clear the cached user_dto property."""
        if "user_dto" in self.__dict__:
            del self.__dict__["user_dto"]

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
            model=f"EI_DUO_{VERSION}_HAi",
            manufacturer=NAME,
            entry_type=DeviceEntryType.SERVICE,
        )
