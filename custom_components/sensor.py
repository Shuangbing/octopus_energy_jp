from homeassistant.helpers.entity import Entity
from .const import DOMAIN, API_URL
from datetime import datetime, timedelta

class OctopusEnergySensor(Entity):
    def __init__(self, hass, config_entry):
        self.hass = hass
        self.token = config_entry.data["token"]
        self.account_number = config_entry.data["account_number"]
        self.data = None

    @property
    def name(self):
        return "Octopus Energy Usage"

    @property
    def state(self):
        return self.data.get("current_usage") if self.data else "unknown"

    async def async_update(self):
        """Fetch new state data for the sensor."""
        self.data = await self.fetch_usage_data()

async def fetch_usage_data(self):
    """Fetch electricity usage data from the API."""
    import aiohttp

    # 現在の日時と過去24時間の日時を計算
    now = datetime.utcnow()
    from_datetime = now - timedelta(hours=24)

    query = """
    query halfHourlyReadings($accountNumber: String!, $fromDatetime: DateTime, $toDatetime: DateTime) {
      account(accountNumber: $accountNumber) {
        properties {
          electricitySupplyPoints {
            halfHourlyReadings(fromDatetime: $fromDatetime, toDatetime: $toDatetime) {
              startAt
              value
            }
          }
        }
      }
    }
    """
    # クエリ変数を動的に設定
    variables = {
        "accountNumber": self.account_number,
        "fromDatetime": from_datetime.isoformat() + "Z",  # UTCのISOフォーマット
        "toDatetime": now.isoformat() + "Z",
    }
    headers = {"Authorization": f"Bearer {self.token}"}

    async with aiohttp.ClientSession() as session:
        response = await session.post(API_URL, json={"query": query, "variables": variables}, headers=headers)
        result = await response.json()
        return result["data"]["account"]["properties"][0]["electricitySupplyPoints"][0]["halfHourlyReadings"]