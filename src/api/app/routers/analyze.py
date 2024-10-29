import logging
from typing import Annotated

import nest_asyncio
from fastapi import APIRouter, Depends
from opentelemetry import trace

from semantic_kernel import Kernel
from semantic_kernel.agents import AgentGroupChat
from semantic_kernel.contents.chat_message_content import ChatMessageContent
from semantic_kernel.contents.utils.author_role import AuthorRole
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior

from ..config import get_settings
from ..dependencies import Dependencies
from ..models.stock_news_input import StockNewsInput
from ..models.stock_news_output import StockNewsOutput
from ..agents.news_agent import NewsAgent
from ..agents.stock_agent import StockAgent
from ..plugins.news_plugin import NewsPlugin
from ..plugins.stock_plugin import StockPlugin

logger = logging.getLogger("uvicorn.error")
tracer = trace.get_tracer(__name__)

router = APIRouter()


@tracer.start_as_current_span(name="analyze")
@router.post("/analyze")
async def post_analyze(
    dependencies: Annotated[Dependencies, Depends()], stock_news_input: StockNewsInput
) -> StockNewsOutput:
    return await analyze(dependencies, stock_news_input)


async def analyze(dependencies, stock_news_input):
    message = f"Analyze the stock prices and news articles for {stock_news_input.companyName1} ({stock_news_input.stockTicker1}) and {stock_news_input.companyName2} ({stock_news_input.stockTicker2}). Determine if there is correlation between the two."

    chat_results = await build_chat_results(dependencies, message)

    result = StockNewsOutput(
        stockTicker1=stock_news_input.stockTicker1,
        companyName1=stock_news_input.companyName1,
        stockTicker2=stock_news_input.stockTicker2,
        companyName2=stock_news_input.companyName2,
        overall_result="",
        chat_results=chat_results,
    )

    return result


async def build_chat_results(dependencies, message):
    with tracer.start_as_current_span(name="build_chat_results"):
        kernel = Kernel()
        
        kernel.add_service(dependencies.azure_chat_completion)
        settings = kernel.get_prompt_execution_settings_from_service_id(service_id="default")
        settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

        kernel.add_plugin(NewsPlugin(), plugin_name="NewsPlugin")
        kernel.add_plugin(StockPlugin(), plugin_name="StockPlugin")

        stock_agent = StockAgent(
            kernel=kernel,
            execution_settings=settings
        )

        news_agent = NewsAgent(
            kernel=kernel,
            execution_settings=settings
        )

        chat = AgentGroupChat(
            agents=[
                stock_agent,
                news_agent
            ]
        )

        await chat.add_chat_message(ChatMessageContent(
            role=AuthorRole.USER,
            content=message
        ))

        chat_results = []

        async for content in chat.invoke():
            chat_results.append(content.content)

        return chat_results
