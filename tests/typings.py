"""Test type definitions for flext-oracle-wms.

Provides TestsFlextOracleWmsTypes, combining TestsFlextTypes with
t for test-specific type definitions.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_tests import FlextTestsTypes

from tests import FlextOracleWmsTypes

if TYPE_CHECKING:
    from tests import FlextOracleWmsUtilities


class TestsFlextOracleWmsTypes(FlextTestsTypes, FlextOracleWmsTypes):
    """Test types combining TestsFlextTypes with flext-oracle-wms types."""

    class Tests(FlextTestsTypes.Tests):
        """Oracle WMS-specific test type aliases."""

        type Client = FlextOracleWmsUtilities.OracleWms.Client
        type EnvConfig = FlextOracleWmsTypes.MetadataMapping


t = TestsFlextOracleWmsTypes

__all__: list[str] = ["TestsFlextOracleWmsTypes", "t"]
