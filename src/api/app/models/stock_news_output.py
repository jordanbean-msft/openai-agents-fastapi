from pydantic import BaseModel

class StockNewsOutput(BaseModel):
    stockTicker1: str
    companyName1: str
    stockTicker2: str
    companyName2: str
    overall_result: str
    chat_results: list[str]


__all__ = ["StockNewsOutput"]
