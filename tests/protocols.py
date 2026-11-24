"""Test protocol definitions for flext-oracle-wms.

Provides TestsFlextOracleWmsProtocols, combining TestsFlextProtocols with
p for test-specific protocol definitions.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsProtocols

from tests import FlextOracleWmsProtocols


class TestsFlextOracleWmsProtocols(FlextTestsProtocols, FlextOracleWmsProtocols):
    """Test protocols combining TestsFlextProtocols and p."""

    class Tests(FlextTestsProtocols.Tests):
        """OracleWms-specific test protocols."""


p = TestsFlextOracleWmsProtocols
__all__: list[str] = ["TestsFlextOracleWmsProtocols", "p"]
