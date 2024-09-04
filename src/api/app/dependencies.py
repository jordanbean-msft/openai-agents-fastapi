import asyncio
import logging
from functools import lru_cache

from autogen import AssistantAgent, UserProxyAgent
from fastapi import Depends
from msal import ConfidentialClientApplication

# ------------------------------------------------------------------------------
# NOTE: DO NOT REMOVE THIS, you must import the create_agent functions in order
# for the decorators to register the functions
from .agents import agent1, agent2, user_proxy
from .config import get_settings
from .decorators import open_ai_agent_functions
from .models.all_agents import AllAgents

# ------------------------------------------------------------------------------

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


async def setup_agents_internal() -> AllAgents:
    config = {}
    config["base_url"] = get_settings().azure_openai_endpoint
    config["api_version"] = get_settings().openai_api_version
    config["api_type"] = "azure"
    config["azure_ad_token"] = get_token()["access_token"]
    # config["azure_ad_token_provider"] = result
    config["default_headers"] = {
        "Ocp-Apim-Subscription-Key": get_settings().apim_subscription_key
    }

    config["model"] = get_settings().openai_model_id

    agent_user_proxy = await asyncio.to_thread(user_proxy.create_agent)

    agent1 = await asyncio.to_thread(agent1.create_agent, config)

    register_functions(agent1, agent_user_proxy)

    agent2 = await asyncio.to_thread(agent2.create_agent, config)

    register_functions(agent2, agent_user_proxy)

    return AllAgents(
        agent1=agent1,
        agent2=agent2,
        agent_user_proxy=agent_user_proxy,
    )


def register_functions(
    risk_agent: AssistantAgent, agent_function_executor: UserProxyAgent
):
    # Register the functions for the agent
    for function in risk_agent.llm_config["tools"]:
        name = function["function"]["name"]
        agent_function_executor.register_for_execution(
            name=name,
        )(open_ai_agent_functions[name])


async def setup_agents() -> AllAgents:
    return await setup_agents_internal()


class Agents:
    def __init__(self, common: AllAgents = Depends(setup_agents)):
        self.common = common
        self.agent1 = common.agent1
        self.agent2 = common.agent2
        self.agent_user_proxy = common.agent_user_proxy


__all__ = ["setup_agents", "Agents"]
