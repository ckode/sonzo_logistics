

from fastapi import FastAPI
from routers.base import address_router
from configparser import ConfigParser

import logging
import sys
import asyncio


def include_routers(_app) -> None:
    """include_routers(_app)

    Add the sub-routers to the FastAPI object

    :param _app: The FastAPI application object
    """
    _app.include_router(address_router)


def get_configuration() -> None:
    """get_configuration()

    Load the application's configuration
    """
    from models.globals import CONFIG_FILE, update_global

    cfg = ConfigParser()
    try:
        cfg.read_file(open(CONFIG_FILE))
    except FileNotFoundError as err:
        logging.error(f"Unable to read configuration file: {CONFIG_FILE}")
        sys.exit(1)

    update_global(cfg, "CONFIG")


def configure_logging() -> None:
    from models.globals import CONFIG, APP_CONFIG_SECTION

    _filename = CONFIG.get(APP_CONFIG_SECTION, 'log_file')
    _log_level = int(CONFIG.get(APP_CONFIG_SECTION, 'log_level'))
    logging.basicConfig(filename=_filename,
                        format='%(asctime)s %(levelname)s :%(message)s',
                        level=_log_level)


def start_service():
    from models.globals import CONFIG, APPLICATION_NAME, APP_VERSION
    from models.auth_token import generate_fedex_auth_token

    _app = FastAPI(title=APPLICATION_NAME, version=APP_VERSION)
    configure_logging()
    asyncio.create_task(generate_fedex_auth_token(CONFIG))
    #generate_fedex_auth_token(CONFIG)
    include_routers(_app)
    return _app


get_configuration()
app = start_service()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

