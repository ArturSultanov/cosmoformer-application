import os
from pydantic.v1 import BaseSettings


# TODO: switch to pydantic-settings

class Settings(BaseSettings):
    MODEL_PATH: str = os.environ.get("MODEL_PATH", "cosmoformer_traced_cpu.pt")
    LOG_LEVEL: str = os.environ.get("LOG_LEVEL", "INFO")
    ACCEPTED_MIME_TYPES = {"image/jpeg", "image/png"}

settings = Settings()
