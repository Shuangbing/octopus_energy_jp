from homeassistant import config_entries
from homeassistant.core import callback
import voluptuous as vol
from .const import DOMAIN, API_URL, LOGIN_MUTATION

class OctopusEnergyConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Octopus Energy."""

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            try:
                token = await self.obtain_token(user_input["email"], user_input["password"])
                return self.async_create_entry(
                    title="Octopus Energy",
                    data={"email": user_input["email"], "token": token},
                )
            except Exception:
                errors["base"] = "auth_failed"

        data_schema = vol.Schema(
            {
                vol.Required("email"): str,
                vol.Required("password"): str,
            }
        )
        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)

    async def obtain_token(self, email, password):
        """Authenticate with Octopus Energy API and get a token."""
        import aiohttp

        async with aiohttp.ClientSession() as session:
            response = await session.post(
                API_URL,
                json={"query": LOGIN_MUTATION, "variables": {"input": {"email": email, "password": password}}},
            )
            result = await response.json()
            if "errors" in result:
                raise Exception("Authentication failed")
            return result["data"]["obtainKrakenToken"]["token"]

