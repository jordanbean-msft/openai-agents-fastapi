import asyncio
import logging
from functools import lru_cache

from fastapi import Depends
from msal import ConfidentialClientApplication
from .models import AllDependencies
from .config import get_settings
from semantic_kernel.connectors.ai.open_ai.services.azure_chat_completion import AzureChatCompletion

logger = logging.getLogger("uvicorn.error")


@lru_cache
def get_token():
    return get_token_internal()


def get_token_internal():
    app = ConfidentialClientApplication(
        client_id=get_settings().client_id,
        client_credential=get_settings().client_secret,
        authority=f"https://login.microsoftonline.com/{get_settings().authority}",
    )

    result = app.acquire_token_for_client(
        scopes=[f"api://{get_settings().openai_client_id}//.default"]
    )

    return result

@lru_cache
async def setup_dependencies_internal() -> AllDependencies:
    config = {}
    config["base_url"] = get_settings().azure_openai_endpoint
    config["api_version"] = get_settings().openai_api_version
    config["api_type"] = "azure"
    config["azure_ad_token"] = get_token()["access_token"]
    config["default_headers"] = {
        "Ocp-Apim-Subscription-Key": get_settings().apim_subscription_key
    }

    config["model"] = get_settings().openai_model_id

    azure_chat_completion = AzureChatCompletion(
    )

    return AllDependencies(
        azure_chat_completion=azure_chat_completion
    )


async def setup_dependencies() -> AllDependencies:
    return await setup_dependencies_internal()


class Dependencies:
    def __init__(self, common: AllDependencies = Depends(setup_dependencies)):
        self.common = common
        self.azure_chat_completion = common.azure_chat_completion

__all__ = ["setup_agents", "Dependencies"]
