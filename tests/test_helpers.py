"""Tests for Oracle WMS utilities module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import pytest
from flext_core import FlextUtilities

from tests import u


@pytest.mark.unit
class TestFlextOracleWmsUtilities:
    """Test FlextOracleWmsUtilities class."""

    def test_utilities_class_exists(self) -> None:
        """Test that u is importable."""
        assert u is not None

    def test_utilities_has_oracle_wms_namespace(self) -> None:
        """Test OracleWms namespace class exists."""
        assert hasattr(u, "OracleWms")

    def test_utilities_inherits_flext_utilities(self) -> None:
        """Test inheritance from FlextUtilities."""
        assert issubclass(u, FlextUtilities)
