"""Test type definitions for flext-oracle-wms.

Provides TestsFlextOracleWmsTypes, combining TestsFlextTypes with
t for test-specific type definitions.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsTypes

from flext_oracle_wms import t
from flext_oracle_wms.utilities import FlextOracleWmsUtilitiesClient


class TestsFlextOracleWmsTypes(FlextTestsTypes, t):
    """Test types combining TestsFlextTypes with flext-oracle-wms types."""

    class OracleWms(t.OracleWms):
        """Oracle WMS domain test type aliases."""

        class Tests(FlextTestsTypes.Tests):
            """Oracle WMS-specific test type aliases."""

            type Client = FlextOracleWmsUtilitiesClient.Client
            type EnvConfig = t.MetadataMapping
            type Record = t.MutableMappingKV[str, str | int]


t = TestsFlextOracleWmsTypes

__all__: list[str] = ["TestsFlextOracleWmsTypes", "t"]
