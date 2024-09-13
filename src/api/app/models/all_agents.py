from dataclasses import dataclass

from autogen import AssistantAgent, UserProxyAgent


@dataclass
class AllAgents:
    news_data_agent: AssistantAgent
    stock_data_agent: AssistantAgent
    agent_user_proxy: UserProxyAgent


__all__ = ["AllAgents"]
