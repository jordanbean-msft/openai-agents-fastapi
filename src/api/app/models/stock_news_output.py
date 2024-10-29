from pydantic import BaseModel

from semantic_kernel.contents.chat_history import ChatHistory

class StockNewsOutput(BaseModel):
    stockTicker: str
    companyName: str
    overall_result: str
    chat_results: list[ChatHistory]


__all__ = ["StockNewsOutput"]
