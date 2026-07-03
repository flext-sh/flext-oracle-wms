"""Oracle WMS runtime settings."""

from __future__ import annotations

from typing import Annotated, ClassVar, Self

from flext_core import FlextSettingsBase, r
from flext_oracle_wms.models import m
from flext_oracle_wms.protocols import p
from flext_oracle_wms.utilities import u


class FlextOracleWmsSettings(FlextSettingsBase):
    """Runtime settings for Oracle WMS client."""

    model_config: ClassVar[m.SettingsConfigDict] = m.SettingsConfigDict(
        env_prefix="FLEXT_ORACLE_WMS_",
        extra="ignore",
    )

    base_url: Annotated[
        str, u.Field(min_length=1, description="Oracle WMS base URL")
    ] = "http://localhost:8080"
    timeout: Annotated[
        float,
        u.Field(ge=1.0, le=300.0, description="Request timeout seconds"),
    ] = 30.0
    username: Annotated[str, u.Field(description="WMS username")] = ""
    password: Annotated[str, u.Field(description="WMS password")] = ""
    retry_attempts: Annotated[int, u.Field(ge=0, description="Retry attempts")] = 3
    api_version: Annotated[str, u.Field(description="WMS API version")] = "LGF_V10"
    auth_method: Annotated[str, u.Field(description="Authentication method")] = "basic"
    verify_ssl: Annotated[
        bool,
        u.Field(description="Verify SSL certificates"),
    ] = True
    enable_logging: Annotated[
        bool,
        u.Field(description="Enable request logging"),
    ] = False
    connection_pool_size: Annotated[
        int,
        u.Field(ge=1, description="HTTP connection pool size"),
    ] = 10
    cache_duration: Annotated[
        int,
        u.Field(ge=0, description="Cache duration in seconds"),
    ] = 300

    def validate_config(self) -> p.Result[bool]:
        """Validate configuration business rules."""
        if not self.base_url:
            return r[bool].fail("base_url is required")
        return r[bool].ok(True)

    @classmethod
    def testing_config(cls) -> Self:
        """Build deterministic settings for tests."""
        settings = cls.model_validate({
            "base_url": "https://test-wms.example.com",
            "timeout": 30.0,
            "username": "test_user",
            "password": "test_password",
        })
        # Keep test fixture generation isolated from the FlextSettings singleton.
        cls.reset_instance()
        return settings
