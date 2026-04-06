"""FLEXT WMS Configuration - Generic WMS integration with composition.

Uses Python 3.13+ syntax, reduces declarations through patterns.
One class per module following SOLID principles. Generic WMS configuration.
Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Annotated, ClassVar, Self

from pydantic import Field
from pydantic_settings import SettingsConfigDict

from flext_core import FlextSettings, r


@FlextSettings.auto_register("oracle-wms")
class FlextOracleWmsSettings(FlextSettings):
    """Runtime settings for Oracle WMS client."""

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(extra="ignore")

    base_url: Annotated[str, Field(min_length=1)] = "http://localhost:8080"
    timeout: Annotated[float, Field(ge=1.0, le=300.0)] = 30.0
    username: str = ""
    password: str = ""
    use_mock: bool = False
    retry_attempts: Annotated[int, Field(ge=0)] = 3

    def validate_config(self) -> r[bool]:
        """Validate configuration business rules."""
        if not self.base_url:
            return r[bool].fail("base_url is required")
        return r[bool].ok(True)

    @classmethod
    def testing_config(cls) -> Self:
        """Build deterministic settings for tests."""
        return cls.model_validate({
            "base_url": "https://test-wms.example.com",
            "timeout": 30.0,
            "use_mock": True,
        })


class FlextOracleWmsClientSettings(FlextOracleWmsSettings):
    """Settings contract consumed by FlextOracleWmsClient."""

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(extra="ignore")

    base_url: str = ""
    username: str = ""
    password: str = ""
    api_version: str = "LGF_V10"
    auth_method: str = "BASIC"
    timeout: Annotated[float, Field(ge=1.0)] = 30.0
    max_retries: Annotated[int, Field(ge=0)] = 3
    verify_ssl: bool = True
    enable_logging: bool = False
    use_mock: bool = False
    connection_pool_size: Annotated[int, Field(ge=1)] = 10
    cache_duration: Annotated[int, Field(ge=0)] = 300
    project_name: str = "flext-oracle-wms"
    project_version: str = "1.0.0"


__all__ = ["FlextOracleWmsClientSettings", "FlextOracleWmsSettings"]
