from dataclasses import dataclass

from autogen import AssistantAgent, UserProxyAgent


@dataclass
class AllAgents:
    agent1: AssistantAgent
    agent2: AssistantAgent
    agent_user_proxy: UserProxyAgent


__all__ = ["AllAgents"]
