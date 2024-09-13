from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    azure_openai_endpoint: str
    openai_api_version: str
    openai_model_id: str
    openai_model_api_name: str
    client_id: str
    client_secret: str
    authority: str
    openai_client_id: str
    apim_subscription_key: str
    application_insights_connection_string: str


@lru_cache
def get_settings():
    return Settings()


__all__ = ["get_settings"]
