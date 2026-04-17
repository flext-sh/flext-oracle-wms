"""Oracle WMS runtime settings."""

from __future__ import annotations

from typing import Annotated, ClassVar, Self

from pydantic_settings import SettingsConfigDict

from flext_core import FlextSettings
from flext_oracle_wms import m, p, r, u


@FlextSettings.auto_register("oracle-wms")
class FlextOracleWmsSettings(FlextSettings):
    """Runtime settings for Oracle WMS client."""

    model_config: ClassVar[SettingsConfigDict] = m.SettingsConfigDict(
        env_prefix="FLEXT_ORACLE_WMS_",
        extra="ignore",
    )

    base_url: Annotated[str, u.Field(min_length=1)] = "http://localhost:8080"
    timeout: Annotated[float, u.Field(ge=1.0, le=300.0)] = 30.0
    username: str = ""
    password: str = ""
    retry_attempts: Annotated[int, u.Field(ge=0)] = 3

    def validate_config(self) -> p.Result[bool]:
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
            "username": "test_user",
            "password": "test_password",
        })
