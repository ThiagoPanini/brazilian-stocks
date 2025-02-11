""" ToDo
from typing import Any
from pydantic import BaseModel


class BaseResponse(BaseModel):
    status_code: int
    message: str | None = None


class SuccessResponse(BaseResponse):
    status_code: int = 200
"""
