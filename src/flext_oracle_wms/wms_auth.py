"""FLEXT Oracle WMS Authentication module.

Provides authentication classes and configurations for Oracle WMS Cloud integration.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import base64
from collections.abc import Mapping

from flext_core import FlextResult

from flext_oracle_wms.constants import OracleWMSAuthMethod


class FlextOracleWmsAuthenticator:
    """Oracle WMS authenticator with enterprise patterns."""

    def __init__(self, config: FlextOracleWmsAuthSettings) -> None:
        """Initialize authenticator."""
        self.config = config
        self._token: str | None = None

    def authenticate(self) -> FlextResult[str]:
        """Perform authentication."""
        if self.config.method == OracleWMSAuthMethod.BASIC:
            if not self.config.username or not self.config.password:
                return FlextResult.fail("Username and password required for basic auth")

            credentials = f"{self.config.username}:{self.config.password}".encode()
            token = base64.b64encode(credentials).decode("ascii")
            self._token = token
            return FlextResult.ok(token)

        if self.config.method == OracleWMSAuthMethod.OAUTH2:
            if not self.config.oauth2_client_id or not self.config.oauth2_client_secret:
                return FlextResult.fail("OAuth2 credentials required")

            return FlextResult.fail("OAuth2 not configured")

        return FlextResult.fail(f"Unsupported auth method: {self.config.method}")

    def get_auth_headers(self) -> FlextResult[Mapping[str, str]]:
        """Get authentication headers."""
        auth_result = self.authenticate()
        if auth_result.is_failure:
            return FlextResult.fail(f"Authentication failed: {auth_result.error}")

        token = auth_result.value
        auth_scheme = (
            "Basic" if self.config.method == OracleWMSAuthMethod.BASIC else "Bearer"
        )
        return FlextResult.ok({"Authorization": f"{auth_scheme} {token}"})


def create_oracle_wms_client(config: FlextOracleWmsAuthSettings) -> FlextResult[object]:
    """Create authenticated Oracle WMS client."""
    authenticator = FlextOracleWmsAuthenticator(config)
    auth_result = authenticator.authenticate()
    if auth_result.is_failure:
        return FlextResult.fail(f"Authentication failed: {auth_result.error}")

    return FlextResult.fail("Oracle WMS client creation not configured")


__all__ = [
    "FlextOracleWmsAuthSettings",
    "FlextOracleWmsAuthenticator",
    "create_oracle_wms_client",
]
