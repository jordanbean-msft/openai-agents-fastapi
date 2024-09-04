from pydantic import BaseModel

from .chat_history import ChatHistory


class TestResults(BaseModel):
    test: int
    overall_result: str
    chat_results: list[ChatHistory]


__all__ = ["TestResults"]
