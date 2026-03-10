"""FLEXT Oracle WMS API module.

Provides the main FlextOracleWmsApi class following FLEXT standards with proper inheritance levels.
Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import ClassVar

from pydantic import BaseModel, Field


class FlextOracleWmsApiEndpoint(BaseModel):
    """Typed Oracle WMS API endpoint definition."""

    name: str = Field(min_length=1)
    method: str = Field(min_length=1)
    path: str = Field(min_length=1)
    version: str = Field(min_length=1)
    category: str = Field(min_length=1)
    description: str = Field(default="")


class FlextOracleWmsApi:
    """Main Oracle WMS API class following FLEXT standards.

    Provides consolidated API catalog and mock server functionality
    with proper inheritance levels and enterprise patterns.
    """

    FLEXT_ORACLE_WMS_APIS: ClassVar[dict[str, FlextOracleWmsApiEndpoint]] = {
        "test": FlextOracleWmsApiEndpoint(
            name="test",
            method="GET",
            path="/test/",
            version="v1",
            category="test",
            description="Test endpoint",
        )
    }

    class OracleWmsMockServer:
        """Mock server simulating Oracle WMS Cloud API v10 responses."""

    @classmethod
    def create_mock_server(cls) -> OracleWmsMockServer:
        """Create mock server instance.

        Returns:
            Mock server instance

        """
        return cls.OracleWmsMockServer()


FLEXT_ORACLE_WMS_APIS = FlextOracleWmsApi.FLEXT_ORACLE_WMS_APIS
__all__ = ["FLEXT_ORACLE_WMS_APIS", "FlextOracleWmsApi", "FlextOracleWmsApiEndpoint"]
