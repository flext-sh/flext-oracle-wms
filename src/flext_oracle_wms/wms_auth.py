"""FLEXT Oracle WMS Authentication module.

Provides authentication classes and configurations for Oracle WMS Cloud integration.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping

import base64

from flext_core import r

from flext_oracle_wms import OracleWMSAuthMethod, m


class FlextOracleWmsAuthenticator:
    """Oracle WMS authenticator with enterprise patterns."""

    def __init__(self, config: m.OracleWms.AuthSettings) -> None:
        """Initialize authenticator."""
        self.config = config
        self._token: str | None = None

    def authenticate(self) -> r[str]:
        """Perform authentication."""
        if self.config.method == OracleWMSAuthMethod.BASIC:
            if not self.config.username or not self.config.password:
                return r[str].fail("Username and password required for basic auth")
            credentials = f"{self.config.username}:{self.config.password}".encode()
            token = base64.b64encode(credentials).decode("ascii")
            self._token = token
            return r[str].ok(token)
        if self.config.method == OracleWMSAuthMethod.OAUTH2:
            if not self.config.oauth2_client_id or not self.config.oauth2_client_secret:
                return r[str].fail("OAuth2 credentials required")
            return r[str].fail("OAuth2 not configured")
        return r[str].fail(f"Unsupported auth method: {self.config.method}")

    def get_auth_headers(self) -> r[Mapping[str, str]]:
        """Get authentication headers."""
        auth_result = self.authenticate()
        if auth_result.is_failure:
            return r[Mapping[str, str]].fail(
                f"Authentication failed: {auth_result.error}"
            )
        token = auth_result.value
        auth_scheme = (
            "Basic" if self.config.method == OracleWMSAuthMethod.BASIC else "Bearer"
        )
        return r[Mapping[str, str]].ok({"Authorization": f"{auth_scheme} {token}"})


def create_oracle_wms_client(config: m.OracleWms.AuthSettings) -> r[str]:
    """Create authenticated Oracle WMS client."""
    authenticator = FlextOracleWmsAuthenticator(config)
    auth_result = authenticator.authenticate()
    if auth_result.is_failure:
        return r[str].fail(f"Authentication failed: {auth_result.error}")
    return r[str].fail("Oracle WMS client creation not configured")


FlextOracleWmsAuthSettings = m.OracleWms.AuthSettings

__all__ = [
    "FlextOracleWmsAuthSettings",
    "FlextOracleWmsAuthenticator",
    "create_oracle_wms_client",
]
