# ruff: noqa: BLE001

"""Adds config flow for Duolingo."""

import logging
from typing import Any, cast

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.config_entries import (
    ConfigFlow,
    ConfigFlowResult,
)

from .api import DuolingoApiClient
from .const import (
    CONF_USERNAME,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


class DuolingoFlowHandler(ConfigFlow, domain=DOMAIN):
    """Config flow for Duolingo."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize."""
        self._errors = {}

    async def async_step_user(
            self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle a flow initialized by the user."""
        self._errors = {}

        if user_input is not None:
            username = user_input[CONF_USERNAME]

            # Validate username directly
            try:
                valid = await self._test_credentials(username)
                if valid:
                    # Store username in config entry
                    config_data = {CONF_USERNAME: username}
                    return cast(ConfigFlowResult, self.async_create_entry(
                        title=username,
                        data=config_data,
                    ))
                self._errors["base"] = "auth"
            except Exception:  # noqa: BLE001
                self._errors["base"] = "unknown"
        else:
            user_input = {
                CONF_USERNAME: "",  # Provide defaults for form
            }

        return cast(
            ConfigFlowResult,
            await self._show_config_form(user_input),
        )

    async def _show_config_form(
            self,
            user_input: dict[str, Any]
    ) -> ConfigFlowResult:
        """Show the configuration form to edit location data."""
        result = self.async_show_form(
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
        return cast(ConfigFlowResult, result)

    async def _test_credentials(self, username: str) -> bool:
        """Return true if credentials is valid."""
        try:
            client = DuolingoApiClient(username, self.hass.config.time_zone)
            await self.hass.async_add_executor_job(
                client.get_user_data,
            )
            return True
        except Exception:
            return False
