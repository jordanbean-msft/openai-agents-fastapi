from opentelemetry import trace

from ..decorators.register import register_openai_agent_function

tracer = trace.get_tracer(__name__)


@tracer.start_as_current_span(name="get_data")
@register_openai_agent_function
async def get_data(test: int) -> str:
    return_value = ""

    return return_value


__all__ = ["get_data"]
