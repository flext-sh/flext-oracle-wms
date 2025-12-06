"""FLEXT Oracle WMS Models - Direct Pydantic usage.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextResult
from flext_core.models import FlextModels
from pydantic import BaseModel, Field

from flext_oracle_wms.constants import FlextOracleWmsConstants


class FlextOracleWmsModels(FlextModels):
    """Oracle WMS models using direct Pydantic and FLEXT patterns.

    One class per module following SOLID principles.
    Uses FLEXT railway-oriented programming.
    """

    # Core models using Pydantic directly
    class Entity(BaseModel):
        """WMS entity with validation."""

        name: str = Field(min_length=1)
        endpoint: str = Field(pattern=r"^/")
        description: str | None = None
        primary_key: str | None = None
        replication_key: str | None = None
        supports_incremental: bool = False

        def validate_entity(self) -> FlextResult[None]:
            """Validate using FLEXT patterns."""
            if (
                len(self.name)
                > FlextOracleWmsConstants.WmsEntities.MAX_ENTITY_NAME_LENGTH
            ):
                return FlextResult.fail("Entity name too long")
            return FlextResult.ok(None)

    class ApiResponse(BaseModel):
        """API response model."""

        data: dict = Field(default_factory=dict)
        status_code: int = Field(default=200, ge=200, le=599)
        success: bool = True
        error_message: str | None = None

        def validate_response(self) -> FlextResult[None]:
            """Validate using railway pattern."""
            if not self.success and not self.error_message:
                return FlextResult.fail("Failed response needs error message")
            return FlextResult.ok(None)


# Backward compatibility classes with real inheritance
class FlextOracleWmsEntity(FlextOracleWmsModels.Entity):
    """FlextOracleWmsEntity - real inheritance from FlextOracleWmsModels.Entity."""


class FlextOracleWmsApiResponse(FlextOracleWmsModels.ApiResponse):
    """FlextOracleWmsApiResponse - real inheritance from FlextOracleWmsModels.ApiResponse."""


# Type aliases
TOracleWmsRecord = dict[str, object]
TOracleWmsRecordBatch = list[TOracleWmsRecord]

__all__ = [
    "FlextOracleWmsApiResponse",
    "FlextOracleWmsEntity",
    "FlextOracleWmsModels",
    "TOracleWmsRecord",
    "TOracleWmsRecordBatch",
]
