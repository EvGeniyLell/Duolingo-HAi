# ruff: noqa: BLE001

"""Adds config flow for Duolingo."""
import logging
from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .api import DuolingoApiClient
from .const import (
    CONF_USERNAME,
    CONF_USER_ID,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Duolingo."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize."""
        self._errors = {}

    async def async_step_user(
            self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle a flow initialized by the user."""
        self._errors = {}

        if user_input is not None:
            username = user_input[CONF_USERNAME]

            # Validate username directly
            try:
                user_id = await self._get_user_id(username)
                if user_id is not None:
                    # Store username in config entry
                    config_data = {
                        CONF_USERNAME: username,
                        CONF_USER_ID: user_id,
                    }
                    return self.async_create_entry(
                        title=f"id:{user_id}",
                        description=username,
                        data=config_data,
                    )
                self._errors["base"] = "user_not_found"
            except Exception:  # noqa: BLE001
                self._errors["base"] = "unknown"

            return await self._show_config_form(user_input)

        user_input = {CONF_USERNAME: ""}
        return await self._show_config_form(user_input)

    async def _show_config_form(
            self,
            user_input: dict[str, Any]
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

    async def _get_user_id(self, username: str) -> int | None:
        """Get user ID from username."""
        try:
            user_id = await self.hass.async_add_executor_job(
                DuolingoApiClient.get_user_id, username
            )
            return user_id

        except Exception as exception:
            _LOGGER.warning(
                f"Failed to retrieve user ID for username: {username} with exception: {exception}"
            )
            return None
