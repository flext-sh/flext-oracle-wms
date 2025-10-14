"""Oracle WMS Models - Consolidated Data Models and Types.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT.

Consolidated Oracle WMS data models, type definitions, and entity structures.
This module combines models.py + types.py + core entities from api_catalog.py
into a single unified data model system.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Annotated, Literal, TypedDict

from flext_core import FlextCore
from pydantic import Field, StringConstraints

from flext_oracle_wms.constants import (
    FlextOracleWmsApiVersion,
    FlextOracleWmsConstants,
)
from flext_oracle_wms.typings import FlextOracleWmsTypes

# Core record types - USED EVERYWHERE
TOracleWmsRecord = FlextOracleWmsTypes.Core.Dict
TOracleWmsRecordBatch = list[TOracleWmsRecord]
TOracleWmsSchema = dict[str, FlextOracleWmsTypes.Core.Dict]

# API types - USED BY CLIENT
TOracleWmsApiResponse = FlextOracleWmsTypes.Core.Dict
TOracleWmsApiVersion = Literal["v10", "v9", "v8", "legacy"]

# Entity naming - USED BY CLIENT/DISCOVERY
TOracleWmsEntityId = Annotated[str, StringConstraints(min_length=1, max_length=100)]
TOracleWmsEntityName = Annotated[
    str,
    StringConstraints(min_length=1, max_length=50, pattern=r"^[a-z0-9_]+$"),
]

# Filter types - USED BY FILTERING MODULE
TOracleWmsFilterValue = (
    (str | int | float)
    | (bool | list[str | int | float])
    | FlextOracleWmsTypes.Core.Dict
)
TOracleWmsFilters = dict[str, TOracleWmsFilterValue]

# Configuration essentials - USED BY CONFIG
TOracleWmsEnvironment = Annotated[str, StringConstraints(min_length=1, max_length=50)]
TOracleWmsTimeout = Annotated[float, Field(gt=0, le=300)]


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


class FlextOracleWmsApiCategory(StrEnum):
    """Oracle WMS API categories from official documentation."""

    SETUP_TRANSACTIONAL = "setup_transactional"
    AUTOMATION_OPERATIONS = "automation_operations"
    DATA_EXTRACT = "data_extract"
    ENTITY_OPERATIONS = "entity_operations"


@dataclass(frozen=True)
class FlextOracleWmsEntity(FlextCore.Models):
    """Oracle WMS entity model - USED BY DISCOVERY."""

    name: str
    endpoint: str
    description: str | None = None
    fields: FlextOracleWmsTypes.Core.Dict | None = field(default_factory=dict)
    primary_key: str | None = None
    replication_key: str | None = None
    supports_incremental: bool = False

    def validate_business_rules(self) -> FlextCore.Result[None]:
        """Validate entity business rules."""
        validation_errors: FlextCore.Types.StringList = []

        # Business rule: entity name cannot be empty
        if not self.name.strip():
            validation_errors.append("Entity name cannot be empty")

        if not self.endpoint.startswith("/"):
            validation_errors.append("Entity endpoint must start with /")

        max_length = FlextOracleWmsConstants.Entities.MAX_ENTITY_NAME_LENGTH
        if len(self.name) > max_length:
            validation_errors.append(
                f"Entity name too long (max {max_length} characters)",
            )

        if validation_errors:
            error_messages = [
                str(error) for error in validation_errors if error is not None
            ]
            return FlextCore.Result[None].fail(
                f"{FlextOracleWmsConstants.ErrorMessages.ENTITY_VALIDATION_FAILED}: {'; '.join(error_messages)}",
            )
        return FlextCore.Result[None].ok(None)

    def to_dict_basic(self) -> FlextOracleWmsTypes.Core.Dict:
        """Convert entity to basic dict[str, object] format (used by discovery)."""
        return {
            "name": self.name,
            "endpoint": self.endpoint,
            "description": self.description,
            "primary_key": self.primary_key,
            "replication_key": self.replication_key,
            "supports_incremental": self.supports_incremental,
        }


@dataclass(frozen=True)
class FlextOracleWmsDiscoveryResult(FlextCore.Models):
    """Oracle WMS discovery result - USED BY DISCOVERY."""

    entities: list[FlextOracleWmsEntity] = field(default_factory=list)
    total_count: int = 0
    timestamp: str = ""
    discovery_duration_ms: float = 0.0
    has_errors: bool = False
    errors: FlextOracleWmsTypes.Core.StringList = field(default_factory=list)
    api_version: str | None = "v10"

    def validate_business_rules(self) -> FlextCore.Result[None]:
        """Validate discovery result."""
        validation_errors: FlextCore.Types.StringList = []

        # Entities list is already typed as list[TOracleWmsEntityInfo]

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
            return FlextCore.Result[None].fail(
                f"{FlextOracleWmsConstants.ErrorMessages.DISCOVERY_FAILED}: {'; '.join(validation_errors)}",
            )
        return FlextCore.Result[None].ok(None)


@dataclass(frozen=True)
class FlextOracleWmsApiResponse(FlextCore.Models):
    """Oracle WMS API response wrapper - USED BY CLIENT."""

    data: FlextOracleWmsTypes.Core.Dict = field(default_factory=dict)
    status_code: int = 200
    success: bool = True
    error_message: str | None = None

    def validate_business_rules(self) -> FlextCore.Result[None]:
        """Validate API response."""
        validation_errors: FlextCore.Types.StringList = []

        # Data is already typed as FlextOracleWmsTypes.Core.Dict

        min_code = FlextOracleWmsConstants.Api.MIN_HTTP_STATUS_CODE
        max_code = FlextOracleWmsConstants.Api.MAX_HTTP_STATUS_CODE
        if self.status_code < min_code or self.status_code > max_code:
            validation_errors.append(f"Invalid HTTP status code: {self.status_code}")

        if not self.success and not self.error_message:
            validation_errors.append("Failed response must have error message")

        if validation_errors:
            return FlextCore.Result[None].fail(
                f"{FlextOracleWmsConstants.ErrorMessages.INVALID_RESPONSE}: {'; '.join(str(e) for e in validation_errors)}",
            )
        return FlextCore.Result[None].ok(None)


@dataclass(frozen=True)
class FlextOracleWmsApiEndpoint(FlextCore.Models):
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

    def validate_business_rules(self) -> FlextCore.Result[None]:
        """Validate Oracle WMS API endpoint business rules."""
        validation_errors: FlextCore.Types.StringList = []

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
            return FlextCore.Result[None].fail("; ".join(validation_errors))
        return FlextCore.Result[None].ok(None)


__all__: FlextOracleWmsTypes.Core.StringList = [
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
    "TOracleWmsPaginationInfo",
    "TOracleWmsRecord",
    "TOracleWmsRecordBatch",
    "TOracleWmsSchema",
    "TOracleWmsTimeout",
]
