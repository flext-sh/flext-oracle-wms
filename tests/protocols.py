"""Test protocol definitions for flext-oracle-wms.

Provides TestsFlextOracleWmsProtocols, combining TestsFlextProtocols with
p for test-specific protocol definitions.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_oracle_wms import p
from flext_tests import FlextTestsProtocols


class TestsFlextOracleWmsProtocols(FlextTestsProtocols, p):
    """Test protocols combining TestsFlextProtocols and p."""

    class OracleWms(p.OracleWms):
        """OracleWms test protocols namespace."""

        class Tests:
            """OracleWms-specific test protocols."""


p = TestsFlextOracleWmsProtocols
__all__: list[str] = ["TestsFlextOracleWmsProtocols", "p"]
