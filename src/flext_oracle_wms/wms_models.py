"""FLEXT Oracle WMS Models - Pydantic v2 namespaced models.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextResult as r
from flext_core.models import FlextModels
from pydantic import BaseModel, Field

from flext_oracle_wms.constants import FlextOracleWmsConstants


class FlextOracleWmsModels(FlextModels):
    """Oracle WMS models with namespaced OracleWms domain.

    Access via m.OracleWms.Entity, m.OracleWms.ApiResponse after inheritance.
    """

    def __init_subclass__(cls, **kwargs: object) -> None:
        """Allow downstream projects to inherit FlextOracleWmsModels for namespace composition."""
        super().__init_subclass__(**kwargs)

    class OracleWms:
        """Oracle WMS domain namespace — m.OracleWms.*."""

        class Entity(FlextModels.Entity):
            """WMS entity with validation."""

            name: str = Field(min_length=1)
            endpoint: str = Field(pattern=r"^/")
            description: str | None = None
            primary_key: str | None = None
            replication_key: str | None = None
            supports_incremental: bool = False

            def validate_entity(self) -> r[bool]:
                """Validate using FLEXT patterns."""
                if (
                    len(self.name)
                    > FlextOracleWmsConstants.WmsEntities.MAX_ENTITY_NAME_LENGTH
                ):
                    return r.fail("Entity name too long")
                return r.ok(True)

        class ApiResponse(BaseModel):
            """API response model."""

            data: dict = Field(default_factory=dict)
            status_code: int = Field(default=200, ge=200, le=599)
            success: bool = True
            error_message: str | None = None

            def validate_response(self) -> r[bool]:
                """Validate using railway pattern."""
                if not self.success and not self.error_message:
                    return r.fail("Failed response needs error message")
                return r.ok(True)


# Backward compatibility — use m.OracleWms.Entity in new code
FlextOracleWmsEntity = FlextOracleWmsModels.OracleWms.Entity
FlextOracleWmsApiResponse = FlextOracleWmsModels.OracleWms.ApiResponse

m = FlextOracleWmsModels

__all__ = [
    "FlextOracleWmsApiResponse",
    "FlextOracleWmsEntity",
    "FlextOracleWmsModels",
    "m",
]
