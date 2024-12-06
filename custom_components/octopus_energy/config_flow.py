import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from .const import DOMAIN, CONF_EMAIL, CONF_PASSWORD, CONF_ACCOUNT_NUMBER
from .api import OctopusEnergyAPI

class OctopusEnergyFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        errors = {}
        if user_input is not None:
            api = OctopusEnergyAPI(user_input[CONF_EMAIL], user_input[CONF_PASSWORD])
            try:
                await api.authenticate()
                return self.async_create_entry(title="Octopus Energy", data=user_input)
            except Exception:
                errors["base"] = "auth_error"

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
