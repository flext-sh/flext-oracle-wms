"""Client-specific Oracle WMS settings."""

from __future__ import annotations

from typing import Annotated, ClassVar

from flext_core import m, u

from flext_oracle_wms import FlextOracleWmsSettings


class FlextOracleWmsClientSettings(FlextOracleWmsSettings):
    """Settings contract consumed by FlextOracleWmsClient."""

    model_config: ClassVar[m.SettingsConfigDict] = m.SettingsConfigDict(
        env_prefix="FLEXT_ORACLE_WMS_",
        extra="ignore",
    )

    base_url: str = ""
    username: str = ""
    password: str = ""
    api_version: str = "LGF_V10"
    auth_method: str = "basic"
    timeout: Annotated[float, u.Field(ge=1.0)] = 30.0
    max_retries: Annotated[int, u.Field(ge=0)] = 3
    verify_ssl: bool = True
    enable_logging: bool = False
    connection_pool_size: Annotated[int, u.Field(ge=1)] = 10
    cache_duration: Annotated[int, u.Field(ge=0)] = 300
    project_name: str = "flext-oracle-wms"
    project_version: str = "1.0.0"
