from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN, CONF_EMAIL, CONF_PASSWORD, CONF_ACCOUNT_NUMBER
from .api import OctopusEnergyAPI

class OctopusEnergyConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Octopus Energy Sync."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                api = OctopusEnergyAPI(user_input[CONF_EMAIL], user_input[CONF_PASSWORD])
                await self.hass.async_add_executor_job(api.authenticate)
                
                # If authentication is successful, create the config entry
                return self.async_create_entry(title="Octopus Energy", data=user_input)
            except Exception:
                errors["base"] = "auth_error"

        # Show the form to the user
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_EMAIL): str,
                    vol.Required(CONF_PASSWORD): str,
                    vol.Required(CONF_ACCOUNT_NUMBER): str,
                }
            ),
            errors=errors,
        )

config_entries.HANDLERS.register(DOMAIN)(OctopusEnergyConfigFlow)
