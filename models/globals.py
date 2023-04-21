import logging

"""
###################################################
Application Globals
###################################################
"""
APPLICATION_NAME = "Crown Logistics"
APP_VERSION = "0.1"
APP_CONFIG_SECTION = 'CROWN_LOGISTICS'
CONFIG_FILE = '.crown_logistics.cfg'

# Configurations Objects
CONFIG = None
FEDEX_AUTH_TOKEN = None

"""
####################################################
Class FedExValidationSchema and defines below
####################################################
"""
FEDEX_VALIDATION_SCHEMA = {
    "inEffectAsOfTimestamp": "",
    "validateAddressControlParameters": {
        "includeResolutionTokens": True
    },
    "addressesToValidate": [
        {
            "address": {
                "streetLines": [
                    "",
                    "",
                    ""
                ],
                "city": "",
                "stateOrProvinceCode": "",
                "postalCode": "",
                "countryCode": "US",
                "urbanizationCode": "",
                "addressVerificationId": ""
            }
        }
    ]
}


def update_global(value, global_name) -> bool:
    """update_global(value, global_name)

    :param value: The value to assign to the named global variable.
    :param global_name: The name of the global variable to update.

    :return: bool ~ If the update was successful or not.
    """
    err_message = f"Updated global variable \"{global_name}\" with a value of type: {type(value)}"
    match global_name:
        case "CONFIG":
            global CONFIG
            CONFIG = value
            logging.debug(err_message)
        case "FEDEX_AUTH_TOKEN":
            global FEDEX_AUTH_TOKEN
            FEDEX_AUTH_TOKEN = value
            logging.debug(err_message)
        case other:
            logging.error(f"Failed to update unknown global variable \"{global_name}\" with variable of type: {type(value)}")
            return False

    return True

