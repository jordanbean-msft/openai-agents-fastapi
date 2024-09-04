from pydantic import BaseModel


class TestInput(BaseModel):
    test: int


__all__ = ["TestInput"]
