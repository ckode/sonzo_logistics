from models.globals import FEDEX_VALIDATION_SCHEMA

from datetime import date
from uuid import uuid4

import json


def get_date() -> str:
    """get_date()

    Returns current date as a string in YYYY-MM-DD format

    :return: ~ date string
    """
    return str(date.today())


def generate_transaction_id() -> str:
    """generate_transaction_id()

    Generates a random UUID to use as a
    transaction code for the API request.

    :return: uuid
    """
    return str(uuid4())


def build_validation_request_schema() -> dict:
    """build_validation_request_schema()

    Builds the schema for the FedEx Address Validation API

    :return: dict
    """
    print("Building validation request schema")
    address = {
        "address": {
            "streetLines": [
                "8 John Perry Dr",
                "",
            ],
            "city": "Danbury",
            "stateOrProvinceCode": "CT",
            "postalCode": "06811",
            "countryCode": "US",
            "urbanizationCode": "",
            "addressVerificationId": "{}".format(generate_transaction_id())
        }
    }
    _schema = FEDEX_VALIDATION_SCHEMA
    _schema["inEffectAsOfTimestamp"] = get_date()
    _schema["validateAddressControlParameters"]["includeResolutionTokens"] = True
    _schema["addressesToValidate"][0]["address"] = address["address"]

    print(f"_Schema type: {type(_schema)}")
    return _schema
