from pydantic import BaseModel


class FedExAddressValidationRequest:
    """class FedExAddressValidationRequest

    The class object that handles making an API request to
    the FedEx Address Validation API.
    """


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


class FedExValidationSchema(BaseModel):
    """ class model: FedExValidationSchema(BaseModel)

    This class only contains a dictionary named self.schema

    To use this class, you must first create an instance of it,
    then call obj.initialize() for the structure of the dictionary
    to be created.
    """
    validation_schema: dict = FEDEX_VALIDATION_SCHEMA

