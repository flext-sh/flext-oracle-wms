"""Oracle WMS Configuration - Single source of truth using flext-core singleton.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT.

This module provides the SINGLE configuration class for Oracle WMS operations,
properly extending flext-core singleton pattern without duplicating functionality.
"""

from __future__ import annotations

import base64
import warnings
from typing import Self, cast
from urllib.parse import urlparse

from pydantic import Field, SecretStr, field_validator, model_validator
from pydantic_settings import SettingsConfigDict

from flext_core import FlextConfig, FlextResult

# Constants for validation limits
MAX_TIMEOUT_SECONDS = 300
MAX_RETRIES = 10
MIN_TIMEOUT_SECONDS = 5
MAX_CONNECTION_POOL_SIZE = 50
MAX_CACHE_DURATION_SECONDS = 86400


class FlextOracleWmsConfig(FlextConfig):
    """Single Pydantic 2 Settings class for flext-oracle-wms extending FlextConfig.

    Follows standardized pattern:
    - Extends FlextConfig from flext-core
    - No nested classes within Config
    - All defaults from FlextOracleWmsConstants
    - Uses enhanced singleton pattern with inverse dependency injection
    - Uses Pydantic 2.11+ features (field_validator, model_validator)
    """

    model_config = SettingsConfigDict(
        env_prefix="FLEXT_ORACLE_WMS_",
        case_sensitive=False,
        extra="allow",
        # Inherit enhanced Pydantic 2.11+ features from FlextConfig
        validate_assignment=True,
        str_strip_whitespace=True,
        json_schema_extra={
            "title": "FLEXT Oracle WMS Configuration",
            "description": "Oracle WMS integration configuration extending FlextConfig",
        },
    )

    # Oracle WMS Connection Configuration using FlextOracleWmsConstants for defaults
    oracle_wms_base_url: str = Field(
        default="https://ta29.wms.ocs.oraclecloud.com/raizen_test",
        description="Oracle WMS base URL",
    )

    oracle_wms_username: str = Field(
        default="",
        description="Oracle WMS username",
    )

    oracle_wms_password: SecretStr = Field(
        default_factory=lambda: SecretStr(""),
        description="Oracle WMS password (sensitive)",
    )

    api_version: str = Field(
        default="LGF_V10",
        description="Oracle WMS API version",
    )

    auth_method: str = Field(
        default="BASIC",
        description="Oracle WMS authentication method",
    )

    # Connection Settings using FlextOracleWmsConstants for defaults
    oracle_wms_timeout: int = Field(
        default=30,
        gt=0,
        le=300,
        description="Oracle WMS request timeout in seconds",
    )

    oracle_wms_max_retries: int = Field(
        default=3,
        ge=0,
        le=10,
        description="Oracle WMS maximum retry attempts",
    )

    oracle_wms_verify_ssl: bool = Field(
        default=True,
        description="Oracle WMS SSL certificate verification",
    )

    # Feature Flags using FlextOracleWmsConstants for defaults
    oracle_wms_enable_logging: bool = Field(
        default=True,
        description="Enable Oracle WMS specific logging",
    )

    oracle_wms_use_mock: bool = Field(
        default=False,
        description="Use internal mock server explicitly (testing only)",
    )

    # Performance Configuration using FlextOracleWmsConstants for defaults
    oracle_wms_connection_pool_size: int = Field(
        default=20,
        ge=1,
        le=100,
        description="Oracle WMS connection pool size",
    )

    oracle_wms_cache_duration: int = Field(
        default=3600,
        ge=0,
        le=86400,
        description="Oracle WMS entity cache duration in seconds",
    )

    # Project Identification
    project_name: str = Field(
        default="flext-oracle-wms",
        description="Project name",
    )

    project_version: str = Field(
        default="0.9.0",
        description="Project version",
    )

    # Pydantic 2.11+ field validators
    @field_validator("oracle_wms_base_url")
    @classmethod
    def validate_oracle_wms_base_url(cls, v: str) -> str:
        """Validate Oracle WMS base URL format."""
        if not v.strip():
            msg = "Oracle WMS base URL cannot be empty"
            raise ValueError(msg)

        # Basic URL format validation
        if not (v.startswith(("http://", "https://"))):
            msg = "Oracle WMS base URL must start with http:// or https://"
            raise ValueError(msg)

        return v.strip()

    @field_validator("oracle_wms_timeout")
    @classmethod
    def validate_oracle_wms_timeout(cls, v: int) -> int:
        """Validate Oracle WMS timeout value."""
        if v <= 0:
            msg = "Oracle WMS timeout must be positive"
            raise ValueError(msg)
        if v > MAX_TIMEOUT_SECONDS:
            warnings.warn(
                f"Very long timeout ({v}s) may cause performance issues",
                UserWarning,
                stacklevel=2,
            )
        return v

    @field_validator("oracle_wms_max_retries")
    @classmethod
    def validate_oracle_wms_max_retries(cls, v: int) -> int:
        """Validate Oracle WMS max retries value."""
        if v < 0:
            msg = "Oracle WMS max retries cannot be negative"
            raise ValueError(msg)
        if v > MAX_RETRIES:
            warnings.warn(
                f"High retry count ({v}) may cause performance issues",
                UserWarning,
                stacklevel=2,
            )
        return v

    @field_validator("api_version")
    @classmethod
    def validate_api_version(cls, v: str) -> str:
        """Validate API version format."""
        valid_versions = {"LGF_V10", "LGF_V11", "V1", "V2"}
        if v not in valid_versions:
            msg = f"API version must be one of {valid_versions}"
            raise ValueError(msg)
        return v

    @field_validator("auth_method")
    @classmethod
    def validate_auth_method(cls, v: str) -> str:
        """Validate authentication method."""
        valid_methods = {"BASIC", "BEARER", "API_KEY", "OAUTH2"}
        if v.upper() not in valid_methods:
            msg = f"Auth method must be one of {valid_methods}"
            raise ValueError(msg)
        return v.upper()

    @model_validator(mode="after")
    def validate_oracle_wms_configuration_consistency(self) -> Self:
        """Validate Oracle WMS configuration consistency."""
        # Validate authentication based on method
        if self.auth_method == "BASIC" and (
            not self.oracle_wms_username
            or not self.oracle_wms_password.get_secret_value()
        ):
            msg = "Oracle WMS username and password required for basic auth"
            raise ValueError(msg)

        # Validate mock usage
        if self.oracle_wms_use_mock and not self.oracle_wms_base_url:
            warnings.warn(
                "Oracle WMS base URL is required even when using mock",
                UserWarning,
                stacklevel=2,
            )

        # Validate SSL in production
        if (
            "production" in self.oracle_wms_base_url.lower()
            and not self.oracle_wms_verify_ssl
        ):
            warnings.warn(
                "SSL verification should be enabled for production environments",
                UserWarning,
                stacklevel=2,
            )

        return self

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate Oracle WMS specific business rules."""
        try:
            # Validate authentication requirements
            if self.auth_method == "BASIC" and (
                not self.oracle_wms_username
                or not self.oracle_wms_password.get_secret_value()
            ):
                return FlextResult[None].fail(
                    "Basic auth requires username and password"
                )

            # Validate connection settings
            if self.oracle_wms_timeout < MIN_TIMEOUT_SECONDS:
                return FlextResult[None].fail(
                    f"Timeout too low (minimum {MIN_TIMEOUT_SECONDS} seconds)"
                )

            # Validate pool settings
            if self.oracle_wms_connection_pool_size > MAX_CONNECTION_POOL_SIZE:
                return FlextResult[None].fail(
                    f"Connection pool too large (maximum {MAX_CONNECTION_POOL_SIZE})"
                )

            # Validate cache settings
            if self.oracle_wms_cache_duration > MAX_CACHE_DURATION_SECONDS:
                return FlextResult[None].fail(
                    "Cache duration too long (maximum 24 hours)"
                )

            return FlextResult[None].ok(None)
        except Exception as e:
            return FlextResult[None].fail(f"Business rules validation failed: {e}")

    def get_connection_config(self) -> dict[str, object]:
        """Get Oracle WMS connection configuration context."""
        return {
            "base_url": self.oracle_wms_base_url,
            "username": self.oracle_wms_username,
            "timeout": self.oracle_wms_timeout,
            "max_retries": self.oracle_wms_max_retries,
            "verify_ssl": self.oracle_wms_verify_ssl,
            "pool_size": self.oracle_wms_connection_pool_size,
        }

    def get_auth_config(self) -> dict[str, object]:
        """Get Oracle WMS authentication configuration context."""
        return {
            "auth_method": self.auth_method,
            "username": self.oracle_wms_username,
            "api_version": self.api_version,
        }

    def get_performance_config(self) -> dict[str, object]:
        """Get Oracle WMS performance configuration context."""
        return {
            "timeout": self.oracle_wms_timeout,
            "max_retries": self.oracle_wms_max_retries,
            "pool_size": self.oracle_wms_connection_pool_size,
            "cache_duration": self.oracle_wms_cache_duration,
        }

    def get_feature_config(self) -> dict[str, object]:
        """Get Oracle WMS feature configuration context."""
        return {
            "enable_logging": self.oracle_wms_enable_logging,
            "use_mock": self.oracle_wms_use_mock,
            "verify_ssl": self.oracle_wms_verify_ssl,
        }

    def get_auth_headers(self) -> dict[str, str]:
        """Get authentication headers based on configuration."""
        headers: dict[str, str] = {}

        if self.auth_method == "BASIC":
            credentials = f"{self.oracle_wms_username}:{self.oracle_wms_password.get_secret_value()}"
            encoded_credentials = base64.b64encode(credentials.encode()).decode()
            headers["Authorization"] = f"Basic {encoded_credentials}"

        return headers

    def build_endpoint_url(self, path: str) -> str:
        """Build full endpoint URL."""
        base = self.oracle_wms_base_url.rstrip("/")
        path = path.lstrip("/")
        return f"{base}/{path}"

    def extract_environment_from_url(self) -> str:
        """Extract environment from Oracle WMS base URL."""
        try:
            parsed = urlparse(self.oracle_wms_base_url)
            path_parts = parsed.path.strip("/").split("/")
            if path_parts and path_parts[-1]:
                parsed_env = path_parts[-1].lower()
                # Map to valid environments
                if parsed_env in {"prod", "production"}:
                    return "production"
                if parsed_env in {"stage", "staging"}:
                    return "staging"
                if parsed_env in {"test", "testing", "raizen_test", "test_env"}:
                    return "test"
                if parsed_env == "local":
                    return "local"
                return "development"
        except (ValueError, TypeError, AttributeError, IndexError):
            pass
        return "development"

    @classmethod
    def create_for_environment(
        cls, environment: str, **overrides: object
    ) -> FlextOracleWmsConfig:
        """Create configuration for specific environment using enhanced singleton pattern."""
        return cast(
            "FlextOracleWmsConfig",
            cls.get_or_create_shared_instance(
                project_name="flext-oracle-wms", environment=environment, **overrides
            ),
        )

    @classmethod
    def create_default(cls) -> FlextOracleWmsConfig:
        """Create default configuration instance using enhanced singleton pattern."""
        return cast(
            "FlextOracleWmsConfig",
            cls.get_or_create_shared_instance(project_name="flext-oracle-wms"),
        )

    @classmethod
    def create_for_development(cls) -> FlextOracleWmsConfig:
        """Create configuration optimized for development using enhanced singleton pattern."""
        return cast(
            "FlextOracleWmsConfig",
            cls.get_or_create_shared_instance(
                project_name="flext-oracle-wms",
                oracle_wms_timeout=10,
                oracle_wms_max_retries=1,
                oracle_wms_verify_ssl=False,
                oracle_wms_enable_logging=True,
                oracle_wms_use_mock=True,
                oracle_wms_connection_pool_size=5,
                oracle_wms_cache_duration=300,
            ),
        )

    @classmethod
    def create_for_production(cls) -> FlextOracleWmsConfig:
        """Create configuration optimized for production using enhanced singleton pattern."""
        return cast(
            "FlextOracleWmsConfig",
            cls.get_or_create_shared_instance(
                project_name="flext-oracle-wms",
                oracle_wms_timeout=60,
                oracle_wms_max_retries=5,
                oracle_wms_verify_ssl=True,
                oracle_wms_enable_logging=True,
                oracle_wms_use_mock=False,
                oracle_wms_connection_pool_size=20,
                oracle_wms_cache_duration=3600,
            ),
        )

    @classmethod
    def create_for_testing(cls) -> FlextOracleWmsConfig:
        """Create configuration optimized for testing using enhanced singleton pattern."""
        return cast(
            "FlextOracleWmsConfig",
            cls.get_or_create_shared_instance(
                project_name="flext-oracle-wms",
                oracle_wms_base_url="https://test.example.com",
                oracle_wms_username="test_user",
                oracle_wms_password=SecretStr("test_password"),
                api_version="LGF_V10",
                auth_method="BASIC",
                oracle_wms_timeout=5,
                oracle_wms_max_retries=1,
                oracle_wms_verify_ssl=False,
                oracle_wms_enable_logging=False,
                oracle_wms_use_mock=True,
                oracle_wms_connection_pool_size=2,
                oracle_wms_cache_duration=60,
            ),
        )

    @classmethod
    def get_global_instance(cls) -> FlextOracleWmsConfig:
        """Get the global singleton instance using enhanced FlextConfig pattern."""
        return cast(
            "FlextOracleWmsConfig",
            cls.get_or_create_shared_instance(project_name="flext-oracle-wms"),
        )

    @classmethod
    def reset_global_instance(cls) -> None:
        """Reset the global FlextOracleWmsConfig instance (mainly for testing)."""
        # Use the enhanced FlextConfig reset mechanism
        cls.reset_shared_instance()


class FlextOracleWmsModuleConfig:
    """Module-level configuration for flext-oracle-wms.

    This class holds configuration that is specific to the module
    and not necessarily tied to environment variables.
    """

    def __init__(self) -> None:
        """Initialize module-level configuration with default values."""
        self.enable_caching: bool = True
        self.cache_ttl_seconds: int = 3600
        self.max_concurrent_requests: int = 10
        self.enable_metrics: bool = True
        self.enable_tracing: bool = False


# Backward compatibility aliases
FlextOracleWmsClientConfig = FlextOracleWmsConfig

__all__ = [
    "MAX_CACHE_DURATION_SECONDS",
    "MAX_CONNECTION_POOL_SIZE",
    "MAX_RETRIES",
    "MAX_TIMEOUT_SECONDS",
    "MIN_TIMEOUT_SECONDS",
    "FlextOracleWmsClientConfig",
    "FlextOracleWmsConfig",
    "FlextOracleWmsModuleConfig",
]
