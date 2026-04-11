"""Oracle WMS Authentication utilities.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import base64

from flext_core import r
from flext_oracle_wms import (
    c,
    m,
    t,
)


class FlextOracleWmsUtilitiesAuth:
    """Authentication utilities for Oracle WMS -- u.OracleWms.Auth.*."""

    class Authenticator:
        """Oracle WMS authenticator with enterprise patterns."""

        def __init__(self, config: m.OracleWms.AuthSettings) -> None:
            """Initialize authenticator."""
            self.config = config
            self._token: str | None = None

        def authenticate(self) -> r[str]:
            """Perform authentication."""
            if self.config.method == c.OracleWms.OracleWMSAuthMethod.BASIC:
                if not self.config.username or not self.config.password:
                    return r[str].fail("Username and password required for basic auth")
                credentials = f"{self.config.username}:{self.config.password}".encode()
                token = base64.b64encode(credentials).decode("ascii")
                self._token = token
                return r[str].ok(token)
            if self.config.method == c.OracleWms.OracleWMSAuthMethod.OAUTH2:
                if (
                    not self.config.oauth2_client_id
                    or not self.config.oauth2_client_secret
                ):
                    return r[str].fail("OAuth2 credentials required")
                return r[str].fail("OAuth2 not configured")
            return r[str].fail(f"Unsupported auth method: {self.config.method}")

        def get_auth_headers(self) -> r[t.StrMapping]:
            """Get authentication headers."""
            auth_result = self.authenticate()
            if auth_result.failure:
                return r[t.StrMapping].fail(
                    f"Authentication failed: {auth_result.error}"
                )
            token = auth_result.value
            auth_scheme = (
                "Basic"
                if self.config.method == c.OracleWms.OracleWMSAuthMethod.BASIC
                else "Bearer"
            )
            return r[t.StrMapping].ok({"Authorization": f"{auth_scheme} {token}"})


__all__ = ["FlextOracleWmsUtilitiesAuth"]
