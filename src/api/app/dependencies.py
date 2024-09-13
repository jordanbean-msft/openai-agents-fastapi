import asyncio
import logging
from functools import lru_cache

from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
from fastapi import Depends
from msal import ConfidentialClientApplication

# ------------------------------------------------------------------------------
# NOTE: DO NOT REMOVE THIS, you must import the create_agent functions in order
# for the decorators to register the functions
from .agents import user_proxy, news_agent, stock_agent
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
    config["default_headers"] = {
        "Ocp-Apim-Subscription-Key": get_settings().apim_subscription_key
    }

    config["model"] = get_settings().openai_model_id

    agent_user_proxy = await asyncio.to_thread(user_proxy.create_agent)

    news_data_agent = await asyncio.to_thread(news_agent.create_agent, config)

    register_functions(news_data_agent, agent_user_proxy)

    stock_data_agent = await asyncio.to_thread(stock_agent.create_agent, config)

    register_functions(stock_data_agent, agent_user_proxy)

    groupChat = GroupChat(agents=[
        news_data_agent,
        stock_data_agent,
        agent_user_proxy
    ], messages=[])

    manager = GroupChatManager(groupchat=groupChat, llm_config={
            "config_list": [config],
            "cache_seed": None,
        })

    return AllAgents(
        news_data_agent=news_data_agent,
        stock_data_agent=stock_data_agent,
        agent_user_proxy=agent_user_proxy,
        manager=manager
    )


def register_functions(agent: AssistantAgent, agent_function_executor: UserProxyAgent):
    # Register the functions for the agent
    for function in agent.llm_config["tools"]:
        name = function["function"]["name"]
        agent_function_executor.register_for_execution(
            name=name,
        )(open_ai_agent_functions[name])


async def setup_agents() -> AllAgents:
    return await setup_agents_internal()


class Agents:
    def __init__(self, common: AllAgents = Depends(setup_agents)):
        self.common = common
        self.news_data_agent = common.news_data_agent
        self.stock_data_agent = common.stock_data_agent
        self.agent_user_proxy = common.agent_user_proxy
        self.manager = common.manager


__all__ = ["setup_agents", "Agents"]
