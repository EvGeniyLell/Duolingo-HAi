"""The Duolingo integration."""

import asyncio
import logging

import homeassistant.helpers.config_validation as cv
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .api import DuolingoApiClient
from .const import (
    DOMAIN, PLATFORMS,
    STARTUP_MESSAGE,
)
from .coordinator import DuolingoDataUpdateCoordinator
from .dto import UserDto

_LOGGER: logging.Logger = logging.getLogger(__package__)

# Configuration schema - this integration only supports config entries
CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up this integration using YAML is not supported."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up component from UI."""
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})
        _LOGGER.info(STARTUP_MESSAGE)

    _LOGGER.debug("Entry data: %s", entry.data)

    user_identifiers = UserDto.from_dict(dict(entry.data))
    _LOGGER.debug("Setting up integration with user id: %s",
                  user_identifiers.id)

    client = DuolingoApiClient(
        user_id=user_identifiers.id,
        timezone=hass.config.time_zone
    )

    coordinator = DuolingoDataUpdateCoordinator(
        hass=hass,
        client=client,
    )

    await coordinator.async_refresh()

    if not coordinator.last_update_success:
        raise ConfigEntryNotReady

    hass.data[DOMAIN][entry.entry_id] = coordinator

    platforms_to_setup = [
        platform for platform in PLATFORMS if entry.options.get(platform, True)
    ]
    coordinator.platforms.extend(platforms_to_setup)

    if platforms_to_setup:
        await hass.config_entries.async_forward_entry_setups(
            entry=entry,
            platforms=platforms_to_setup,
        )

    entry.add_update_listener(async_reload_entry)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    unloaded = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, platform)
                for platform in PLATFORMS
                if platform in coordinator.platforms
            ]
        )
    )
    if unloaded:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unloaded


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
