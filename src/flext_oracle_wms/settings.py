"""FLEXT WMS Configuration - Generic WMS integration with composition.

Uses Python 3.13+ syntax, reduces declarations through patterns.
One class per module following SOLID principles. Generic WMS configuration.
Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextResult, FlextSettings
from pydantic import Field
from pydantic_settings import SettingsConfigDict

from flext_oracle_wms.constants import FlextOracleWmsConstants


@FlextSettings.auto_register("oracle_wms")
class FlextOracleWmsSettings(FlextSettings.AutoConfig):
    """Generic WMS configuration with composition patterns.

    **ARCHITECTURAL PATTERN**: Zero-Boilerplate Auto-Registration
    This class uses FlextSettings.AutoConfig for automatic:
    - Singleton pattern (thread-safe)
    - Namespace registration (accessible via config.oracle_wms)
    - Environment variable loading from FLEXT_ORACLE_WMS_* variables
    - .env file loading (production/development)
    - Automatic type conversion and validation via Pydantic v2
    Uses Python 3.13+ syntax, reduces declarations through patterns.
    One class per module following SOLID principles. Generic for any WMS system.
    """

    # Use FlextSettings.resolve_env_file() to ensure all FLEXT configs use same .env
    model_config = SettingsConfigDict(
        env_prefix="FLEXT_ORACLE_WMS_",
        env_file=FlextSettings.resolve_env_file(),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        validate_assignment=True,
        str_strip_whitespace=True,
        validate_default=True,
        frozen=False,
        arbitrary_types_allowed=True,
        strict=False,
    )
    # Connection & Auth (composed fields using advanced patterns)
    base_url: str = Field(
        default=str(FlextOracleWmsConstants.API_CONFIG["base_url_default"]),
    )
    username: str | None = Field(default=None)
    password: str | None = Field(default=None)
    api_key: str | None = Field(default=None)
    # Operational settings (composed with validation)
    timeout: int = Field(
        default=int(FlextOracleWmsConstants.API_CONFIG["timeout_default"]),
        ge=1,
        le=300,
    )
    retry_attempts: int = Field(
        default=int(FlextOracleWmsConstants.API_CONFIG["max_retries"]),
        ge=0,
        le=10,
    )
    enable_ssl_verification: bool = Field(default=True)
    # Enterprise features (flags with composition)
    enable_metrics: bool = Field(default=False)
    enable_tracing: bool = Field(default=False)
    enable_audit_logging: bool = Field(default=False)
    # Version & environment (composed with defaults)
    api_version: str = Field(
        default=str(FlextOracleWmsConstants.API_CONFIG["version_default"]),
    )
    environment: str = Field(default=FlextOracleWmsConstants.ENVIRONMENTS["production"])
    use_mock: bool = Field(default=False)

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
            (env for key, env in env_map.items() if key in self.base_url),
            "unknown",
        )

    @classmethod
    def testing_config(cls) -> FlextOracleWmsSettings:
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


__all__ = ["FlextOracleWmsSettings"]
