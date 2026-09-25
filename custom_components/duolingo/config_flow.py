# ruff: noqa: BLE001

"""Adds config flow for Duolingo."""
import logging

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_USERNAME
from homeassistant.data_entry_flow import FlowResult

from .api import DuolingoApi
from .const import DOMAIN, JWT_TOKEN
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
            username = user_input.get(CONF_USERNAME, "")
            jwt_token = user_input.get(JWT_TOKEN, "")

            if not isinstance(username, str) or not isinstance(jwt_token, str):
                self._errors["base"] = "unknown"
                return await self._show_config_form(user_input)

            try:
                user_identifiers = await self._get_user_identifiers(username)
                if user_identifiers is None:
                    self._errors["base"] = "user_not_found"
                    return await self._show_config_form(user_input)

                return self.async_create_entry(
                    title=user_identifiers.as_entry_title,
                    data={
                        **user_identifiers.to_dict,
                        JWT_TOKEN: jwt_token,
                    },
                )
            except Exception as exception:
                _LOGGER.exception("Exception during setup: %s", exception)
                self._errors["base"] = "unknown"

            return await self._show_config_form(user_input)

        return await self._show_config_form({CONF_USERNAME: "", JWT_TOKEN: ""})

    async def async_step_reauth(
            self, user_input: dict[str, object] | None = None
    ) -> FlowResult:
        """Initiate re-authentication."""
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(
            self, user_input: dict[str, object] | None = None
    ) -> FlowResult:
        """Handle re-authentication confirmation."""
        self._errors = {}
        reauth_entry = self.hass.config_entries.async_get_entry(self.context["entry_id"])

        if user_input is not None:
            jwt_token = user_input[JWT_TOKEN]

            try:
                self.hass.config_entries.async_update_entry(
                    reauth_entry,
                    data={**reauth_entry.data, JWT_TOKEN: jwt_token},
                )
                await self.hass.config_entries.async_reload(reauth_entry.entry_id)
                return self.async_abort(reason="reauth_successful")
            except Exception as exception:
                _LOGGER.exception("Exception during re-authentication: %s", exception)
                self._errors["base"] = "unknown"

        return self.async_show_form(
            step_id="reauth_confirm",
            data_schema=vol.Schema({
                vol.Required(JWT_TOKEN): str,
            }),
            errors=self._errors,
        )

    async def _show_config_form(self, user_input: dict[str, object]) -> FlowResult:
        """Show the configuration form."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_USERNAME, default=user_input.get(CONF_USERNAME, "")): str,
                vol.Required(JWT_TOKEN, default=user_input.get(JWT_TOKEN, "")): str,
            }),
            errors=self._errors,
        )

    async def _get_user_identifiers(self, username: str) -> UserIdentifiersDto | None:
        """Get user identifiers from username."""
        try:
            return await self.hass.async_add_executor_job(
                DuolingoApi.get_user_identifiers, username
            )
        except Exception as exception:
            _LOGGER.exception(
                "Failed to retrieve user ID for username: %s with exception: %s",
                username, exception,
            )
            return None
