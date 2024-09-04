import logging
from typing import Annotated

import nest_asyncio
from fastapi import APIRouter, Depends
from opentelemetry import trace

from ..config import get_settings
from ..dependencies import Agents
from ..models.chat_history import ChatHistory
from ..models.test_input import TestInput
from ..models.test_output import TestResults
from ..models.token_usage import TokenUsage

# NOTE: this is required due to a bug in the autogen package when calling functions in a nested chat
# https://github.com/microsoft/autogen/issues/2673
nest_asyncio.apply()

logger = logging.getLogger("uvicorn.error")
tracer = trace.get_tracer(__name__)

router = APIRouter()


@tracer.start_as_current_span(name="test")
@router.post("/test")
async def post_test(
    dependencies: Annotated[Agents, Depends()], test_input: TestInput
) -> TestResults:
    return await evaluate_risk(dependencies, test_input)


async def evaluate_risk(dependencies, test_input):
    message = ""

    dep = await dependencies()

    chat_results = await build_chat_results(dep, message)

    test_chat_results = build_risk_results_chat_results(chat_results)

    result = TestResults(
        test=test_input.test,
        overall_result=list(chat_results.values())[-1].summary,
        chat_results=test_chat_results,
    )

    return result


def build_risk_results_chat_results(chat_results):
    return_chat_results = []
    # for chat_result in chat_results:
    for key, chat_result in chat_results.items():
        usage_including_cached_inference = TokenUsage(
            prompt_tokens=0, completion_tokens=0, total_tokens=0
        )
        usage_excluding_cached_inference = TokenUsage(
            prompt_tokens=0, completion_tokens=0, total_tokens=0
        )

        # TODO: figure out how to parameterize the model name
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
        chat_results = await dependencies.agent_user_proxy.a_initiate_chats(
            [
                {
                    "chat_id": 1,
                    "sender": dependencies.agent_user_proxy,
                    "recipient": dependencies.agent1,
                    "message": message,
                    "max_turns": 2,
                    "summary_method": "last_msg",
                    "verbose": True,
                },
                {
                    "chat_id": 2,
                    "sender": dependencies.agent_user_proxy,
                    "recipient": dependencies.agent2,
                    "message": message,
                    "max_turns": 2,
                    "summary_method": "last_msg",
                    "verbose": True,
                    "prerequisites": [1],
                },
            ]
        )

    return chat_results
