"""Test protocol definitions for flext-oracle-wms.

Provides TestsFlextOracleWmsProtocols, combining p with
FlextOracleWmsProtocols for test-specific protocol definitions.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import p

from flext_oracle_wms.protocols import FlextOracleWmsProtocols


class TestsFlextOracleWmsProtocols(p, FlextOracleWmsProtocols):
    """Test protocols combining p and FlextOracleWmsProtocols.

    Provides access to:
    - p.Tests.Docker.* (from p)
    - p.Tests.Factory.* (from p)
    - p.OracleWms.* (from FlextOracleWmsProtocols)
    """

    class Tests:
        """Project-specific test protocols.

        Extends p.Tests with OracleWms-specific protocols.
        """

        class OracleWms:
            """OracleWms-specific test protocols."""


__all__ = ["TestsFlextOracleWmsProtocols", "p"]

p = TestsFlextOracleWmsProtocols
