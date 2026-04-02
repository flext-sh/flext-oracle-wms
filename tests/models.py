"""Test models for flext-oracle-wms.

Provides FlextOracleWmsTestModels, combining FlextTestsModels with
FlextOracleWmsModels for test-specific model definitions.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsModels

from flext_oracle_wms import FlextOracleWmsModels


class FlextOracleWmsTestModels(FlextTestsModels, FlextOracleWmsModels):
    """Test models combining FlextTestsModels with flext-oracle-wms models."""

    class OracleWms(FlextOracleWmsModels.OracleWms):
        """Oracle WMS domain test models namespace."""

        class Tests(FlextTestsModels.Tests):
            """Oracle WMS-specific test fixtures."""


m = FlextOracleWmsTestModels

__all__ = [
    "FlextOracleWmsTestModels",
    "m",
]
