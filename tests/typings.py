"""Test type definitions for flext-oracle-wms.

Provides TestsFlextOracleWmsTypes, combining TestsFlextTypes with
FlextOracleWmsTypes for test-specific type definitions.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsTypes

from flext_oracle_wms import FlextOracleWmsTypes


class TestsFlextOracleWmsTypes(FlextTestsTypes, FlextOracleWmsTypes):
    """Test types combining TestsFlextTypes with flext-oracle-wms types."""

    class OracleWms(FlextOracleWmsTypes.OracleWms):
        """Oracle WMS domain test type aliases."""

        class Tests(FlextTestsTypes.Tests):
            """Oracle WMS-specific test type aliases."""

            type EnvConfig = FlextOracleWmsTypes.ContainerMapping


t = TestsFlextOracleWmsTypes

__all__ = ["TestsFlextOracleWmsTypes", "t"]
