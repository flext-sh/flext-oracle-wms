"""Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT.
"""

from __future__ import annotations

from flext_core import FlextTypes

"""Oracle WMS Configuration - Consolidated Configuration Management.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Enterprise configuration management for Oracle WMS integrations.
This module provides unified configuration management for all Oracle WMS operations,
eliminating duplication between tap and target implementations.
Implements flext-core unified configuration standards.
"""


import os
from pathlib import Path
from typing import ClassVar, NewType
from urllib.parse import urlparse

from flext_core import (
    FlextConfig,
    FlextLogger,
    FlextResult,
)
from pydantic import Field, HttpUrl, field_validator
from pydantic_settings import SettingsConfigDict

from flext_oracle_wms.wms_constants import FlextOracleWmsApiVersion

# Type aliases for better type safety
WMSAPIVersion = NewType("WMSAPIVersion", str)
WMSRetryAttempts = NewType("WMSRetryAttempts", int)


class FlextOracleWmsClientConfig(FlextConfig):
    """Oracle WMS Declarative Client Configuration.

    Simplified configuration management for declarative Oracle WMS Cloud client
    operations with comprehensive validation and type safety using FLEXT patterns.

    Features:
      - Type-safe configuration with domain validation
      - Environment-driven settings with sensible defaults
      - SSL verification and security controls
      - Timeout and retry configuration for reliability
      - Integration with FLEXT logging and observability

    Example:
      Basic configuration setup:

      >>> config = FlextOracleWmsClientConfig(
      ...     base_url="https://your-wms.oraclecloud.com",
      ...     username="api_user",
      ...     password="secure_password",
      ...     environment="production",
      ... )
      >>> validation = config.validate_business_rules()
      >>> if validation.success:
      ...     from flext_core import FlextLogger
      ...
      ...     FlextLogger(__name__).info("Configuration is valid")

    """

    base_url: str = Field(..., description="Oracle WMS base URL")
    username: str = Field(..., description="Oracle WMS username")
    password: str = Field(..., description="Oracle WMS password")
    environment: FlextTypes.Config.Environment = Field(
        default="development", description="Environment name"
    )
    api_version: FlextOracleWmsApiVersion = Field(
        default=FlextOracleWmsApiVersion.LGF_V10,
        description="API version",
    )
    timeout: int = Field(default=30, description="Request timeout in seconds")
    max_retries: int = Field(default=3, description="Maximum retry attempts")
    verify_ssl: bool = Field(default=True, description="Verify SSL certificates")
    enable_logging: bool = Field(default=True, description="Enable logging")
    use_mock: bool = Field(
        default=False,
        description="Use internal mock server explicitly (testing only)",
    )

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate Oracle WMS client configuration business rules."""
        validation_errors = []

        if not self.base_url:
            validation_errors.append("Base URL cannot be empty")
        elif not self.base_url.startswith(("http://", "https://")):
            validation_errors.append("Base URL must start with http:// or https://")

        if not self.username:
            validation_errors.append("Username cannot be empty")
        if not self.password:
            validation_errors.append("Password cannot be empty")
        if self.timeout <= 0:
            validation_errors.append("Timeout must be greater than 0")
        if self.max_retries < 0:
            validation_errors.append("Max retries cannot be negative")
        # Explicit mock must be intentional; no auto-mock by URL heuristics
        if self.use_mock and not self.base_url:
            validation_errors.append("Base URL is required even when using mock")

        if validation_errors:
            return FlextResult[None].fail("; ".join(validation_errors))
        return FlextResult[None].ok(None)

    @classmethod
    def from_legacy_config(
        cls,
        legacy_config: FlextOracleWmsModuleConfig,
    ) -> FlextOracleWmsClientConfig:
        """Create declarative config from legacy config."""
        # Extract environment from base_url, ensuring it's a valid literal
        environment: FlextTypes.Config.Environment = "development"
        base_url_str = str(legacy_config.base_url)
        try:
            parsed = urlparse(base_url_str)
            path_parts = parsed.path.strip("/").split("/")
            if path_parts and path_parts[-1]:
                parsed_env = path_parts[-1].lower()
                # Map to valid environments
                if parsed_env in {"prod", "production"}:
                    environment = "production"
                elif parsed_env in {"stage", "staging"}:
                    environment = "staging"
                elif parsed_env in {"test", "testing"}:
                    environment = "test"
                elif parsed_env == "local":
                    environment = "local"
                else:
                    environment = "development"
        except (ValueError, TypeError, AttributeError, IndexError):
            environment = "development"

        return cls(
            base_url=base_url_str,
            username=legacy_config.username,
            password=legacy_config.password,
            environment=environment,
            api_version=FlextOracleWmsApiVersion.LGF_V10
            if legacy_config.api_version == "v10"
            else FlextOracleWmsApiVersion.LEGACY,
            timeout=int(legacy_config.timeout_seconds),
            max_retries=legacy_config.retries,
            verify_ssl=legacy_config.verify_ssl,
            enable_logging=legacy_config.enable_request_logging,
        )


class FlextOracleWmsModuleConfig(FlextConfig):
    """Enterprise Oracle WMS configuration using modern Pydantic patterns.

    Simplified configuration management for Oracle WMS integration operations
    with proper type safety and validation, following SOLID principles.
    """

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_prefix="ORACLE_WMS_",
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        case_sensitive=False,
        extra="ignore",  # Allow extra fields in .env
        validate_assignment=True,
        str_strip_whitespace=True,
    )
    # === Oracle WMS API Configuration (additional to WMSConfigMixin) ===
    base_url: HttpUrl = Field(
        default_factory=lambda: HttpUrl("https://example.oraclecloud.com"),
        description="Oracle WMS base URL (e.g., https://ta29.wms.ocs.oraclecloud.com/raizen_test)",
    )
    api_version: str = Field(
        default="v10",
        description="Oracle WMS API version",
    )
    username: str = Field(default="", description="Oracle WMS API username")
    password: str = Field(default="", description="Oracle WMS API password")
    # === WMS Rate Limiting (additional to PerformanceConfigMixin) ===
    enable_rate_limiting: bool = Field(
        default=True,
        description="Enable WMS API rate limiting",
    )
    max_requests_per_minute: int = Field(
        default=60,
        description="Max WMS requests per minute",
    )
    min_request_delay: float = Field(
        default=0.1,
        description="Minimum delay between WMS requests",
    )
    # === Security Configuration ===
    verify_ssl: bool = Field(default=True, description="Verify SSL certificates")
    ssl_cert_path: Path | None = Field(
        default=None,
        description="Path to SSL certificate file",
    )
    # === Observability (additional to LoggingConfigMixin) ===
    enable_request_logging: bool = Field(
        default=False,
        description="Log detailed API request/response information",
    )
    enable_metrics: bool = Field(default=True, description="Enable metrics collection")
    # === Discovery Configuration ===
    auto_discover: bool = Field(
        default=True,
        description="Enable automatic schema discovery",
    )
    include_metadata: bool = Field(
        default=True,
        description="Include metadata in responses",
    )
    # === Connection Pool Configuration (additional to PerformanceConfigMixin) ===
    pool_size: int = Field(
        default=5,
        description="HTTP connection pool size",
    )
    pool_timeout: float = Field(
        default=30.0,
        description="Connection pool timeout",
    )
    # Note: version is inherited from FlextConfig

    # === Enterprise Cache Configuration ===
    enable_cache: bool = Field(default=True, description="Enable enterprise caching")
    cache_ttl_seconds: int = Field(default=300, description="Cache TTL in seconds")
    max_cache_size: int = Field(default=1000, description="Maximum cache entries")
    cleanup_interval_seconds: int = Field(
        default=300,
        description="Cache cleanup interval",
    )

    # === Performance Configuration ===
    # Note: timeout_seconds is inherited from FlextConfig
    batch_size: int = Field(
        default=100,
        description="Batch size for API requests",
    )
    # Note: max_retries is inherited from FlextConfig (as retries)
    retry_delay: float = Field(
        default=1.0,
        description="Delay between retry attempts in seconds",
    )

    # === Project Configuration ===
    project_name: str = Field(
        default="flext-oracle-wms",
        description="Project name for identification",
    )
    # Note: environment is inherited from FlextConfig

    # === Compatibility Properties ===
    @property
    def max_retries(self) -> int:
        """Compatibility property for max_retries access."""
        return self.retries

    @field_validator("base_url")
    @classmethod
    def validate_base_url(cls, v: HttpUrl) -> HttpUrl:
        """Validate Oracle WMS base URL format."""
        url_str = str(v)
        if not url_str.startswith(("http://", "https://")):
            invalid_protocol_msg: str = f"Invalid Oracle WMS base URL: {url_str} (must start with http:// or https://)"
            raise ValueError(invalid_protocol_msg)
        # Validate Oracle WMS URL pattern - more flexible for different environments
        oracle_patterns = [
            ".wms.ocs.oraclecloud.com",  # Production Oracle Cloud
            ".oraclecloud.com",  # Other Oracle Cloud services
            "oracle.com",  # Oracle domains
        ]

        dev_patterns = [
            "localhost",
            "127.0.0.1",
            "test",
            "dev",
            "staging",
            "demo",
            "sandbox",
            "internal",
            "lab",
            "qa",
        ]

        # Check if URL matches Oracle patterns or dev patterns
        is_oracle_url = any(pattern in url_str for pattern in oracle_patterns)
        is_dev_url = any(pattern in url_str for pattern in dev_patterns)

        if not (is_oracle_url or is_dev_url):
            # Allow any HTTPS URL for maximum flexibility
            if not url_str.startswith("https://"):
                https_security_msg: str = (
                    f"Oracle WMS URL should use HTTPS for security: {url_str}"
                )
                raise ValueError(https_security_msg)
            # For non-Oracle URLs, just issue a warning in logs but allow it

            logger = FlextLogger(__name__)
            logger.warning(
                "Using non-standard Oracle WMS URL: %s. "
                "Ensure this is correct for your environment.",
                url_str,
            )
        return v

    # Note: log_level validation is now handled by LoggingConfigMixin
    @property
    def api_headers(self) -> FlextTypes.Core.Headers:
        """Generate standard API headers for Oracle WMS requests."""
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": f"flext-oracle-wms/{self.version}",
        }

    @property
    def connection_config(self) -> FlextTypes.Core.Dict:
        """Generate connection configuration for HTTP client."""
        return {
            "base_url": str(self.base_url),
            "timeout": self.timeout_seconds,  # Using composition mixin field
            "verify": self.verify_ssl,
            "headers": self.api_headers,
        }

    @property
    def wms_endpoint_base(self) -> str:
        """Get the WMS API endpoint base path."""
        return f"/wms/lgfapi/{self.api_version}/entity/"

    def get_entity_endpoint(self, entity_name: str) -> str:
        """Get the full endpoint URL for a specific entity."""
        return f"{self.wms_endpoint_base}{entity_name}"

    def get_entity_params(self, **additional_params: object) -> FlextTypes.Core.Dict:
        """Generate standard entity query parameters."""
        params: FlextTypes.Core.Dict = {
            "page_size": self.batch_size,  # Using composition mixin field
        }

        for key, value in additional_params.items():
            if isinstance(value, (str, int, float, bool)):
                params[key] = value
            else:
                params[key] = str(value)
        return params

    @classmethod
    def from_env_file(cls, env_file: str | Path = ".env") -> FlextOracleWmsModuleConfig:
        """Create configuration from environment file."""
        # Note: BaseSettings uses model_config.env_file, not constructor param
        # For dynamic env files, temporarily load into environment
        if Path(env_file).exists():
            from dotenv import load_dotenv

            load_dotenv(env_file)
        return cls()

    @classmethod
    def for_testing(cls) -> FlextOracleWmsModuleConfig:
        """Create configuration optimized for testing."""
        return cls(
            project_name="flext-oracle-wms-test",
            environment="test",
            base_url=HttpUrl("https://test.example.com"),
            username="test_user",
            password=os.environ.get("FLEXT_ORACLE_WMS_TEST_PASSWORD", "test_password"),
            batch_size=10,  # Using composition mixin field
            timeout_seconds=5,  # Using composition mixin field
            retries=1,  # Using composition mixin field
            enable_request_logging=True,
            verify_ssl=False,
        )


def load_config() -> FlextOracleWmsModuleConfig:
    """Load Oracle WMS configuration from environment.

    This function provides a convenient way to load configuration
    with automatic environment file detection.
    """
    # Try to find .env file in current directory or parent directories
    current_dir = Path.cwd()
    for _ in range(5):  # Search up to 5 levels up
        potential_env = Path(current_dir) / ".env"
        if Path(potential_env).exists():
            break
        current_dir = Path(current_dir).parent
    # FlextConfig/BaseSettings handles env files via model_config, not constructor
    return FlextOracleWmsModuleConfig()


# Rebuild the model to ensure all types are properly resolved
FlextOracleWmsModuleConfig.model_rebuild()


__all__: FlextTypes.Core.StringList = [
    "FlextOracleWmsClientConfig",
    "FlextOracleWmsModuleConfig",
    "WMSAPIVersion",
    "WMSRetryAttempts",
    "load_config",
]
