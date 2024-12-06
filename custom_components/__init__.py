from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

DOMAIN = "octopus_energy"

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up Octopus Energy from YAML configuration."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Octopus Energy from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.async_create_task(hass.config_entries.async_forward_entry_setup(entry, "sensor"))
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload Octopus Energy config entry."""
    await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    return True

