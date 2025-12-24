"""Test models for flext-oracle-wms tests.

Provides TestsFlextOracleWmsModels, extending FlextTestsModels with
flext-oracle-wms-specific models using COMPOSITION INHERITANCE.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests.models import FlextTestsModels

from flext_oracle_wms.models import FlextWmsModels


class TestsFlextOracleWmsModels(FlextTestsModels, FlextWmsModels):
    """Models for flext-oracle-wms tests using COMPOSITION INHERITANCE.

    MANDATORY: Inherits from BOTH:
    1. FlextTestsModels - for test infrastructure (.Tests.*)
    2. FlextWmsModels - for domain models

    Access patterns:
    - tm.Tests.* (generic test models from FlextTestsModels)
    - tm.* (Oracle WMS domain models)
    - m.* (production models via alternative alias)
    """

    class Tests:
        """Project-specific test fixtures namespace."""

        class OracleWms:
            """Oracle WMS-specific test fixtures."""


# Short aliases per FLEXT convention
tm = TestsFlextOracleWmsModels
m = TestsFlextOracleWmsModels

__all__ = [
    "TestsFlextOracleWmsModels",
    "m",
    "tm",
]
