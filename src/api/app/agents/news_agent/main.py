import logging
import tempfile

from semantic_kernel.agents import ChatCompletionAgent

logger = logging.getLogger("uvicorn.error")
temp_dir = tempfile.TemporaryDirectory()

class NewsAgent(ChatCompletionAgent):
    def __init__(self, kernel):
        ChatCompletionAgent.__init__(
            self,
            kernel=kernel,
            name="news-agent",
            instructions="You are the news agent. You are responsible for providing news articles related to the stock market."
    )

__all__ = ["NewsAgent"]
