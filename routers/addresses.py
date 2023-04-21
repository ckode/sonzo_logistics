

from fastapi import APIRouter
from fastapi import Request
from models.auth_token import validate_token
import httpx
import json

address_router = APIRouter(include_in_schema=False)


@address_router.get("/validate_address")
@validate_token
async def validate_address():
    from models.globals import FEDEX_AUTH_TOKEN, CONFIG
    from utils.tools import build_validation_request_schema, generate_transaction_id

    _url = CONFIG.get("FEDEX_CONFIG", 'address_validation_api_url')
    _data = json.dumps(build_validation_request_schema())
    _headers = {
            'x-customer-transaction-id': generate_transaction_id(),
            'Content-Type': "application/json",
            'X-locale': "en_US",
            'Authorization': "Bearer {}".format(FEDEX_AUTH_TOKEN.access_token)
    }
    print(f"Data = {_data}")
    async with httpx.AsyncClient() as client:
        response = await client.post(_url, headers=_headers, data=_data)

    print(f"Response was: {response.text}")
    print(f"Response code was: {response.status_code}")
    return response.text


@address_router.get("/list_endpoints")
def list_endpoints(request: Request):
    print(request)
    url_list = [
        {'path': route.path, 'name': route.name}
        for route in request.app.routes
    ]
    return url_list
