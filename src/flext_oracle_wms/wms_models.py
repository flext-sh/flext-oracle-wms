"""Oracle WMS Models - Consolidated Data Models and Types.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Consolidated Oracle WMS data models, type definitions, and entity structures.
This module combines models.py + types.py + core entities from api_catalog.py
into a single unified data model system.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Annotated, Literal, TypedDict

from flext_core import FlextResult, FlextValueObject
from pydantic import Field, StringConstraints

from flext_oracle_wms.wms_constants import (
    FlextOracleWmsDefaults,
    FlextOracleWmsErrorMessages,
)

# =============================================================================
# TYPE DEFINITIONS - Core Oracle WMS Types
# =============================================================================

# Core record types - USED EVERYWHERE
TOracleWmsRecord = dict[str, object]
TOracleWmsRecordBatch = list[TOracleWmsRecord]
TOracleWmsSchema = dict[str, dict[str, object]]

# API types - USED BY CLIENT
TOracleWmsApiResponse = dict[str, object]
TOracleWmsApiVersion = Literal["v10", "v9", "v8", "legacy"]

# Entity naming - USED BY CLIENT/DISCOVERY
TOracleWmsEntityId = Annotated[str, StringConstraints(min_length=1, max_length=100)]
TOracleWmsEntityName = Annotated[
    str,
    StringConstraints(min_length=1, max_length=50, pattern=r"^[a-z0-9_]+$"),
]

# Filter types - USED BY FILTERING MODULE
TOracleWmsFilterValue = (
    str | int | float | bool | list[str | int | float] | dict[str, object]
)
TOracleWmsFilters = dict[str, TOracleWmsFilterValue]

# Configuration essentials - USED BY CONFIG
TOracleWmsEnvironment = Annotated[str, StringConstraints(min_length=1, max_length=50)]
TOracleWmsTimeout = Annotated[float, Field(gt=0, le=300)]


# =============================================================================
# TYPED DICTIONARIES - Structured Data Types
# =============================================================================


class TOracleWmsPaginationInfo(TypedDict):
    """Pagination information for Oracle WMS API responses."""

    current_page: int
    total_pages: int
    total_results: int
    has_next: bool
    has_previous: bool
    next_url: str | None
    previous_url: str | None


class TOracleWmsEntityInfo(TypedDict):
    """Oracle WMS entity information with metadata."""

    name: TOracleWmsEntityName
    description: str
    endpoint: str
    fields: TOracleWmsSchema
    primary_key: str | None
    replication_key: str | None
    supports_incremental: bool


class TOracleWmsDiscoveryResult(TypedDict):
    """Oracle WMS discovery result with entities and metadata."""

    entities: list[TOracleWmsEntityInfo]
    total_count: int
    discovered_at: str
    api_version: TOracleWmsApiVersion
    discovery_duration_ms: int


# =============================================================================
# API CATALOG ENUMS - API Classification
# =============================================================================


class FlextOracleWmsApiVersion(StrEnum):
    """Oracle WMS API versions."""

    LEGACY = "legacy"  # /wms/api/
    LGF_V10 = "v10"  # /wms/lgfapi/v10/


class FlextOracleWmsApiCategory(StrEnum):
    """Oracle WMS API categories from official documentation."""

    SETUP_TRANSACTIONAL = "setup_transactional"
    AUTOMATION_OPERATIONS = "automation_operations"
    DATA_EXTRACT = "data_extract"
    ENTITY_OPERATIONS = "entity_operations"


# =============================================================================
# CORE DATA MODELS - Essential Oracle WMS Models
# =============================================================================


@dataclass(frozen=True)
class FlextOracleWmsEntity(FlextValueObject):
    """Oracle WMS entity model - USED BY DISCOVERY."""

    name: str
    endpoint: str
    description: str | None = None
    fields: dict[str, object] | None = field(default_factory=dict)
    primary_key: str | None = None
    replication_key: str | None = None
    supports_incremental: bool = False

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate entity business rules."""
        from flext_oracle_wms.wms_operations import (
            validate_string_parameter,
        )

        validation_errors = []

        try:
            validate_string_parameter(self.name, "entity name")
            validate_string_parameter(self.endpoint, "entity endpoint")
        except (TypeError, ValueError, AttributeError) as e:
            validation_errors.append(str(e))

        if not self.endpoint.startswith("/"):
            validation_errors.append("Entity endpoint must start with /")

        max_length = FlextOracleWmsDefaults.MAX_ENTITY_NAME_LENGTH
        if len(self.name) > max_length:
            validation_errors.append(
                f"Entity name too long (max {max_length} characters)",
            )

        if validation_errors:
            return FlextResult.fail(
                f"{FlextOracleWmsErrorMessages.ENTITY_VALIDATION_FAILED}: {'; '.join(validation_errors)}",
            )
        return FlextResult.ok(None)


