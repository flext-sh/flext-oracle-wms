"""Test utilities for flext-oracle-wms.

Provides FlextOracleWmsTestUtilities, combining FlextTestsUtilities with
FlextOracleWmsUtilities for test-specific utility definitions.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsUtilities

from flext_oracle_wms import FlextOracleWmsUtilities


class FlextOracleWmsTestUtilities(FlextTestsUtilities, FlextOracleWmsUtilities):
    """Test utilities combining FlextTestsUtilities with flext-oracle-wms utilities."""

    class OracleWms(FlextOracleWmsUtilities.OracleWms):
        """OracleWms test utilities namespace."""

        class Tests:
            """Internal tests declarations."""


u = FlextOracleWmsTestUtilities
__all__ = ["FlextOracleWmsTestUtilities", "u"]
