from pydantic import BaseModel

from semantic_kernel.contents.chat_history import ChatHistory

class StockNewsOutput(BaseModel):
    stockTicker1: str
    companyName1: str
    stockTicker2: str
    companyName2: str
    overall_result: str
    chat_results: list[ChatHistory]


__all__ = ["StockNewsOutput"]
