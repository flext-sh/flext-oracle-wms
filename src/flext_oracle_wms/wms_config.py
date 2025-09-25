"""Oracle WMS Configuration - Single source of truth using flext-core singleton.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT.

This module provides the SINGLE configuration class for Oracle WMS operations,
properly extending flext-core singleton pattern without duplicating functionality.
"""

from __future__ import annotations

import base64
import os
from pathlib import Path
from typing import ClassVar
from urllib.parse import urlparse

from pydantic import Field, field_validator

from flext_core import FlextConfig, FlextModels, FlextResult, FlextTypes
from flext_oracle_wms.wms_constants import FlextOracleWmsConstants


class FlextOracleWmsConfig(FlextConfig):
    """Oracle WMS configuration - Single source of truth using flext-core singleton.

    This is the ONLY configuration class for Oracle WMS operations.
    Properly extends flext-core singleton pattern without duplicating functionality.

    Uses the global singleton instance from flext-core as the base configuration,
    adding Oracle WMS specific fields on top of the core configuration.

    The singleton pattern allows parameters to be passed to change behavior
    while maintaining a single source of truth for configuration.
    """

    # Class attribute for singleton instance
    _oracle_wms_global_instance: ClassVar[FlextOracleWmsConfig | None] = None

    # Oracle WMS specific fields - extend the base FlextConfig
    oracle_wms_base_url: str = Field(
        default="https://ta29.wms.ocs.oraclecloud.com/raizen_test",
        description="Oracle WMS base URL",
    )
    oracle_wms_username: str = Field(
        default="USER_WMS_INTEGRA",
        description="Oracle WMS username",
    )
    oracle_wms_password: str = Field(
        default="jmCyS7BK94YvhS@",
        description="Oracle WMS password",
    )
    api_version: FlextOracleWmsApiVersion = Field(
        default=FlextOracleWmsApiVersion.LGF_V10,
        description="API version",
    )
    auth_method: OracleWMSAuthMethod = Field(
        default=OracleWMSAuthMethod.BASIC,
        description="Authentication method",
    )

    # Connection settings - extend base timeout with Oracle WMS specific values
    oracle_wms_timeout: int = Field(
        default=30,
        description="Oracle WMS request timeout in seconds",
    )
    oracle_wms_max_retries: int = Field(
        default=3,
        description="Oracle WMS maximum retry attempts",
    )
    oracle_wms_verify_ssl: bool = Field(
        default=True,
        description="Oracle WMS SSL certificate verification",
    )

    # Feature flags - extend base logging with Oracle WMS specific flags
    oracle_wms_enable_logging: bool = Field(
        default=True,
        description="Enable Oracle WMS specific logging",
    )
    oracle_wms_use_mock: bool = Field(
        default=False,
        description="Use internal mock server explicitly (testing only)",
    )

    @field_validator("oracle_wms_base_url")
    @classmethod
    def validate_oracle_wms_base_url(cls, v: str) -> str:
        """Validate Oracle WMS base URL using centralized FlextModels validation."""
        # Use centralized FlextModels validation instead of duplicate logic
        validation_result = FlextModels.create_validated_http_url(
            v.strip() if v else "",
        )
        if validation_result.is_failure:
            error_msg = f"Invalid Oracle WMS base URL: {validation_result.error}"
            raise ValueError(error_msg)
        return str(validation_result.unwrap())

    @field_validator("oracle_wms_timeout")
    @classmethod
    def validate_oracle_wms_timeout(cls, v: int) -> int:
        """Validate Oracle WMS timeout value."""
        if v <= 0:
            msg = "Oracle WMS timeout must be greater than 0"
            raise ValueError(msg)
        return v

    @field_validator("oracle_wms_max_retries")
    @classmethod
    def validate_oracle_wms_max_retries(cls, v: int) -> int:
        """Validate Oracle WMS max retries value."""
        if v < 0:
            msg = "Oracle WMS max retries cannot be negative"
            raise ValueError(msg)
        return v

    def validate_business_rules(self: object) -> FlextResult[None]:
        """Validate Oracle WMS specific business rules."""
        validation_errors: list[str] = []

        # Validate authentication based on method
        if self.auth_method == OracleWMSAuthMethod.BASIC:
            if not self.oracle_wms_username or not self.oracle_wms_password:
                validation_errors.append(
                    "Oracle WMS username and password required for basic auth",
                )
        elif self.auth_method == OracleWMSAuthMethod.BEARER:
            # Add bearer token validation if needed
            pass
        elif self.auth_method == OracleWMSAuthMethod.API_KEY:
            # Add API key validation if needed
            pass

        # Validate mock usage
        if self.oracle_wms_use_mock and not self.oracle_wms_base_url:
            validation_errors.append(
                "Oracle WMS base URL is required even when using real",
            )

        if validation_errors:
            return FlextResult[None].fail("; ".join(validation_errors))
        return FlextResult[None].ok(None)

    class _AuthHelper:
        """Nested helper for authentication operations."""

        @staticmethod
        def get_auth_headers(
            config: FlextOracleWmsConfig,
        ) -> FlextTypes.Core.Headers:
            """Get authentication headers based on configuration."""
            headers: dict[str, str] = {}

            if config.auth_method == OracleWMSAuthMethod.BASIC:
                credentials = (
                    f"{config.oracle_wms_username}:{config.oracle_wms_password}"
                )
                encoded_credentials = base64.b64encode(credentials.encode()).decode()
                headers["Authorization"] = f"Basic {encoded_credentials}"

            return headers

    class _ConnectionHelper:
        """Nested helper for connection operations."""

        @staticmethod
        def build_endpoint_url(config: FlextOracleWmsConfig, path: str) -> str:
            """Build full endpoint URL."""
            base = config.oracle_wms_base_url.rstrip("/")
            path = path.lstrip("/")
            return f"{base}/{path}"

    # Convenience methods using nested helpers
    def get_auth_headers(self: object) -> FlextTypes.Core.Headers:
        """Get authentication headers."""
        return self._AuthHelper.get_auth_headers(self)

    def build_endpoint_url(self, path: str) -> str:
        """Build full endpoint URL."""
        return self._ConnectionHelper.build_endpoint_url(self, path)

    def extract_environment_from_url(self: object) -> str:
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
    def for_testing(cls: object) -> FlextOracleWmsConfig:
        """Create configuration optimized for testing."""
        # Use environment variable for test password to avoid hardcoded values
        test_password = os.getenv("TEST_WMS_PASSWORD", "test_password")
        return cls(
            oracle_wms_base_url="https://test.example.com",
            oracle_wms_username="test_user",
            oracle_wms_password=test_password,
            api_version=FlextOracleWmsApiVersion.LGF_V10,
            auth_method=OracleWMSAuthMethod.BASIC,
            oracle_wms_timeout=5,
            oracle_wms_max_retries=1,
            oracle_wms_verify_ssl=False,
            oracle_wms_enable_logging=False,
            oracle_wms_use_mock=True,
        )

    @classmethod
    def create_production_config(
        cls,
        *,
        oracle_wms_base_url: str,
        oracle_wms_username: str,
        oracle_wms_password: str,
        oracle_wms_timeout: int = 60,
        oracle_wms_max_retries: int = 5,
        oracle_wms_verify_ssl: bool = True,
        oracle_wms_enable_logging: bool = True,
        oracle_wms_use_mock: bool = False,
    ) -> FlextResult[FlextConfig]:
        """Create production Oracle WMS configuration.

        Args:
            oracle_wms_base_url: Production Oracle WMS base URL
            oracle_wms_username: Production username
            oracle_wms_password: Production password
            oracle_wms_timeout: Request timeout in seconds
            oracle_wms_max_retries: Maximum retry attempts
            oracle_wms_verify_ssl: Enable SSL verification
            oracle_wms_enable_logging: Enable logging
            oracle_wms_use_mock: Use mock server

        Returns:
            FlextResult containing the configuration or error

        """
        try:
            config: dict[str, object] = cls(
                oracle_wms_base_url=oracle_wms_base_url,
                oracle_wms_username=oracle_wms_username,
                oracle_wms_password=oracle_wms_password,
                environment="production",
                oracle_wms_timeout=oracle_wms_timeout,
                oracle_wms_max_retries=oracle_wms_max_retries,
                oracle_wms_verify_ssl=oracle_wms_verify_ssl,
                oracle_wms_enable_logging=oracle_wms_enable_logging,
                oracle_wms_use_mock=oracle_wms_use_mock,
            )
            validation_result: FlextResult[object] = config.validate_business_rules()
            if validation_result.is_failure:
                error_msg = validation_result.error or "Validation failed"
                return FlextResult[FlextConfig].fail(error_msg)
            return FlextResult[FlextConfig].ok(config)
        except Exception as e:
            return FlextResult[FlextConfig].fail(
                f"Failed to create production config: {e}",
            )

    @classmethod
    def get_oracle_wms_global_instance(cls, **kwargs: object) -> FlextOracleWmsConfig:
        """Get the SINGLETON GLOBAL Oracle WMS configuration instance.

        This method ensures a single source of truth for Oracle WMS configuration
        across the entire application, extending the flext-core singleton pattern.

        Parameters passed via kwargs can override default values and change behavior.
        The singleton pattern ensures only one instance exists, but allows dynamic
        configuration updates.

        Args:
            **kwargs: Configuration parameters to override defaults

        Returns:
            FlextOracleWmsConfig: The global Oracle WMS configuration instance

        """
        # Check if we already have a global instance
        if cls._oracle_wms_global_instance is not None:
            # Update existing instance with new parameters if provided
            if kwargs:
                for key, value in kwargs.items():
                    if hasattr(cls._oracle_wms_global_instance, key):
                        setattr(cls._oracle_wms_global_instance, key, value)
            return cls._oracle_wms_global_instance

        # Create new instance with default values
        config: dict[str, object] = cls()

        # Apply any provided kwargs
        if kwargs:
            for key, value in kwargs.items():
                if hasattr(config, key):
                    setattr(config, key, value)

        # Set as global instance
        cls._oracle_wms_global_instance = config
        return config

    @classmethod
    def create_from_environment(
        cls,
        *,
        env_file: str | Path | None = None,
        extra_settings: FlextTypes.Core.Dict | None = None,
    ) -> FlextResult[FlextConfig]:
        """Create Oracle WMS configuration from environment variables.

        Uses the singleton pattern from flext-core and extends it with Oracle WMS specific fields.
        Environment variables can be overridden by parameters passed via override_kwargs.

        Environment Variables:
            ORACLE_WMS_BASE_URL: Oracle WMS base URL
            ORACLE_WMS_USERNAME: Oracle WMS username
            ORACLE_WMS_PASSWORD: Oracle WMS password
            ORACLE_WMS_API_VERSION: API version (default: LGF_V10)
            ORACLE_WMS_AUTH_METHOD: Authentication method (default: BASIC)
            ORACLE_WMS_TIMEOUT: Request timeout in seconds (default: 30)
            ORACLE_WMS_MAX_RETRIES: Maximum retry attempts (default: 3)
            ORACLE_WMS_VERIFY_SSL: SSL certificate verification (default: true)
            ORACLE_WMS_ENABLE_LOGGING: Enable logging (default: true)
            ORACLE_WMS_USE_MOCK: Use mock server (default: false)

        Args:
            env_file: Environment file path (currently unused but required for compatibility)
            extra_settings: Configuration parameters to override environment variables

        Returns:
            FlextResult containing the configuration or error

        """
        try:
            # Note: env_file parameter is required for compatibility with parent class
            # but not currently used in this implementation
            _ = env_file  # Suppress unused parameter warning

            # Build configuration from environment variables with overrides
            override_kwargs = extra_settings or {}
            env_config = {
                "oracle_wms_base_url": override_kwargs.get(
                    "oracle_wms_base_url",
                    os.getenv(
                        "ORACLE_WMS_BASE_URL",
                        "https://ta29.wms.ocs.oraclecloud.com/raizen_test",
                    ),
                ),
                "oracle_wms_username": override_kwargs.get(
                    "oracle_wms_username",
                    os.getenv("ORACLE_WMS_USERNAME", "USER_WMS_INTEGRA"),
                ),
                "oracle_wms_password": override_kwargs.get(
                    "oracle_wms_password",
                    os.getenv("ORACLE_WMS_PASSWORD", "jmCyS7BK94YvhS@"),
                ),
                "api_version": override_kwargs.get(
                    "api_version",
                    FlextOracleWmsApiVersion(
                        os.getenv("ORACLE_WMS_API_VERSION", "LGF_V10"),
                    ),
                ),
                "auth_method": override_kwargs.get(
                    "auth_method",
                    OracleWMSAuthMethod(os.getenv("ORACLE_WMS_AUTH_METHOD", "BASIC")),
                ),
                "oracle_wms_timeout": override_kwargs.get(
                    "oracle_wms_timeout",
                    int(os.getenv("ORACLE_WMS_TIMEOUT", "30")),
                ),
                "oracle_wms_max_retries": override_kwargs.get(
                    "oracle_wms_max_retries",
                    int(os.getenv("ORACLE_WMS_MAX_RETRIES", "3")),
                ),
                "oracle_wms_verify_ssl": override_kwargs.get(
                    "oracle_wms_verify_ssl",
                    os.getenv("ORACLE_WMS_VERIFY_SSL", "true").lower() == "true",
                ),
                "oracle_wms_enable_logging": override_kwargs.get(
                    "oracle_wms_enable_logging",
                    os.getenv("ORACLE_WMS_ENABLE_LOGGING", "true").lower() == "true",
                ),
                "oracle_wms_use_mock": override_kwargs.get(
                    "oracle_wms_use_mock",
                    os.getenv("ORACLE_WMS_USE_MOCK", "false").lower() == "true",
                ),
            }

            # Add any additional override_kwargs that don't conflict
            for key, value in override_kwargs.items():
                if key not in env_config:
                    env_config[key] = value

            # Get the global singleton instance with environment configuration
            config: dict[str, object] = cls.get_oracle_wms_global_instance(**env_config)

            validation_result: FlextResult[object] = config.validate_business_rules()
            if validation_result.is_failure:
                error_msg = validation_result.error or "Validation failed"
                return FlextResult[FlextConfig].fail(error_msg)
            return FlextResult[FlextConfig].ok(config)
        except Exception as e:
            return FlextResult[FlextConfig].fail(
                f"Failed to create config from environment: {e}",
            )

    @classmethod
    def reset_global_instance(cls: object) -> None:
        """Reset the global singleton instance.

        This allows for dynamic reconfiguration by clearing the current
        singleton instance. The next call to get_oracle_wms_global_instance()
        will create a new instance with the provided parameters.
        """
        if hasattr(cls, "_oracle_wms_global_instance"):
            cls._oracle_wms_global_instance = None

    @classmethod
    def update_global_instance(cls, **kwargs: object) -> FlextResult[FlextConfig]:
        """Update the global singleton instance with new parameters.

        This method allows dynamic reconfiguration of the global instance
        without creating a new instance. Parameters are validated before
        being applied.

        Args:
            **kwargs: Configuration parameters to update

        Returns:
            FlextResult containing the updated configuration or error

        """
        try:
            # Get current global instance or create new one
            config: dict[str, object] = cls.get_oracle_wms_global_instance()

            # Update with new parameters
            for key, value in kwargs.items():
                if hasattr(config, key):
                    setattr(config, key, value)

            # Validate updated configuration
            validation_result: FlextResult[object] = config.validate_business_rules()
            if validation_result.is_failure:
                error_msg = validation_result.error or "Validation failed"
                return FlextResult[FlextConfig].fail(error_msg)

            return FlextResult[FlextConfig].ok(config)
        except Exception as e:
            return FlextResult[FlextConfig].fail(
                f"Failed to update global instance: {e}",
            )


# Aliases for backward compatibility - used across the codebase
FlextOracleWmsClientConfig = FlextOracleWmsConfig
FlextOracleWmsModuleConfig = FlextOracleWmsConfig
