from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    azure_openai_endpoint: str
    openai_api_version: str
    openai_deployment_name: str
    client_id: str
    client_secret: str
    tenant_id: str
    openai_client_id: str
    apim_subscription_key: str
    application_insights_connection_string: str
    azure_openai_api_key: str = ""
    use_apim: bool = False


@lru_cache
def get_settings():
    return Settings()


__all__ = ["get_settings"]
