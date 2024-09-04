import logging
import tempfile

from autogen import UserProxyAgent
from autogen.coding import LocalCommandLineCodeExecutor

logger = logging.getLogger("uvicorn.error")

temp_dir = tempfile.TemporaryDirectory()
executor = LocalCommandLineCodeExecutor(timeout=10, work_dir=temp_dir.name)


def create_agent() -> UserProxyAgent:
    agent = UserProxyAgent(
        name="user",
        llm_config=None,
        human_input_mode="NEVER",
        code_execution_config={"executor": executor},
    )

    logger.debug(f"Agent created - NAME: {agent.name}")

    return agent


__all__ = ["create_agent"]
