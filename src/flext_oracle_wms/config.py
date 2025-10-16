"""FLEXT Oracle WMS Configuration module.

Provides the main FlextOracleWmsConfig class following FLEXT standards with proper inheritance levels.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import FlextConfig
from pydantic import Field

from flext_oracle_wms.constants import FlextOracleWmsConstants


class FlextOracleWmsConfig(FlextConfig):
    """Oracle WMS client configuration for enterprise integration.

    Provides comprehensive configuration for Oracle WMS Cloud client connections,
    authentication, timeouts, and enterprise features.
    """

    # Oracle WMS connection settings
    base_url: str = Field(
        default=FlextOracleWmsConstants.API_BASE_URL_DEFAULT,
        description="Oracle WMS Cloud base URL",
    )

    # Authentication settings
    username: str | None = Field(
        default=None, description="Oracle WMS username for authentication"
    )
    password: str | None = Field(
        default=None, description="Oracle WMS password for authentication"
    )

    # Connection settings
    timeout: int = Field(
        default=FlextOracleWmsConstants.API_TIMEOUT_DEFAULT,
        description="Request timeout in seconds",
    )
    retry_attempts: int = Field(
        default=FlextOracleWmsConstants.API_MAX_RETRIES,
        description="Number of retry attempts for failed requests",
    )
    enable_ssl_verification: bool = Field(
        default=True, description="Enable SSL certificate verification"
    )

    # Enterprise features
    enable_metrics: bool = Field(default=False, description="Enable metrics collection")
    enable_tracing: bool = Field(
        default=False, description="Enable distributed tracing"
    )
    enable_audit_logging: bool = Field(
        default=False, description="Enable audit logging"
    )

    # API version
    api_version: str = Field(
        default=FlextOracleWmsConstants.API_VERSION_DEFAULT,
        description="Oracle WMS API version",
    )

    # Environment settings
    environment: str = Field(
        default=FlextOracleWmsConstants.ENVIRONMENT,
        description="Deployment environment",
    )
    use_mock: bool = Field(default=False, description="Use mock Oracle WMS for testing")


__all__ = ["FlextOracleWmsConfig"]
