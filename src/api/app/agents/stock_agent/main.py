import logging
import tempfile

from semantic_kernel.agents import ChatCompletionAgent

logger = logging.getLogger("uvicorn.error")
temp_dir = tempfile.TemporaryDirectory()

def create_agent(service_id, kernel) -> ChatCompletionAgent:
    agent = ChatCompletionAgent(
        service_id=service_id,
        kernel=kernel,
        name="stock-agent",
        instructions=""
    )

    logger.debug(f"Agent created - NAME: {agent.name}")

    return agent

__all__ = ["create_agent"]
