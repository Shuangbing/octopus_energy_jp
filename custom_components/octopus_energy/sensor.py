from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)
from datetime import timedelta
from .const import DOMAIN, CONF_ACCOUNT_NUMBER
from .api import OctopusEnergyAPI

async def async_setup_entry(hass: HomeAssistant, entry, async_add_entities):
    api = OctopusEnergyAPI(entry.data["email"], entry.data["password"])
    await api.authenticate()

    coordinator = DataUpdateCoordinator(
        hass,
        hass.logger,
        name="octopus_energy_usage",
        update_method=lambda: update_usage_data(api, entry.data[CONF_ACCOUNT_NUMBER]),
        update_interval=timedelta(hours=1),
    )

    await coordinator.async_refresh()

    async_add_entities([OctopusEnergySensor(coordinator)], True)

async def update_usage_data(api, account_number):
    now = datetime.utcnow()
    from_time = now - timedelta(hours=13)
    to_time = now - timedelta(hours=1)
    usage_data = await api.get_usage_data(account_number, from_time, to_time)
    total_usage = sum(float(reading["value"]) for reading in usage_data)
    return total_usage

class OctopusEnergySensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Octopus Energy Usage"
        self._attr_unique_id = f"{DOMAIN}_usage"
        self._attr_unit_of_measurement = "kWh"

    @property
    def state(self):
        return self.coordinator.data
