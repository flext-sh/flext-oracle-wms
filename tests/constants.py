"""Test constants for flext-oracle-wms tests.

Provides TestsFlextOracleWmsConstants, extending FlextTestsConstants with
flext-oracle-wms-specific constants.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import base64
import secrets
from enum import StrEnum, unique
from typing import ClassVar

from flext_tests import FlextTestsConstants

from flext_oracle_wms import FlextOracleWmsConstants


class TestsFlextOracleWmsConstants(FlextTestsConstants, FlextOracleWmsConstants):
    """Test constants for flext-oracle-wms."""

    class OracleWms(FlextOracleWmsConstants.OracleWms):
        """Oracle WMS domain test constants namespace."""

        class Tests(FlextTestsConstants.Tests):
            """Oracle WMS-specific test constants."""

            @unique
            class Categories(StrEnum):
                """Oracle WMS API category classifications."""

                DATA_EXTRACT = "data_extract"
                ENTITY_OPERATIONS = "entity_operations"
                SETUP_TRANSACTIONAL = "setup_transactional"
                AUTOMATION_OPERATIONS = "automation_operations"

            API_VERSION_LGF_V10: ClassVar[str] = "LGF_V10"
            "Oracle WMS LGF API version 10 identifier."

            BASIC_USERNAME: ClassVar[str] = "test_user"
            "Canonical BASIC username used across authentication tests."
            BASIC_PASSWORD: ClassVar[str] = secrets.token_urlsafe()
            "Generated BASIC password used across authentication tests."
            BASIC_TOKEN: ClassVar[str] = base64.b64encode(
                f"{BASIC_USERNAME}:{BASIC_PASSWORD}".encode(),
            ).decode("ascii")
            "Base64 BASIC token of the canonical username and password."
            WMS_PASSWORD: ClassVar[str] = secrets.token_urlsafe()
            "Generated password for WMS-specific client tests."
            WMS_PASSWORD_UNDERSCORE: ClassVar[str] = secrets.token_urlsafe()
            "Second generated password for WMS-specific client tests."
            TEST_PASS: ClassVar[str] = secrets.token_urlsafe()
            "Generated password for client settings tests."
            CUSTOM_PASSWORD: ClassVar[str] = secrets.token_urlsafe()
            "Generated password for settings-resolution tests."
            SHORT_PASSWORD: ClassVar[str] = secrets.token_urlsafe()
            "Generated password for unsupported-method tests."
            GENERIC_SECRET: ClassVar[str] = secrets.token_urlsafe()
            "Generated client secret for OAuth2 client-secret tests."
            OAUTH_SECRET: ClassVar[str] = secrets.token_urlsafe()
            "Generated canonical OAuth2 client secret."
            OAUTH_SECRET_DASHED: ClassVar[str] = secrets.token_urlsafe()
            "Generated second OAuth2 client secret."
            OAUTH_SECRET_NUMERIC: ClassVar[str] = secrets.token_urlsafe()
            "Generated third OAuth2 client secret."


c = TestsFlextOracleWmsConstants

__all__: list[str] = ["TestsFlextOracleWmsConstants", "c"]
