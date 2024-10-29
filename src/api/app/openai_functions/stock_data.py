from opentelemetry import trace
from json import loads
import aiofiles
import os

from semantic_kernel.functions.kernel_function_decorator import kernel_function

tracer = trace.get_tracer(__name__)

class StockPlugin:
    @tracer.start_as_current_span(name="get_stock_data")
    @kernel_function(description="")
    async def get_stock_data(stock_ticker_symbol: str) -> str:
        return_value = []
        async with aiofiles.open(os.path.abspath(os.path.dirname(__file__)) + '/../data/stock_data.json', 'r') as f:
            data = loads(await f.read())
            for article in data['stockPriceChanges']:
                if stock_ticker_symbol in article['stockTicker']:
                    return_value.append(article)
                    
        return str(return_value)


__all__ = ["StockPlugin"]
