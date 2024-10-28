import logging
from typing import Annotated

import nest_asyncio
from fastapi import APIRouter, Depends
from opentelemetry import trace
import autogen

from ..config import get_settings
from ..dependencies import Agents
from ..models.chat_history import ChatHistory
from ..models.stock_news_input import StockNewsInput
from ..models.stock_news_output import StockNewsOutput
from ..models.token_usage import TokenUsage

# NOTE: this is required due to a bug in the autogen package when calling functions in a nested chat
# https://github.com/microsoft/autogen/issues/2673
nest_asyncio.apply()

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

    #dep = await dependencies()

    results = await build_chat_results(dependencies, message)

    if hasattr(results, 'items'):
        chat_results = results
    else:
        chat_results = { 'input': results }

    analyze_test_results = build_analyze_test_results(chat_results)

    result = StockNewsOutput(
        stockTicker=stock_news_input.stockTicker,
        companyName=stock_news_input.companyName,
        overall_result=list(chat_results.values())[-1].summary,
        chat_results=analyze_test_results,
    )

    return result


def build_analyze_test_results(chat_results):
    return_chat_results = []

    for key, chat_result in chat_results.items():
        usage_including_cached_inference = TokenUsage(
            prompt_tokens=0, completion_tokens=0, total_tokens=0
        )
        usage_excluding_cached_inference = TokenUsage(
            prompt_tokens=0, completion_tokens=0, total_tokens=0
        )

        if (
            get_settings().openai_model_api_name
            in chat_result.cost["usage_including_cached_inference"]
        ):
            usage_including_cached_inference = TokenUsage(
                prompt_tokens=chat_result.cost["usage_including_cached_inference"][
                    get_settings().openai_model_api_name
                ]["prompt_tokens"],
                completion_tokens=chat_result.cost["usage_including_cached_inference"][
                    get_settings().openai_model_api_name
                ]["completion_tokens"],
                total_tokens=chat_result.cost["usage_including_cached_inference"][
                    get_settings().openai_model_api_name
                ]["total_tokens"],
            )

        if (
            get_settings().openai_model_api_name
            in chat_result.cost["usage_excluding_cached_inference"]
        ):
            usage_excluding_cached_inference = TokenUsage(
                prompt_tokens=chat_result.cost["usage_excluding_cached_inference"][
                    get_settings().openai_model_api_name
                ]["prompt_tokens"],
                completion_tokens=chat_result.cost["usage_excluding_cached_inference"][
                    get_settings().openai_model_api_name
                ]["completion_tokens"],
                total_tokens=chat_result.cost["usage_excluding_cached_inference"][
                    get_settings().openai_model_api_name
                ]["total_tokens"],
            )

        return_chat_results.append(
            ChatHistory(
                summary=chat_result.summary,
                usage_including_cached_inference=usage_including_cached_inference,
                usage_excluding_cached_inference=usage_excluding_cached_inference,
            )
        )

    return return_chat_results


async def build_chat_results(dependencies, message):
    with tracer.start_as_current_span(name="build_chat_results"):
        chat_results = await dependencies.agent_user_proxy.a_initiate_chat(
            dependencies.manager,
            message=message
        )
        # chat_results = await dependencies.agent_user_proxy.a_initiate_chats(
        #     [
        #         {
        #             "chat_id": 1,
        #             "sender": dependencies.agent_user_proxy,
        #             "recipient": dependencies.news_data_agent,
        #             "message": message,
        #             "max_turns": 2,
        #             "summary_method": "last_msg",
        #             "verbose": True,
        #         },
        #         {
        #             "chat_id": 2,
        #             "sender": dependencies.agent_user_proxy,
        #             "recipient": dependencies.stock_data_agent,
        #             "message": message,
        #             "max_turns": 2,
        #             "summary_method": "last_msg",
        #             "verbose": True,
        #             "prerequisites": [1],
        #         },
        #     ]
        # )

    return chat_results
