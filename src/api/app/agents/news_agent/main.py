import logging
import tempfile

from autogen import AssistantAgent
from autogen.coding import LocalCommandLineCodeExecutor

from ...decorators.register import register_create_agent_function
from ...openai_functions.news_data import get_news_data

logger = logging.getLogger("uvicorn.error")
temp_dir = tempfile.TemporaryDirectory()
executor = LocalCommandLineCodeExecutor(timeout=10, work_dir=temp_dir.name)


@register_create_agent_function
def create_agent(config) -> AssistantAgent:
    agent = AssistantAgent(
        name="news-article-agent",
        llm_config={
            "config_list": [config],
            "cache_seed": None,
        },
        code_execution_config={"executor": executor},
        function_map=None,
        human_input_mode="NEVER",
        system_message=(" Return 'TERMINATE' when the task is done."),
        is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
    )

    agent.register_for_llm(
        name="get_news_data",
        description="Get news data",
    )(get_news_data)

    logger.debug(f"Agent created - NAME: {agent.name}")

    return agent


__all__ = ["create_agent"]