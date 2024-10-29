from opentelemetry import trace
from json import loads
import aiofiles
import os
from typing import Annotated

from semantic_kernel.functions.kernel_function_decorator import kernel_function

tracer = trace.get_tracer(__name__)

class NewsPlugin:
    @tracer.start_as_current_span(name="get_news_data")
    @kernel_function(description="Provides news articles related to the stock market.")
    async def get_news_data(self, company_name: Annotated[str, "The name of the company to get news articles for"]) -> Annotated[str, "News articles for the given company"]:
        return_value = []
        async with aiofiles.open(os.path.abspath(os.path.dirname(__file__)) + '/../data/news_data.json', 'r') as f:
            data = loads(await f.read())
            return_value = [article for article in data['newsArticles'] if company_name in article['companyName']]

        return str(return_value)


__all__ = ["NewsPlugin"]
