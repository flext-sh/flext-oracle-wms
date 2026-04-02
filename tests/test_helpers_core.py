"""Unit tests for Oracle WMS utilities module.

Tests u from utilities.py.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import pytest

from flext_core import FlextUtilities
from tests import u


@pytest.mark.unit
class TestFlextOracleWmsUtilities:
    """Test suite for FlextOracleWmsUtilities class."""

    def test_inherits_from_flext_utilities(self) -> None:
        assert issubclass(u, FlextUtilities)

    def test_has_oracle_wms_namespace(self) -> None:
        assert hasattr(u, "OracleWms")

    def test_utilities_is_accessible(self) -> None:
        assert u is not None
