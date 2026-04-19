"""Test models for flext-oracle-wms.

Provides TestsFlextOracleWmsModels, combining TestsFlextModels with
m for test-specific model definitions.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsModels

from flext_oracle_wms import m


class TestsFlextOracleWmsModels(FlextTestsModels, m):
    """Test models combining TestsFlextModels with flext-oracle-wms models."""

    class OracleWms(m.OracleWms):
        """Oracle WMS domain test models namespace."""

        class Tests(FlextTestsModels.Tests):
            """Oracle WMS-specific test fixtures."""


m = TestsFlextOracleWmsModels

__all__: list[str] = [
    "TestsFlextOracleWmsModels",
    "m",
]
