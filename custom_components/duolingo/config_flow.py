# ruff: noqa: BLE001

"""Adds config flow for Duolingo."""
import logging

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_USERNAME
from homeassistant.data_entry_flow import FlowResult

from .api import DuolingoApiClient
from .const import DOMAIN
from .dto import UserIdentifiersDto

_LOGGER = logging.getLogger(__name__)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Duolingo."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize."""
        self._errors = {}

    async def async_step_user(
            self, user_input: dict[str, object] | None = None
    ) -> FlowResult:
        """Handle a flow initialized by the user."""
        self._errors = {}

        if user_input is not None:
            username = user_input[CONF_USERNAME]

            # Validate username directly
            try:
                user_identifiers = await self._get_user_identifiers(username)
                if user_identifiers is not None:
                    # Store username in config entry
                    return self.async_create_entry(
                        title=user_identifiers.as_entry_title,
                        data=user_identifiers.to_dict,
                    )
                self._errors["base"] = "user_not_found"
            except Exception as exception:  # noqa: BLE001
                _LOGGER.warning(
                    f"Exception during username validation: {exception}")
                self._errors["base"] = "unknown"

            return await self._show_config_form(user_input)

        user_input = {CONF_USERNAME: ""}
        return await self._show_config_form(user_input)

    async def _show_config_form(
            self,
            user_input: dict[str, object]
    ) -> FlowResult:
        """Show the configuration form to edit location data."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_USERNAME,
                        default=user_input[CONF_USERNAME]
                    ): str,
                }
            ),
            errors=self._errors,
        )

    async def _get_user_identifiers(
            self,
            username: str
    ) -> UserIdentifiersDto | None:
        """Get user ID from username."""
        try:
            dto = await self.hass.async_add_executor_job(
                DuolingoApiClient.get_user_identifiers, username
            )
            _LOGGER.warning(f"dto: {dto.to_dict}")
            return dto

        except Exception as exception:
            _LOGGER.warning(
                f"Failed to retrieve user ID for username: {username} "
                f"with exception: {exception}"
            )
            return None