@dataclass(frozen=True)
class FlextOracleWmsDiscoveryResult(FlextValueObject):
    """Oracle WMS discovery result - USED BY DISCOVERY."""

    entities: list[FlextOracleWmsEntity] = field(default_factory=list)
    total_count: int = 0
    timestamp: str = ""
    discovery_duration_ms: float = 0.0
    has_errors: bool = False
    errors: list[str] = field(default_factory=list)
    api_version: str | None = None

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate discovery result."""
        from flext_oracle_wms.wms_operations import (
            validate_records_list,
        )

        validation_errors = []

        try:
            validate_records_list(self.entities, "entities")
        except (TypeError, ValueError, AttributeError) as e:
            validation_errors.append(str(e))

        if self.total_count < 0:
            validation_errors.append("Total count cannot be negative")

        if self.entities and len(self.entities) != self.total_count:
            validation_errors.append("Entity count mismatch")

        # Validate all entities
        for entity in self.entities:
            entity_validation = entity.validate_business_rules()
            if not entity_validation.success:
                validation_errors.append(
                    f"Entity {entity.name}: {entity_validation.error}",
                )

        if validation_errors:
            return FlextResult.fail(
                f"{FlextOracleWmsErrorMessages.DISCOVERY_FAILED}: {'; '.join(validation_errors)}",
            )
        return FlextResult.ok(None)


@dataclass(frozen=True)
class FlextOracleWmsApiResponse(FlextValueObject):
    """Oracle WMS API response wrapper - USED BY CLIENT."""

    data: dict[str, object] = field(default_factory=dict)
    status_code: int = 200
    success: bool = True
    error_message: str | None = None

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate API response."""
        from flext_oracle_wms.wms_operations import (
            validate_dict_parameter,
        )

        validation_errors = []

        try:
            validate_dict_parameter(self.data, "data")
        except (TypeError, ValueError, AttributeError) as e:
            validation_errors.append(str(e))

        min_code = FlextOracleWmsDefaults.MIN_HTTP_STATUS_CODE
        max_code = FlextOracleWmsDefaults.MAX_HTTP_STATUS_CODE
        if self.status_code < min_code or self.status_code > max_code:
            validation_errors.append(f"Invalid HTTP status code: {self.status_code}")

        if not self.success and not self.error_message:
            validation_errors.append("Failed response must have error message")

        if validation_errors:
            return FlextResult.fail(
                f"{FlextOracleWmsErrorMessages.INVALID_RESPONSE}: {'; '.join(validation_errors)}",
            )
        return FlextResult.ok(None)


@dataclass(frozen=True)
class FlextOracleWmsApiEndpoint(FlextValueObject):
    """Declarative API endpoint definition - FROM API_CATALOG."""

    name: str
    method: str
    path: str
    version: FlextOracleWmsApiVersion
    category: FlextOracleWmsApiCategory
    description: str
    since_version: str = "6.1"

    def get_full_path(self, environment: str) -> str:
        """Get full API path with environment."""
        if self.version == FlextOracleWmsApiVersion.LGF_V10:
            return f"/{environment}/wms/lgfapi/v10{self.path}"
        return f"/{environment}/wms/api{self.path}"

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate Oracle WMS API endpoint business rules."""
        validation_errors = []

        if not self.name:
            validation_errors.append("API name cannot be empty")
        if not self.method:
            validation_errors.append("HTTP method cannot be empty")
        if not self.path:
            validation_errors.append("API path cannot be empty")
        if self.method not in {"GET", "POST", "PUT", "PATCH", "DELETE"}:
            validation_errors.append(f"Invalid HTTP method: {self.method}")
        if not self.path.startswith("/"):
            validation_errors.append("API path must start with /")
        if not self.description:
            validation_errors.append("API description cannot be empty")

        if validation_errors:
            return FlextResult.fail("; ".join(validation_errors))
        return FlextResult.ok(None)


# =============================================================================
# EXPORTS
# =============================================================================

__all__: list[str] = [
    "FlextOracleWmsApiCategory",
    "FlextOracleWmsApiEndpoint",
    "FlextOracleWmsApiResponse",
    # Enums
    "FlextOracleWmsApiVersion",
    "FlextOracleWmsDiscoveryResult",
    # Core Models
    "FlextOracleWmsEntity",
    "TOracleWmsApiResponse",
    "TOracleWmsApiVersion",
    "TOracleWmsDiscoveryResult",
    "TOracleWmsEntityId",
    "TOracleWmsEntityInfo",
    "TOracleWmsEntityName",
    "TOracleWmsEnvironment",
    "TOracleWmsFilterValue",
    "TOracleWmsFilters",
    # Typed Dictionaries
    "TOracleWmsPaginationInfo",
    # Type Definitions
    "TOracleWmsRecord",
    "TOracleWmsRecordBatch",
    "TOracleWmsSchema",
    "TOracleWmsTimeout",
]
