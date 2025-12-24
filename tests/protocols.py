"""Test protocol definitions for flext-oracle-wms.

Provides TestsFlextOracleWmsProtocols, combining FlextTestsProtocols with
FlextOracleWmsProtocols for test-specific protocol definitions.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests.protocols import FlextTestsProtocols

from flext_oracle_wms.protocols import FlextOracleWmsProtocols


class TestsFlextOracleWmsProtocols(FlextTestsProtocols, FlextOracleWmsProtocols):
    """Test protocols combining FlextTestsProtocols and FlextOracleWmsProtocols.

    Provides access to:
    - tp.Tests.Docker.* (from FlextTestsProtocols)
    - tp.Tests.Factory.* (from FlextTestsProtocols)
    - tp.OracleWms.* (from FlextOracleWmsProtocols)
    """

    class Tests:
        """Project-specific test protocols.

        Extends FlextTestsProtocols.Tests with OracleWms-specific protocols.
        """

        class OracleWms:
            """OracleWms-specific test protocols."""


# Runtime aliases
p = TestsFlextOracleWmsProtocols
tp = TestsFlextOracleWmsProtocols

__all__ = ["TestsFlextOracleWmsProtocols", "p", "tp"]
