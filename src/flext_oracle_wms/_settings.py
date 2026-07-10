"""Oracle WMS runtime settings."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, Field
from pydantic_settings import SettingsConfigDict

from flext_core import FlextSettings


class FlextOracleWmsSettings(FlextSettings):
    """Runtime settings for Oracle WMS client.

    Project-scoped scalars live under the nested ``OracleWms`` namespace group;
    universal fields (``debug``, ``trace``, ``log_level``, ``timezone``,
    ``async_logging``) are inherited from ``FlextSettings`` via MRO and are not
    redeclared here.
    """

    model_config = SettingsConfigDict(
        env_prefix="FLEXT_ORACLE_WMS_",
        env_nested_delimiter="__",
        extra="ignore",
    )

    class _OracleWms(BaseModel):
        """Oracle WMS connection and runtime scalar settings."""

        base_url: str = "http://localhost:8080"
        timeout: float = 30.0
        username: str = ""
        password: str = ""
        retry_attempts: int = 3
        api_version: str = "LGF_V10"
        auth_method: str = "basic"
        verify_ssl: bool = True
        enable_logging: bool = False
        connection_pool_size: int = 10
        cache_duration: int = 300

    if TYPE_CHECKING:
        OracleWms: _OracleWms
    else:
        OracleWms: _OracleWms = Field(default_factory=_OracleWms)


settings: FlextOracleWmsSettings = FlextOracleWmsSettings.fetch_global()
"""Pre-instantiated project settings singleton — ``from flext_oracle_wms import settings``."""

__all__ = ["FlextOracleWmsSettings", "settings"]
