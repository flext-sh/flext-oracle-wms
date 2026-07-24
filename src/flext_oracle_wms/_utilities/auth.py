"""Oracle WMS Authentication utilities.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import base64

from flext_oracle_wms import c, p, r, t


class FlextOracleWmsUtilitiesAuth:
    """Authentication utilities for Oracle WMS -- u.OracleWms.Auth.*."""

    @staticmethod
    def validate_auth_settings(
        auth_settings: p.OracleWms.AuthSettings,
    ) -> p.Result[bool]:
        """Validate Oracle WMS authentication configuration business rules."""
        # NOTE (multi-agent): U17 — business validation lives in u.*, not on the
        # model (declaration layer). Moved verbatim from m.OracleWms.AuthSettings.
        basic_method = str(c.OracleWms.OracleWMSAuthMethod.BASIC)
        oauth2_method = str(c.OracleWms.OracleWMSAuthMethod.OAUTH2)
        if auth_settings.normalized_method == basic_method:
            if not auth_settings.username or not auth_settings.password:
                return r[bool].fail("Basic auth requires username and password")
            return r[bool].ok(True)
        if auth_settings.normalized_method == oauth2_method:
            if (
                not auth_settings.oauth2_client_id
                or not auth_settings.oauth2_client_secret
            ):
                return r[bool].fail("OAuth2 requires client_id and client_secret")
            return r[bool].ok(True)
        return r[bool].fail(f"Unsupported auth method: {auth_settings.method}")

    class Authenticator:
        """Oracle WMS authenticator with enterprise patterns."""

        def __init__(self, settings: p.OracleWms.AuthSettings) -> None:
            """Initialize authenticator with an injected auth value model."""
            # NOTE (multi-agent): mro-rn88 — retain the injected AuthSettings value model;
            # every method consumes it via self._settings (was an unbound bare name).
            self._settings: p.OracleWms.AuthSettings = settings
            self._token: str | None = None

        @property
        def normalized_method(self) -> str:
            """The auth method in canonical lowercase form (from the model)."""
            # NOTE (multi-agent): DRY — consume the model's computed_field, do not
            # re-derive (was a duplicate of m.OracleWms.AuthSettings.normalized_method).
            return str(self._settings.normalized_method)

        def authenticate(self) -> p.Result[str]:
            """Perform authentication."""
            basic_method = str(c.OracleWms.OracleWMSAuthMethod.BASIC)
            oauth2_method = str(c.OracleWms.OracleWMSAuthMethod.OAUTH2)
            if self.normalized_method == basic_method:
                if not self._settings.username or not self._settings.password:
                    return r[str].fail("Username and password required for basic auth")
                credentials = (
                    f"{self._settings.username}:{self._settings.password}".encode()
                )
                token = base64.b64encode(credentials).decode("ascii")
                self._token = token
                return r[str].ok(token)
            if self.normalized_method == oauth2_method:
                if (
                    not self._settings.oauth2_client_id
                    or not self._settings.oauth2_client_secret
                ):
                    return r[str].fail("OAuth2 credentials required")
                return r[str].fail("OAuth2 not configured")
            return r[str].fail(f"Unsupported auth method: {self._settings.method}")

        def get_auth_headers(self) -> p.Result[t.StrMapping]:
            """Return the authentication headers."""
            auth_result = self.authenticate()
            if auth_result.failure:
                return r[t.StrMapping].fail_op("Authentication", auth_result.error)
            token = auth_result.value
            basic_method = str(c.OracleWms.OracleWMSAuthMethod.BASIC)
            auth_scheme = (
                "Basic" if self.normalized_method == basic_method else "Bearer"
            )
            return r[t.StrMapping].ok({"Authorization": f"{auth_scheme} {token}"})


__all__: list[str] = ["FlextOracleWmsUtilitiesAuth"]
