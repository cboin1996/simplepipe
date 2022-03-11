from datetime import datetime
from typing import List, Optional
from pydantic import BaseSettings
import os, sys

class Settings(BaseSettings):
    """Configuration using .env file, or environment variables

    Args:
        BaseSettings (pydantic.BaseSettings): BaseSettings object from pydantic
    """
    prod_enabled: bool
    push_gateway_hostname: str
    class Config:
        config_path = os.path.join(os.path.dirname(sys.path[0]), '.env')
        env_file=config_path
        env_file_encoding="utf-8"

def loader():
    """Config loader.\n
    Loading of config is performed first through checking environment,
    then if nothing is found will look for a .env file.
    Note: in production, you should be storing secrets in the environment anyways.
    """
    return Settings()