"""Test protocol definitions for flext-oracle-wms.

Provides TestsFlextOracleWmsProtocols, combining TestsFlextProtocols with
FlextOracleWmsProtocols for test-specific protocol definitions.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsProtocols

from flext_oracle_wms import FlextOracleWmsProtocols


class TestsFlextOracleWmsProtocols(FlextTestsProtocols, FlextOracleWmsProtocols):
    """Test protocols combining TestsFlextProtocols and FlextOracleWmsProtocols."""

    class OracleWms(FlextOracleWmsProtocols.OracleWms):
        """OracleWms test protocols namespace."""

        class Tests:
            """OracleWms-specific test protocols."""


p = TestsFlextOracleWmsProtocols
__all__: list[str] = ["TestsFlextOracleWmsProtocols", "p"]
