DOMAIN = "octopus_energy"
API_URL = "https://api.octopus.energy/graphql/"
LOGIN_MUTATION = """
mutation login($input: ObtainJSONWebTokenInput!) {
  obtainKrakenToken(input: $input) {
    token
    refreshToken
  }
}
"""

