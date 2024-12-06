import aiohttp
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from datetime import datetime, timedelta

class OctopusEnergyAPI:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.token = None
        self.refresh_token = None
        self.client = None

    async def authenticate(self):
        transport = AIOHTTPTransport(url="https://api.oejp-kraken.energy/v1/graphql/")
        async with Client(transport=transport, fetch_schema_from_transport=True) as client:
            query = gql(
                """
                mutation login($input: ObtainJSONWebTokenInput!) {
                    obtainKrakenToken(input: $input) {
                        token
                        refreshToken
                    }
                }
                """
            )
            variables = {
                "input": {
                    "email": self.email,
                    "password": self.password
                }
            }
            result = await client.execute(query, variable_values=variables)
            self.token = result["obtainKrakenToken"]["token"]
            self.refresh_token = result["obtainKrakenToken"]["refreshToken"]

    async def get_usage_data(self, account_number, from_datetime, to_datetime):
        if not self.client:
            headers = {"Authorization": f"JWT {self.token}"}
            transport = AIOHTTPTransport(url="https://api.oejp-kraken.energy/v1/graphql/", headers=headers)
            self.client = Client(transport=transport, fetch_schema_from_transport=True)

        query = gql(
            """
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
        )
        variables = {
            "accountNumber": account_number,
            "fromDatetime": from_datetime.isoformat(),
            "toDatetime": to_datetime.isoformat(),
        }
        result = await self.client.execute(query, variable_values=variables)
        return result["account"]["properties"][0]["electricitySupplyPoints"][0]["halfHourlyReadings"]
