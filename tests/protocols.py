"""Test protocol definitions for flext-oracle-wms.

Provides FlextOracleWmsTestProtocols, combining FlextTestsProtocols with
FlextOracleWmsProtocols for test-specific protocol definitions.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsProtocols

from flext_oracle_wms import FlextOracleWmsProtocols


class FlextOracleWmsTestProtocols(FlextTestsProtocols, FlextOracleWmsProtocols):
    """Test protocols combining FlextTestsProtocols and FlextOracleWmsProtocols."""

    class OracleWms(FlextOracleWmsProtocols.OracleWms):
        """OracleWms test protocols namespace."""

        class Tests:
            """OracleWms-specific test protocols."""


p = FlextOracleWmsTestProtocols
__all__ = ["FlextOracleWmsTestProtocols", "p"]
