import asyncio
import logging
from functools import lru_cache

from fastapi import Depends
from azure.identity import ClientSecretCredential, get_bearer_token_provider
from .models.all_dependencies import AllDependencies
from .config import get_settings
from semantic_kernel.connectors.ai.open_ai.services.azure_chat_completion import AzureChatCompletion

logger = logging.getLogger("uvicorn.error")


# @lru_cache
# def get_token():
#     return get_token_internal()


# def get_token_internal():
#     app = ConfidentialClientApplication(
#         client_id=get_settings().client_id,
#         client_credential=get_settings().client_secret,
#         authority=f"https://login.microsoftonline.com/{get_settings().authority}",
#     )

#     result = app.acquire_token_for_client(
#         scopes=[f"api://{get_settings().openai_client_id}//.default"]
#     )

#     return result

@lru_cache
def setup_dependencies_internal() -> AllDependencies:    
    credential = ClientSecretCredential(
        tenant_id=get_settings().tenant_id, 
        client_id=get_settings().client_id,
        client_secret=get_settings().client_secret
    )

    token_provider = get_bearer_token_provider(credential, f"api://{get_settings().openai_client_id}/.default")

    azure_chat_completion = AzureChatCompletion(
        deployment_name=get_settings().openai_deployment_name,
        endpoint=get_settings().azure_openai_endpoint,
        api_version=get_settings().openai_api_version,
        ad_token_provider=token_provider,
        default_headers={
            "Ocp-Apim-Subscription-Key": get_settings().apim_subscription_key
        },        
    )

    return AllDependencies(
        azure_chat_completion=azure_chat_completion
    )


def setup_dependencies() -> AllDependencies:
    return setup_dependencies_internal()


class Dependencies:
    def __init__(self, common: AllDependencies = Depends(setup_dependencies)):
        self.common = common
        self.azure_chat_completion = common.azure_chat_completion

__all__ = ["setup_agents", "Dependencies"]
