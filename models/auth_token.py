import functools

from pydantic import BaseModel, validator

import time
import json
import logging
import asyncio
import httpx


class FedExAuthToken(BaseModel):
    raw_json: str
    access_token: str
    token_type: str
    expires_in: int = 0
    scope: str
    token_expires: float = 0.0

    def __repr__(self, hide_token=True) -> str:
        """FedExAuthToken.__repr__()

        A method to display a visually friendly version
        of the FedExAuthToken.

        Keyword arguments:
        hide_token: bool -- If True, replace token characters with * for security. (default: True)
        """
        t_length = len(self.access_token)
        if hide_token:
            token = "*" * t_length
        else:
            token = self.access_token

        output = (f"FedExAuthToken->Raw JSON: {self.raw_json}", f"FedExAuthToken->Access Token: {token}",
                  f"FedExAuthToken->Token Type: {self.token_type}", f"FedExAuthToken->Expires In: {self.expires_in}",
                  f"FedExAuthToken->Scope: {self.scope}")

        return '\n'.join(output)

    @classmethod
    def initialize(cls, json_resp: str) -> bool:
        """FedExAuthToken.initialize(json_resp) -> bool

        Initialize the FedExAuthToken class object and return a boolean
        for success or failure.

        Arguments
        json_resp: str -- The json response returned from FedEx's OAuth
        API token authentication request.
        """
        try:
            data = json.loads(json_resp)
        except Exception as err:
            logging.error("Failure to load OAuth Token JSON Response.")
            logging.error(err.args)
            return False

        try:
            cls.raw_json = data
            cls.access_token = data['access_token']
            cls.token_type = data['token_type']
            cls.expires_in = data['expires_in']
            cls.scope = data['scope']
            # Current time in seconds + expires_in time - Configured "expire_early" time
            from models.globals import CONFIG
            cls.token_expires = int(time.time()) + cls.expires_in - int(CONFIG.get("FEDEX_CONFIG", "expire_early"))

        except Exception as err:
            logging.error("Failed to initialize FedExAuthToken object from JSON response data.")
            logging.error(err.args)
            return False

        return True

    @classmethod
    @validator("access_token")
    def is_valid_token(cls) -> bool:
        """FedExAuthToken.valid_token() -> bool

        Evaluate if token is still valid and return True or False.
        """
        from models.globals import FEDEX_AUTH_TOKEN

        if not FEDEX_AUTH_TOKEN or time.time() > FEDEX_AUTH_TOKEN.token_expires:
            return False

        return True


def validate_token(func):
    """Decorator ~ validate_token(func)

    Validate FedEx OAuth token is still valid or
    regenerate a new one if expired.
    """
    @functools.wraps(func)
    async def _wrapper():
        from models.globals import FEDEX_AUTH_TOKEN, CONFIG

        if not FEDEX_AUTH_TOKEN or not FedExAuthToken.is_valid_token():
            _ = await generate_fedex_auth_token(CONFIG)
        _str = await func()
        return _str
    return _wrapper


async def make_fedex_auth_token_request(_auth_url, _payload, _headers) -> str:
    """make_fedex_auth_token_request(_auth_url, _auth_payload, _headers) -> str

    Make FedEx Address Validation API request.

    :param _auth_url: str -- FedEx OAuth API URL
    :param _payload: str -- FedEx Address Validation Schema with Address Data to be validated
    :param _headers: dict -- Required headers to make an authenticated address validation request

    :return: str -- JSON response from FedEx Address Validation API
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(_auth_url, data=_payload, headers=_headers)

    return str(response.text)


async def generate_fedex_auth_token(configuration) -> bool:
    """generate_fedex_auth_token(configuration)

    Generate a FedEx OAuth token.

    :param configuration:
    :return: FedExAuthToken class object
    """
    from models.globals import update_global

    response = ""
    _token = None

    cfg_section = "FEDEX_CONFIG"
    client_id = configuration.get(cfg_section, 'client_id')
    client_secret = configuration.get(cfg_section, 'client_secret')
    auth_payload = configuration.get(cfg_section, 'auth_payload').format(client_id, client_secret)
    auth_url = configuration.get(cfg_section, 'auth_token_api_url')
    expire_early = int(configuration.get(cfg_section, 'expire_early'))

    headers = {
        'Content-Type': "application/x-www-form-urlencoded"
    }
    _token = await make_fedex_auth_token_request(auth_url, auth_payload, headers)
    _token_data = json.loads(_token)
    _token = FedExAuthToken(raw_json=json.dumps(_token_data),
                             access_token=_token_data['access_token'],
                             token_type=_token_data['token_type'],
                             expires_in=int(_token_data['expires_in']),
                             scope=_token_data['scope'],
                             token_expires=int(time.time() + int(_token_data['expires_in']) - expire_early)
                             )

    update_global(_token, "FEDEX_AUTH_TOKEN")
    return True


def print_token():
    from models.globals import FEDEX_AUTH_TOKEN

    print(f"Token = {FEDEX_AUTH_TOKEN}")
