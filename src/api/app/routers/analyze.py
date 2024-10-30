import logging
from typing import Annotated

from fastapi import APIRouter, Depends
from opentelemetry import trace

from semantic_kernel import Kernel
from semantic_kernel.agents import AgentGroupChat
from semantic_kernel.contents.chat_message_content import ChatMessageContent
from semantic_kernel.contents.utils.author_role import AuthorRole
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.functions.kernel_function_from_prompt import KernelFunctionFromPrompt
from semantic_kernel.agents.strategies.selection.kernel_function_selection_strategy import KernelFunctionSelectionStrategy
from semantic_kernel.agents.strategies.termination.kernel_function_termination_strategy import KernelFunctionTerminationStrategy

from app.dependencies import Dependencies
from app.models.stock_news_input import StockNewsInput
from app.models.stock_news_output import StockNewsOutput
from app.agents.news_agent import NewsAgent
from app.agents.stock_agent import StockAgent
from app.plugins.news_plugin import NewsPlugin
from app.plugins.stock_plugin import StockPlugin

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
    message = f"""Analyze the stock prices and news articles for
        {stock_news_input.companyName1} ({stock_news_input.stockTicker1}) and
        {stock_news_input.companyName2} ({stock_news_input.stockTicker2}).
        Determine if there is correlation between the two.
    """

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
        settings = kernel.get_prompt_execution_settings_from_service_id(
            service_id="default")
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

        termination_function = KernelFunctionFromPrompt(
            function_name="termination",
            prompt="""
            Determine if the stock data has been analyzed together with the news data.  If so, respond with a single word: yes

            History:
            {{$history}}
            """,
        )

        selection_function = KernelFunctionFromPrompt(
            function_name="selection",
            prompt=f"""
                Determine which participant takes the next turn in a conversation based on the the most recent participant.
                State only the name of the participant to take the next turn.
                No participant should take more than one turn in a row.

                Choose only from these participants:
                - {stock_agent.name}
                - {news_agent.name}

                Always follow these rules when selecting the next participant:
                - After user input, it is {stock_agent.name}'s turn.
                - After {stock_agent.name} replies, it is {news_agent.name}'s turn.

                History:
                {{{{$history}}}}
            """
        )

        chat = AgentGroupChat(
            agents=[
                stock_agent,
                news_agent
            ],
            selection_strategy=KernelFunctionSelectionStrategy(
                function=selection_function,
                kernel=kernel,
                result_parser=lambda result: str(
                    result.value[0]) if result.value is not None else news_agent.name,
                agent_variable_name="agents",
                history_variable_name="history"
            ),
            termination_strategy=KernelFunctionTerminationStrategy(
                agents=[news_agent],
                function=termination_function,
                kernel=kernel,
                result_parser=lambda result: str(
                    result.value[0]).lower() == "yes",
                history_variable_name="history",
                maximum_iterations=10
            )
        )

        await chat.add_chat_message(ChatMessageContent(
            role=AuthorRole.USER,
            content=message
        ))

        chat_results = []

        async for content in chat.invoke():
            chat_results.append(content.content)

        return chat_results
