from opentelemetry import trace
from json import loads
import aiofiles
import os

from semantic_kernel.functions.kernel_function_decorator import kernel_function

tracer = trace.get_tracer(__name__)

class NewsPlugin:
    @tracer.start_as_current_span(name="get_news_data")
    @kernel_function(description="")
    async def get_news_data(company_name: str) -> str:
        return_value = []
        async with aiofiles.open(os.path.abspath(os.path.dirname(__file__)) + '/../data/news_data.json', 'r') as f:
            data = loads(await f.read())
            for article in data['newsArticles']:
                if company_name in article['companyName']:
                    return_value.append(article)

        return str(return_value)


__all__ = ["NewsPlugin"]
