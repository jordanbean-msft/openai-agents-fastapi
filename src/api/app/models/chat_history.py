from pydantic import BaseModel

from .token_usage import TokenUsage


class ChatHistory(BaseModel):
    summary: str
    usage_including_cached_inference: TokenUsage
    usage_excluding_cached_inference: TokenUsage


__all__ = ["ChatHistory"]
