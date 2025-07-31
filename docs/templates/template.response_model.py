# File: template.response_model.py
# Path: backend/app/models/model_response.py

"""
Model: Response Wrapper
Description:
    Generic API response model wrapping data, success flag, and error info.
    Compatible with Pydantic v2 and FastAPI response_model typing.

Author: Matthias Morath
"""

# MARK: ━━━ Imports ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
from typing import Generic, TypeVar
from pydantic import BaseModel, field
from pydantic.functional_validators import AfterValidator
from models.model_error import ErrorModel

T = TypeVar("T")


# MARK: ━━━ Response Model ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class ResponseModel(BaseModel, Generic[T]):
    """Standard API wrapper model"""

    success: bool = field(..., description="Indicates request outcome")
    data: T | None = field(default=None, description="Response payload")
    error: ErrorModel | None = field(default=None, description="Error details")

    model_config = {"from_attributes": True, "extra": "forbid"}


# EOF
