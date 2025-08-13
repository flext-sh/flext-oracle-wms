"""Compatibility models module mapping to wms_models.

Re-exports domain models for tests that import flext_oracle_wms.models directly.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from flext_core import FlextResult

# Re-export but also provide a thin dataclass-compatible shim for tests that
# construct with minimal args using Pydantic-based FlextValueObject.
from flext_oracle_wms.wms_models import *  # noqa: F403
from flext_oracle_wms.wms_models import (
    FlextOracleWmsDiscoveryResult as _BaseDiscoveryResult,
)


@dataclass(frozen=True)
class FlextOracleWmsEntity:  # type: ignore[no-redef]
    name: str
    endpoint: str
    description: str | None = None
    fields: dict[str, object] = field(default_factory=dict)
    primary_key: str | None = None
    replication_key: str | None = None
    supports_incremental: bool = False

    def validate_business_rules(self) -> FlextResult[None]:
        from flext_oracle_wms.wms_constants import (
            FlextOracleWmsDefaults,
            FlextOracleWmsErrorMessages,
        )
        from flext_oracle_wms.wms_exceptions import FlextOracleWmsDataValidationError
        from flext_oracle_wms.wms_operations import validate_string_parameter

        errors: list[str] = []
        try:
            validate_string_parameter(self.name, "entity name")
            validate_string_parameter(self.endpoint, "entity endpoint")
        except Exception as e:  # pragma: no cover - message composed below
            errors.append(str(e))

        if not self.endpoint.startswith("/"):
            errors.append("Entity endpoint must start with /")
        if len(self.name) > FlextOracleWmsDefaults.MAX_ENTITY_NAME_LENGTH:
            errors.append(
                f"Entity name too long (max {FlextOracleWmsDefaults.MAX_ENTITY_NAME_LENGTH} characters)",
            )
        if errors:
            # Mirror legacy behavior: raise data validation error
            msg = f"{FlextOracleWmsErrorMessages.ENTITY_VALIDATION_FAILED}: {'; '.join(errors)}"
            raise FlextOracleWmsDataValidationError(
                msg,
            )
        return FlextResult.ok(None)


@dataclass(frozen=True)
class FlextOracleWmsDiscoveryResult(_BaseDiscoveryResult):  # type: ignore[misc, no-redef]
    # Provide defaults so tests can omit some fields when constructing
    entities: list[FlextOracleWmsEntity] = field(default_factory=list)
    total_count: int = 0
    timestamp: str = ""
    discovery_duration_ms: float = 0.0
    has_errors: bool = False
    errors: list[str] = field(default_factory=list)
    api_version: str | None = "v10"
