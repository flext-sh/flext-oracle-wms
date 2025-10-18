"""FLEXT Oracle WMS Authentication module.

Provides authentication classes and configurations for Oracle WMS Cloud integration.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextResult
from pydantic import BaseModel, Field

from flext_oracle_wms.constants import OracleWMSAuthMethod


class FlextOracleWmsAuthConfig(BaseModel):
    """Oracle WMS authentication configuration."""

    method: OracleWMSAuthMethod = Field(default=OracleWMSAuthMethod.BASIC)
    username: str | None = Field(default=None)
    password: str | None = Field(default=None)
    oauth2_client_id: str | None = Field(default=None)
    oauth2_client_secret: str | None = Field(default=None)
    oauth2_scope: str = Field(default="wms.read wms.write")
    token_refresh_threshold: int = Field(default=300)  # 5 minutes

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate auth configuration."""
        errors = []
        if self.method == OracleWMSAuthMethod.BASIC:
            if not self.username or not self.password:
                errors.append("Username and password required for basic auth")
        elif self.method == OracleWMSAuthMethod.OAUTH2:
            if not self.oauth2_client_id or not self.oauth2_client_secret:
                errors.append("OAuth2 credentials required")
        return (
            FlextResult[None].fail("; ".join(errors))
            if errors
            else FlextResult[None].ok(None)
        )


class FlextOracleWmsAuthenticator:
    """Oracle WMS authenticator with enterprise patterns."""

    def __init__(self, config: FlextOracleWmsAuthConfig) -> None:
        """Initialize authenticator."""
        self.config = config
        self._token: str | None = None

    def authenticate(self) -> FlextResult[str]:
        """Perform authentication."""
        if self.config.method == OracleWMSAuthMethod.BASIC:
            if not self.config.username or not self.config.password:
                return FlextResult.fail("Username and password required for basic auth")
            # Basic auth logic would go here
            return FlextResult.ok("basic_token_placeholder")

        if self.config.method == OracleWMSAuthMethod.OAUTH2:
            if not self.config.oauth2_client_id or not self.config.oauth2_client_secret:
                return FlextResult.fail("OAuth2 credentials required")
            # OAuth2 logic would go here
            return FlextResult.ok("oauth2_token_placeholder")

        return FlextResult.fail(f"Unsupported auth method: {self.config.method}")

    def get_auth_headers(self) -> FlextResult[dict[str, str]]:
        """Get authentication headers."""
        auth_result = self.authenticate()
        if auth_result.is_failure:
            return FlextResult.fail(f"Authentication failed: {auth_result.error}")

        token = auth_result.unwrap()
        return FlextResult.ok({"Authorization": f"Bearer {token}"})


def create_oracle_wms_client(config: FlextOracleWmsAuthConfig) -> FlextResult[object]:
    """Create authenticated Oracle WMS client."""
    authenticator = FlextOracleWmsAuthenticator(config)
    auth_result = authenticator.authenticate()
    if auth_result.is_failure:
        return FlextResult.fail(f"Authentication failed: {auth_result.error}")
    # Client creation logic would go here
    return FlextResult.ok("client_placeholder")


__all__ = [
    "FlextOracleWmsAuthConfig",
    "FlextOracleWmsAuthenticator",
    "create_oracle_wms_client",
]
