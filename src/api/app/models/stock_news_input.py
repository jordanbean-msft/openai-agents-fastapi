from pydantic import BaseModel


class StockNewsInput(BaseModel):
    stockTicker1: str
    companyName1: str
    stockTicker2: str
    companyName2: str


__all__ = ["StockNewsInput"]
