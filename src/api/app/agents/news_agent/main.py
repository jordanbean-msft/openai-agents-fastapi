import logging

from semantic_kernel.agents import ChatCompletionAgent

logger = logging.getLogger("uvicorn.error")

class NewsAgent(ChatCompletionAgent):
    def __init__(self, kernel, execution_settings):
        ChatCompletionAgent.__init__(
            self,
            kernel=kernel,
            name="news-agent",
            instructions="You are the news agent. You are responsible for providing news articles related to the stock market.",
            execution_settings=execution_settings
        )

__all__ = ["NewsAgent"]
