"""FLEXT Oracle WMS Configuration module.

Provides the main FlextOracleWmsConfig class following FLEXT standards with proper inheritance levels.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextConfig
from pydantic import Field


class FlextOracleWmsConfig(FlextConfig):
    """Oracle WMS client configuration for enterprise integration.

    Provides comprehensive configuration for Oracle WMS Cloud client connections,
    authentication, timeouts, and enterprise features.
    """

    # Oracle WMS connection settings
    base_url: str = Field(
        default="https://wms.oraclecloud.com", description="Oracle WMS Cloud base URL"
    )
    oracle_wms_base_url: str = Field(
        default="https://wms.oraclecloud.com",
        description="Oracle WMS base URL (alias for base_url)",
    )

    # Authentication settings
    username: str | None = Field(
        default=None, description="Oracle WMS username for authentication"
    )
    password: str | None = Field(
        default=None, description="Oracle WMS password for authentication"
    )
    oracle_wms_username: str | None = Field(
        default=None, description="Oracle WMS username (alias for username)"
    )
    oracle_wms_password: str | None = Field(
        default=None, description="Oracle WMS password (alias for password)"
    )

    # Connection settings
    timeout: int = Field(default=30, description="Request timeout in seconds")
    retry_attempts: int = Field(
        default=3, description="Number of retry attempts for failed requests"
    )
    oracle_wms_timeout: int = Field(
        default=30, description="Oracle WMS timeout (alias for timeout)"
    )
    oracle_wms_max_retries: int = Field(
        default=3, description="Oracle WMS max retries (alias for retry_attempts)"
    )
    enable_ssl_verification: bool = Field(
        default=True, description="Enable SSL certificate verification"
    )
    oracle_wms_verify_ssl: bool = Field(
        default=True,
        description="Oracle WMS SSL verification (alias for enable_ssl_verification)",
    )

    # Enterprise features
    enable_metrics: bool = Field(default=False, description="Enable metrics collection")
    enable_tracing: bool = Field(
        default=False, description="Enable distributed tracing"
    )
    enable_audit_logging: bool = Field(
        default=False, description="Enable audit logging"
    )
    oracle_wms_enable_logging: bool = Field(
        default=False, description="Oracle WMS logging (alias for enable_audit_logging)"
    )

    # API version
    api_version: str = Field(default="v2", description="Oracle WMS API version")

    @classmethod
    def create_default(cls) -> FlextOracleWmsClientConfig:
        """Create default Oracle WMS client configuration.

        Returns:
            Default configuration instance

        """
        return cls()

    # Additional methods for environment management
    @classmethod
    def get_oracle_wms_global_instance(cls) -> FlextOracleWmsConfig:
        """Get the global Oracle WMS configuration instance.

        Returns:
            Global configuration instance

        """
        return cls()

    @classmethod
    def create_for_development(cls) -> FlextOracleWmsConfig:
        """Create development Oracle WMS configuration.

        Returns:
            Development configuration instance

        """
        return cls()

    @classmethod
    def for_testing(cls) -> FlextOracleWmsConfig:
        """Create testing Oracle WMS configuration.

        Returns:
            Testing configuration instance

        """
        return cls()

    def extract_environment_from_url(self) -> str:
        """Extract environment from Oracle WMS URL.

        Returns:
            Environment name

        """
        base_url = self.base_url or self.oracle_wms_base_url
        if "demo" in base_url:
            return "demo"
        if "test" in base_url:
            return "test"
        if "prod" in base_url:
            return "production"
        return "default"


__all__ = ["FlextOracleWmsConfig"]
