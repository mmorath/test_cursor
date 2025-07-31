# File: template.error_model.py
# Path: backend/app/models/model_error.py

"""
Model: Error Response
Description:
    Defines the standard error structure returned by all endpoints.
    Used to wrap all API-level errors with code, message, and optional details.

Author: Matthias Morath
"""

# MARK: ━━━ Imports ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
from pydantic import BaseModel, field


# MARK: ━━━ Error Model ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class ErrorModel(BaseModel):
    """Standardized error response structure"""

    code: str = field(
        ..., description="Machine-readable error code (e.g., 'INVALID_INPUT')"
    )
    message: str = field(..., description="Human-readable explanation of the error")
    details: dict | None = field(
        default=None, description="Optional key-value context information"
    )

    model_config = {"extra": "forbid"}


# EOF
