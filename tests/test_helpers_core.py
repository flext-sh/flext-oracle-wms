"""Unit tests for Oracle WMS utilities module.

Tests FlextOracleWmsUtilities from utilities.py.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

import pytest
from flext_oracle_wms.utilities import FlextOracleWmsUtilities


@pytest.mark.unit
class TestFlextOracleWmsUtilities:
    def test_inherits_from_flext_utilities(self) -> None:
        from flext_core import FlextUtilities

        assert issubclass(FlextOracleWmsUtilities, FlextUtilities)

    def test_has_oracle_wms_namespace(self) -> None:
        assert hasattr(FlextOracleWmsUtilities, "OracleWms")

    def test_module_alias(self) -> None:
        from flext_oracle_wms.utilities import u

        assert u is FlextOracleWmsUtilities
