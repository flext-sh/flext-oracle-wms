"""Test constants for flext-oracle-wms tests.

Provides TestsFlextOracleWmsConstants, extending FlextTestsConstants with
flext-oracle-wms-specific constants.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsConstants

from flext_oracle_wms import FlextOracleWmsConstants


class TestsFlextOracleWmsConstants(FlextTestsConstants, FlextOracleWmsConstants):
    """Test constants for flext-oracle-wms."""

    class OracleWms(FlextOracleWmsConstants.OracleWms):
        """Oracle WMS domain test constants namespace."""

        class Tests(FlextTestsConstants.Tests):
            """Oracle WMS-specific test constants."""


c = TestsFlextOracleWmsConstants
__all__: list[str] = ["TestsFlextOracleWmsConstants", "c"]
