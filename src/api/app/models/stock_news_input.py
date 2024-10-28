from pydantic import BaseModel


class StockNewsInput(BaseModel):
    stockTicker: str
    companyName: str


__all__ = ["StockNewsInput"]
