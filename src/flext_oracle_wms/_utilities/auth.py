"""Oracle WMS Authentication utilities.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import base64

from flext_oracle_wms import c, m, p, r, t


class FlextOracleWmsUtilitiesAuth:
    """Authentication utilities for Oracle WMS -- u.OracleWms.Auth.*."""

    class Authenticator:
        """Oracle WMS authenticator with enterprise patterns."""

        def __init__(self, settings: m.OracleWms.AuthSettings) -> None:
            """Initialize authenticator."""
            self.settings = settings
            self._token: str | None = None

        @property
        def normalized_method(self) -> str:
            """Return auth method in canonical lowercase form."""
            return self.settings.method.strip().lower()

        def authenticate(self) -> p.Result[str]:
            """Perform authentication."""
            basic_method = str(c.OracleWms.OracleWMSAuthMethod.BASIC)
            oauth2_method = str(c.OracleWms.OracleWMSAuthMethod.OAUTH2)
            if self.normalized_method == basic_method:
                if not self.settings.username or not self.settings.password:
                    return r[str].fail("Username and password required for basic auth")
                credentials = (
                    f"{self.settings.username}:{self.settings.password}".encode()
                )
                token = base64.b64encode(credentials).decode("ascii")
                self._token = token
                return r[str].ok(token)
            if self.normalized_method == oauth2_method:
                if (
                    not self.settings.oauth2_client_id
                    or not self.settings.oauth2_client_secret
                ):
                    return r[str].fail("OAuth2 credentials required")
                return r[str].fail("OAuth2 not configured")
            return r[str].fail(f"Unsupported auth method: {self.settings.method}")

        def get_auth_headers(self) -> p.Result[t.StrMapping]:
            """Get authentication headers."""
            auth_result = self.authenticate()
            if auth_result.failure:
                return r[t.StrMapping].fail(
                    f"Authentication failed: {auth_result.error}"
                )
            token = auth_result.value
            basic_method = str(c.OracleWms.OracleWMSAuthMethod.BASIC)
            auth_scheme = (
                "Basic" if self.normalized_method == basic_method else "Bearer"
            )
            return r[t.StrMapping].ok({"Authorization": f"{auth_scheme} {token}"})


__all__: list[str] = ["FlextOracleWmsUtilitiesAuth"]
