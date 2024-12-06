from .const import API_URL

async def refresh_token(hass, refresh_token):
    """
    Refresh the authentication token using the provided refresh token.

    Args:
        hass: Home Assistant instance.
        refresh_token (str): The current refresh token to be used for fetching a new token.

    Returns:
        str: The new token if successfully refreshed.
    """
    import aiohttp

    # GraphQL mutation for refreshing token
    REFRESH_MUTATION = """
    mutation refreshToken($input: RefreshTokenInput!) {
      refreshKrakenToken(input: $input) {
        token
        refreshToken
      }
    }
    """

    variables = {"input": {"refreshToken": refresh_token}}

    async with aiohttp.ClientSession() as session:
        try:
            response = await session.post(
                API_URL,
                json={"query": REFRESH_MUTATION, "variables": variables},
            )
            response.raise_for_status()  # Raise exception for HTTP errors
            result = await response.json()

            # Check if the mutation returned a valid response
            if "errors" in result:
                raise Exception(f"Failed to refresh token: {result['errors']}")

            new_token = result["data"]["refreshKrakenToken"]["token"]
            new_refresh_token = result["data"]["refreshKrakenToken"]["refreshToken"]

            # Update the Home Assistant configuration or store with the new tokens
            hass.data["octopus_energy"]["token"] = new_token
            hass.data["octopus_energy"]["refresh_token"] = new_refresh_token

            return new_token

        except Exception as e:
            raise Exception(f"Token refresh failed: {e}")
