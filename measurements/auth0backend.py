import requests
from social_core.backends.oauth import BaseOAuth2

class Auth0(BaseOAuth2):
    """Auth0 OAuth authentication backend"""
    name = 'auth0'
    SCOPE_SEPARATOR = ''
    ACCESS_TOKEN_METHOD = 'POST'
    EXTRA_DATA = [
        ('picture', 'picture')
    ]

    def authorization_url(self):
        return "https://" + self.setting('DOMAIN') + "/authorize"

    def access_token_url(self):
        """Return the token endpoint."""
        return "https://" + self.setting('DOMAIN') + "/oauth/token"

    def get_user_id(self, details, response):
        """Return current user id."""
        return details['user_id'] #cambiando

    def get_user_details(self, response):
        url = 'https://' + self.setting('DOMAIN') + '/userinfo'
        headers = {'authorization': 'Bearer ' + response['access_token']}
        resp = requests.get(url, headers=headers)
        userinfo = resp.json();print('backend: ' + str(userinfo))
        return {'user_id': userinfo['http://isis2503-whatevercamps:auth0:com/role']}
