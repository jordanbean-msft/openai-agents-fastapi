import logging
from typing import Annotated

import nest_asyncio
from fastapi import APIRouter, Depends
from opentelemetry import trace

from semantic_kernel import Kernel
from semantic_kernel.agents import AgentGroupChat
from semantic_kernel.contents.chat_message_content import ChatMessageContent
from semantic_kernel.contents.utils.author_role import AuthorRole

from ..config import get_settings
from ..dependencies import Dependencies
from ..models.stock_news_input import StockNewsInput
from ..models.stock_news_output import StockNewsOutput

logger = logging.getLogger("uvicorn.error")
tracer = trace.get_tracer(__name__)

router = APIRouter()


@tracer.start_as_current_span(name="analyze")
@router.post("/analyze")
async def post_analyze(
    dependencies: Annotated[Agents, Depends()], stock_news_input: StockNewsInput
) -> StockNewsOutput:
    return await analyze(dependencies, stock_news_input)


async def analyze(dependencies, stock_news_input):
    message = f"Analyze the stock prices and news articles for {stock_news_input.companyName} ({stock_news_input.stockTicker}). Determine if there is correlation between the two."

    results = await build_chat_results(dependencies, message)

    if hasattr(results, 'items'):
        chat_results = results
    else:
        chat_results = { 'input': results }

    result = StockNewsOutput(
        stockTicker=stock_news_input.stockTicker,
        companyName=stock_news_input.companyName,
        overall_result=list(chat_results.values())[-1].summary,
        chat_results=chat_results,
    )

    return result


async def build_chat_results(dependencies, message):
    with tracer.start_as_current_span(name="build_chat_results"):
        kernel = Kernel()
        kernel.add_service(dependencies.Dependencies.azure_chat_completion)

        stock_agent = stock_agent.create_agent(
            kernel=kernel
        )

        news_agent = news_agent.create_agent(
            kernel=kernel
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
            chat_results.append(content)

        return chat_results
