import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.translation import async_get_translations
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .api import DuolingoApiClient
from .const import DOMAIN
from .dto import UserDto

SCAN_INTERVAL = timedelta(minutes=20)

_LOGGER: logging.Logger = logging.getLogger(__name__)


class DuolingoDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    def __init__(self, hass: HomeAssistant, client: DuolingoApiClient) -> None:
        """Initialize."""
        self.api = client
        self.platforms = []
        self.translations = {}
        self.user_dto = UserDto.from_dict({})

        super().__init__(
            hass=hass,
            logger=_LOGGER,
            name=DOMAIN,
            update_interval=SCAN_INTERVAL,
        )

    async def _async_update_data(self) -> dict[str, object]:
        """Update data via library."""
        try:
            await self.async_fetch_translations()
            self.user_dto = await self.hass.async_add_executor_job(
                self.api.get_user_data,
            )
            return self.user_dto.to_dict

        except Exception as exception:
            raise UpdateFailed(exception) from exception

    async def async_fetch_translations(self) -> None:
        """Fetch translations."""
        self.translations = await async_get_translations(
            self.hass,
            self.hass.config.language,
            "common",
            [DOMAIN],
        )
