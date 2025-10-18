"""FLEXT Oracle WMS Configuration - Advanced composition patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextConfig, FlextResult
from pydantic import Field

from flext_oracle_wms.constants import FlextOracleWmsConstants


class FlextOracleWmsConfig(FlextConfig):
    """Enterprise Oracle WMS configuration with advanced composition.

    Uses Python 3.13+ syntax, reduces declarations through advanced patterns.
    One class per module following SOLID principles.
    """

    # Connection & Auth (composed fields)
    base_url: str = Field(
        default=str(FlextOracleWmsConstants.API_CONFIG["base_url_default"])
    )
    username: str | None = Field(default=None)
    password: str | None = Field(default=None)

    # Operational settings (composed)
    timeout: int = Field(
        default=int(FlextOracleWmsConstants.API_CONFIG["timeout_default"])
    )
    retry_attempts: int = Field(
        default=int(FlextOracleWmsConstants.API_CONFIG["max_retries"])
    )
    enable_ssl_verification: bool = Field(default=True)

    # Enterprise features (flags)
    enable_metrics: bool = Field(default=False)
    enable_tracing: bool = Field(default=False)
    enable_audit_logging: bool = Field(default=False)

    # Version & environment (composed)
    api_version: str = Field(
        default=str(FlextOracleWmsConstants.API_CONFIG["version_default"])
    )
    environment: str = Field(default=FlextOracleWmsConstants.ENVIRONMENTS["production"])
    use_mock: bool = Field(default=False)

    def environment_from_url(self) -> str:
        """Extract environment using advanced pattern matching."""
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
        return cls(use_mock=True, base_url="https://test-wms.oraclecloud.com")

    def validate_config(self) -> FlextResult[None]:
        """Validate configuration using railway pattern."""
        errors = []
        if self.timeout <= 0:
            errors.append("Timeout must be positive")
        if self.retry_attempts < 0:
            errors.append("Retry attempts cannot be negative")
        if self.base_url and not self.base_url.startswith(("http://", "https://")):
            errors.append("Base URL must be HTTP/HTTPS")
        return (
            FlextResult[None].fail("; ".join(errors))
            if errors
            else FlextResult[None].ok(None)
        )


__all__ = ["FlextOracleWmsConfig"]
