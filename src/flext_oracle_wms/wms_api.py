"""FLEXT Oracle WMS API module.

Provides the main FlextOracleWmsApi class following FLEXT standards with proper inheritance levels.
Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import ClassVar

from flext_oracle_wms.models import FlextOracleWmsModels as m


class FlextOracleWmsApi:
    """Main Oracle WMS API class following FLEXT standards.

    Provides consolidated API catalog and mock server functionality
    with proper inheritance levels and enterprise patterns.
    """

    FLEXT_ORACLE_WMS_APIS: ClassVar[Mapping[str, m.OracleWms.ApiEndpoint]] = {
        "test": m.OracleWms.ApiEndpoint(
            name="test",
            method="GET",
            path="/test/",
            version="v1",
            category="test",
            description="Test endpoint",
            since_version="6.1",
        ),
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


__all__ = ["FlextOracleWmsApi"]
