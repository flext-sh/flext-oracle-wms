"""Unified Oracle WMS Configuration - Using flext-core patterns correctly.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT.

This module provides a SINGLE unified configuration class that properly uses
flext-core patterns instead of duplicating functionality.
"""

from __future__ import annotations

import base64

from flext_core import FlextConfig, FlextResult, FlextTypes
from pydantic import Field, field_validator

from flext_oracle_wms.wms_constants import FlextOracleWmsApiVersion, OracleWMSAuthMethod


class FlextOracleWmsUnifiedConfig(FlextConfig):
    """Unified Oracle WMS configuration using flext-core patterns correctly.

    This is the SINGLE configuration class that replaces all the duplicated
    configuration classes. It properly extends flext-core instead of
    duplicating functionality.
    """

    # Oracle WMS specific fields
    oracle_wms_base_url: str = Field(..., description="Oracle WMS base URL")
    oracle_wms_username: str = Field(..., description="Oracle WMS username")
    oracle_wms_password: str = Field(..., description="Oracle WMS password")
    api_version: FlextOracleWmsApiVersion = Field(
        default=FlextOracleWmsApiVersion.LGF_V10,
        description="API version",
    )
    auth_method: OracleWMSAuthMethod = Field(
        default=OracleWMSAuthMethod.BASIC,
        description="Authentication method",
    )

    # Connection settings
    timeout: int = Field(default=30, description="Request timeout in seconds")
    max_retries: int = Field(default=3, description="Maximum retry attempts")
    verify_ssl: bool = Field(default=True, description="Verify SSL certificates")

    # Feature flags
    enable_logging: bool = Field(default=True, description="Enable logging")
    use_mock: bool = Field(
        default=False,
        description="Use internal mock server explicitly (testing only)",
    )

    @field_validator("oracle_wms_base_url")
    @classmethod
    def validate_base_url(cls, v: str) -> str:
        """Validate base URL format."""
        if not v.startswith(("http://", "https://")):
            msg = "Base URL must start with http:// or https://"
            raise ValueError(msg)
        return v

    @field_validator("timeout")
    @classmethod
    def validate_timeout(cls, v: int) -> int:
        """Validate timeout value."""
        if v <= 0:
            msg = "Timeout must be greater than 0"
            raise ValueError(msg)
        return v

    @field_validator("max_retries")
    @classmethod
    def validate_max_retries(cls, v: int) -> int:
        """Validate max retries value."""
        if v < 0:
            msg = "Max retries cannot be negative"
            raise ValueError(msg)
        return v

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate Oracle WMS specific business rules."""
        validation_errors = []

        # Validate authentication based on method
        if self.auth_method == OracleWMSAuthMethod.BASIC:
            if not self.oracle_wms_username or not self.oracle_wms_password:
                validation_errors.append("Username and password required for basic auth")
        elif self.auth_method == OracleWMSAuthMethod.BEARER:
            # Add bearer token validation if needed
            pass
        elif self.auth_method == OracleWMSAuthMethod.API_KEY:
            # Add API key validation if needed
            pass

        # Validate mock usage
        if self.use_mock and not self.oracle_wms_base_url:
            validation_errors.append("Base URL is required even when using mock")

        if validation_errors:
            return FlextResult[None].fail("; ".join(validation_errors))
        return FlextResult[None].ok(None)

    class _AuthHelper:
        """Nested helper for authentication operations."""

        @staticmethod
        def get_auth_headers(config: FlextOracleWmsUnifiedConfig) -> FlextTypes.Core.Headers:
            """Get authentication headers based on configuration."""
            headers = {}

            if config.auth_method == OracleWMSAuthMethod.BASIC:
                credentials = f"{config.oracle_wms_username}:{config.oracle_wms_password}"
                encoded_credentials = base64.b64encode(credentials.encode()).decode()
                headers["Authorization"] = f"Basic {encoded_credentials}"

            return headers

    class _ConnectionHelper:
        """Nested helper for connection operations."""

        @staticmethod
        def build_endpoint_url(config: FlextOracleWmsUnifiedConfig, path: str) -> str:
            """Build full endpoint URL."""
            base = config.oracle_wms_base_url.rstrip("/")
            path = path.lstrip("/")
            return f"{base}/{path}"

    # Convenience methods using nested helpers
    def get_auth_headers(self) -> FlextTypes.Core.Headers:
        """Get authentication headers."""
        return self._AuthHelper.get_auth_headers(self)

    def build_endpoint_url(self, path: str) -> str:
        """Build full endpoint URL."""
        return self._ConnectionHelper.build_endpoint_url(self, path)
