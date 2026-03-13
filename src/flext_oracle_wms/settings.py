"""FLEXT WMS Configuration - Generic WMS integration with composition.

Uses Python 3.13+ syntax, reduces declarations through patterns.
One class per module following SOLID principles. Generic WMS configuration.
Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextSettings
from pydantic import Field
from pydantic_settings import SettingsConfigDict


class FlextOracleWmsSettings(FlextSettings):
    """Runtime settings for Oracle WMS client."""

    model_config = SettingsConfigDict(extra="ignore")

    base_url: str = Field(default="http://localhost:8080", min_length=1)
    timeout: float = Field(default=30.0, ge=1.0, le=300.0)

    @classmethod
    def testing_config(cls) -> FlextOracleWmsSettings:
        """Build deterministic settings for tests."""
        return cls(base_url="http://localhost:8080", timeout=30.0)


class FlextOracleWmsClientSettings(FlextOracleWmsSettings):
    """Settings contract consumed by FlextOracleWmsClient."""

    model_config = SettingsConfigDict(extra="ignore")

    base_url: str = Field(default="")
    username: str = Field(default="")
    password: str = Field(default="")
    api_version: str = Field(default="LGF_V10")
    auth_method: str = Field(default="BASIC")
    timeout: float = Field(default=30.0, ge=1.0)
    max_retries: int = Field(default=3, ge=0)
    verify_ssl: bool = Field(default=True)
    enable_logging: bool = Field(default=False)
    use_mock: bool = Field(default=False)
    connection_pool_size: int = Field(default=10, ge=1)
    cache_duration: int = Field(default=300, ge=0)
    project_name: str = Field(default="flext-oracle-wms")
    project_version: str = Field(default="1.0.0")


__all__ = ["FlextOracleWmsClientSettings", "FlextOracleWmsSettings"]
