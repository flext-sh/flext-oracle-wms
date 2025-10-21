"""FLEXT WMS Configuration - Generic WMS integration with composition.

Uses Python 3.13+ syntax, reduces declarations through patterns.
One class per module following SOLID principles. Generic WMS configuration.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextConfig, FlextResult
from pydantic import Field, field_validator

from flext_oracle_wms.constants import FlextOracleWmsConstants


class FlextOracleWmsConfig(FlextConfig):
    """Generic WMS configuration with composition patterns.

    Uses Python 3.13+ syntax, reduces declarations through patterns.
    One class per module following SOLID principles. Generic for any WMS system.
    """

    # Connection & Auth (composed fields using advanced patterns)
    base_url: str = Field(
        default=str(FlextOracleWmsConstants.API_CONFIG["base_url_default"])
    )
    username: str | None = Field(default=None)
    password: str | None = Field(default=None)
    api_key: str | None = Field(default=None)

    # Operational settings (composed with validation)
    timeout: int = Field(
        default=int(FlextOracleWmsConstants.API_CONFIG["timeout_default"]), ge=1, le=300
    )
    retry_attempts: int = Field(
        default=int(FlextOracleWmsConstants.API_CONFIG["max_retries"]), ge=0, le=10
    )
    enable_ssl_verification: bool = Field(default=True)

    # Enterprise features (flags with composition)
    enable_metrics: bool = Field(default=False)
    enable_tracing: bool = Field(default=False)
    enable_audit_logging: bool = Field(default=False)

    # Version & environment (composed with defaults)
    api_version: str = Field(
        default=str(FlextOracleWmsConstants.API_CONFIG["version_default"])
    )
    environment: str = Field(default=FlextOracleWmsConstants.ENVIRONMENTS["production"])
    use_mock: bool = Field(default=False)

    @field_validator("base_url")
    @classmethod
    def validate_base_url(cls, v: str) -> str:
        """Validate base URL format."""
        if not v.startswith(("http://", "https://")):
            msg = "Base URL must be HTTP/HTTPS"
            raise ValueError(msg)
        return v

    @property
    def environment_from_url(self) -> str:
        """Extract environment using pattern matching."""
        if not self.base_url:
            return "unknown"
        # Advanced dict comprehension with next() for efficiency
        env_keys = {"dev", "staging", "prod"}
        env_map = {
            k: v
            for k, v in FlextOracleWmsConstants.ENVIRONMENTS.items()
            if k in env_keys
        }
        return next(
            (env for key, env in env_map.items() if key in self.base_url), "unknown"
        )

    @classmethod
    def testing_config(cls) -> FlextOracleWmsConfig:
        """Create testing configuration with modern patterns."""
        return cls(use_mock=True, base_url="https://test-wms.example.com")

    def validate_config(self) -> FlextResult[None]:
        """Validate configuration using railway pattern."""
        errors = []
        if self.timeout <= 0:
            errors.append("Timeout must be positive")
        if self.retry_attempts < 0:
            errors.append("Retry attempts cannot be negative")
        return (
            FlextResult[None].fail("; ".join(errors))
            if errors
            else FlextResult[None].ok(None)
        )


__all__ = ["FlextOracleWmsConfig"]
