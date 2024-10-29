import logging
import tempfile

from semantic_kernel.agents import ChatCompletionAgent

logger = logging.getLogger("uvicorn.error")
temp_dir = tempfile.TemporaryDirectory()

class StockAgent(ChatCompletionAgent):
    def __init__(self, kernel):
        ChatCompletionAgent.__init__(
            self,
            kernel=kernel,
            name="stock-agent",
            instructions="You are the stock agent. You are responsible for providing stock prices related to the stock market."
    )
        
__all__ = ["StockAgent"]
