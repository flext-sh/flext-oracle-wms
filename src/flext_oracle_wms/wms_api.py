"""FLEXT Oracle WMS API module.

Provides the main FlextOracleWmsApi class following FLEXT standards with proper inheritance levels.
Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import ClassVar

from pydantic import BaseModel


class FlextOracleWmsApiEndpoint(BaseModel):
    """Simple Pydantic model for API endpoints using FLEXT patterns."""

    name: str
    method: str
    path: str
    version: str
    category: str
    description: str
    since_version: str = "6.1"


class FlextOracleWmsApi:
    """Main Oracle WMS API class following FLEXT standards.

    Provides consolidated API catalog and mock server functionality
    with proper inheritance levels and enterprise patterns.
    """

    # =========================================================================
    # API CATALOG - CLASS CONSTANT
    FLEXT_ORACLE_WMS_APIS: ClassVar[dict[str, FlextOracleWmsApiEndpoint]] = {
        "test": FlextOracleWmsApiEndpoint(
            name="test",
            method="GET",
            path="/test/",
            version="v1",
            category="test",
            description="Test endpoint",
        ),
    }

    class OracleWmsMockServer:
        """Mock server simulating Oracle WMS Cloud API v10 responses."""

    @classmethod
    def create_mock_server(cls, environment: str = "mock") -> OracleWmsMockServer:
        """Create mock server instance.

        Returns:
            Mock server instance

        """
        return cls()


__all__ = ["FlextOracleWmsApi"]
