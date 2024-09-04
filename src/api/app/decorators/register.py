open_ai_agent_functions = {}
create_agent_functions = {}


def register_openai_agent_function(func):
    open_ai_agent_functions[func.__name__] = func
    return func


def register_create_agent_function(func):
    create_agent_functions[f"{func.__module__}.{func.__name__}"] = func
    return func


__all__ = [
    "register_openai_agent_function",
    "register_create_agent_function",
    "open_ai_agent_functions",
    "create_agent_functions",
]
