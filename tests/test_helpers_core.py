"""Unit tests for Oracle WMS utilities module.

Tests FlextOracleWmsUtilities from utilities.py.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import pytest
from flext_core import FlextUtilities

from flext_oracle_wms.utilities import FlextOracleWmsUtilities, u


@pytest.mark.unit
class TestFlextOracleWmsUtilities:
    """Test suite for FlextOracleWmsUtilities class."""

    def test_inherits_from_flext_utilities(self) -> None:
        assert issubclass(FlextOracleWmsUtilities, FlextUtilities)

    def test_has_oracle_wms_namespace(self) -> None:
        assert hasattr(FlextOracleWmsUtilities, "OracleWms")

    def test_module_alias(self) -> None:
        assert u is FlextOracleWmsUtilities
