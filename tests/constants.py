"""Test constants for flext-oracle-wms tests.

Provides TestsFlextOracleWmsConstants, extending FlextTestsConstants with
flext-oracle-wms-specific constants.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from enum import StrEnum, unique
from typing import Final

from flext_tests import FlextTestsConstants

from flext_oracle_wms import c


@unique
class OracleWmsCategoryEnum(StrEnum):
    """Oracle WMS API category classifications."""

    DATA_EXTRACT = "data_extract"
    ENTITY_OPERATIONS = "entity_operations"
    SETUP_TRANSACTIONAL = "setup_transactional"
    AUTOMATION_OPERATIONS = "automation_operations"


class TestsFlextOracleWmsConstants(FlextTestsConstants, c):
    """Test constants for flext-oracle-wms."""

    class OracleWms(c.OracleWms):
        """Oracle WMS domain test constants namespace."""

        class Tests(FlextTestsConstants.Tests):
            """Oracle WMS-specific test constants."""

            Categories: type[OracleWmsCategoryEnum] = OracleWmsCategoryEnum
            "Oracle WMS API category classifications (data_extract, entity_operations, setup_transactional, automation_operations)."

            API_VERSION_LGF_V10: Final[str] = "LGF_V10"
            "Oracle WMS LGF API version 10 identifier."


c = TestsFlextOracleWmsConstants
__all__: list[str] = ["TestsFlextOracleWmsConstants", "c"]
