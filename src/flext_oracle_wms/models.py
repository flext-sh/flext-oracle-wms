"""Enterprise Oracle WMS data models using flext-core standards.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Ultra-modern Python 3.13 models with MAXIMUM flext-core integration.
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Annotated, Any

# Import from flext-core root namespace as required
from flext_core import FlextResult
from pydantic import BaseModel, Field

# Import constants for runtime usage

# Define WMS-specific types at runtime - needed for Pydantic models
WMSPageSize = Annotated[int, Field(ge=1, le=10000)]
WMSRecord = dict[str, Any]
WMSFieldName = str

if TYPE_CHECKING:
    from flext_oracle_wms.constants import OracleWMSEntityType
    from flext_oracle_wms.typedefs import WMSSchema

    # Define WMS-specific types for this module
    WMSErrorCode = str
    WMSErrorMessage = str


class FlextOracleWmsEntity(BaseModel):
    """Oracle WMS entity model using flext-core standards."""

    name: str = Field(
        ...,
        description="Oracle WMS entity name",
    )
    description: str | None = Field(
        None,
        description="Human-readable entity description",
    )
    fields: dict[str, Any] = Field(
        default_factory=dict,
        description="Entity schema fields using flext-core WMS types",
    )
    endpoint: str = Field(..., description="Oracle WMS API endpoint for this entity")

    # Additional Oracle WMS entity metadata
    primary_key: str | None = Field(None, description="Primary key field for entity")
    replication_key: str | None = Field(
        None,
        description="Replication key for incremental sync",
    )
    supports_incremental: bool = Field(
        default=False,
        description="Whether entity supports incremental extraction",
    )


class FlextOracleWmsDiscoveryResult(BaseModel):
    """Oracle WMS discovery result using flext-core standards."""

    entities: list[FlextOracleWmsEntity] = Field(
        default_factory=list,
        description="List of discovered Oracle WMS entities",
    )
    total_count: int = Field(
        default=0,
        description="Total number of discovered entities",
    )
    timestamp: str = Field(..., description="Discovery timestamp in ISO format")

    # Additional discovery metadata
    api_version: str | None = Field(
        None,
        description="Oracle WMS API version used for discovery",
    )
    discovery_duration_ms: float | None = Field(
        None,
        description="Time taken for discovery in milliseconds",
    )
    has_errors: bool = Field(
        default=False,
        description="Whether discovery encountered any errors",
    )
    errors: list[str] = Field(
        default_factory=list,
        description="List of discovery errors if any",
    )


class FlextOracleWmsError(BaseModel):
    """Oracle WMS error model using flext-core standards."""

    code: str | None = Field(
        None,
        description="Oracle WMS error code using flext-core validation",
    )
    message: str | None = Field(
        None,
        description="Oracle WMS error message using flext-core validation",
    )
    details: dict[str, Any] | None = Field(
        None,
        description="Additional error context and details",
    )

    # Enhanced error metadata
    timestamp: datetime | None = Field(None, description="When the error occurred")
    entity_name: str | None = Field(
        None,
        description="Oracle WMS entity associated with error",
    )
    field_name: WMSFieldName | None = Field(
        None,
        description="Specific field that caused the error",
    )
    recoverable: bool = Field(
        default=True,
        description="Whether this error can be recovered from",
    )
    retry_count: int = Field(default=0, description="Number of retry attempts made")

    # Additional fields for test compatibility
    error_type: str | None = Field(None, description="Error type classification")
    endpoint: str | None = Field(None, description="API endpoint where error occurred")
    status_code: int | None = Field(None, description="HTTP status code")
    retryable: bool | None = Field(None, description="Whether error is retryable")
    request_id: str | None = Field(None, description="Request ID for tracking")


class FlextOracleWmsResponse(BaseModel):
    """Oracle WMS API response using flext-core standards."""

    data: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Oracle WMS response data - flexible structure for any entity",
    )
    records: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Oracle WMS records - flexible structure for any entity",
    )
    total_count: int = Field(
        default=0,
        description="Total number of records in response",
    )
    page_size: WMSPageSize = Field(
        default=100,
        description="Page size using flext-core WMS validation",
    )
    has_more: bool = Field(
        default=False,
        description="Whether more pages are available",
    )

    # Enhanced Oracle WMS response metadata
    entity_name: str | None = Field(
        None,
        description="Oracle WMS entity name for this response",
    )
    api_version: str | None = Field(None, description="Oracle WMS API version used")
    response_time_ms: float | None = Field(
        None,
        description="API response time in milliseconds",
    )
    extracted_at: datetime | None = Field(
        None,
        description="When the data was extracted from Oracle WMS",
    )
    cursor_bookmark: str | None = Field(
        None,
        description="Pagination cursor for next page",
    )

    def model_post_init(self, __context: Any, /) -> None:
        """Post-init hook to synchronize records and data fields."""
        # Synchronize data and records for backward compatibility
        if hasattr(self, "data") and self.data and not getattr(self, "records", None):
            object.__setattr__(self, "records", self.data)
        elif (
            hasattr(self, "records")
            and self.records
            and not getattr(self, "data", None)
        ):
            object.__setattr__(self, "data", self.records)


class FlextOracleWmsEntityField(BaseModel):
    """Oracle WMS entity field definition using flext-core standards."""

    name: WMSFieldName = Field(
        ...,
        description="Field name using flext-core WMS validation",
    )
    type: str = Field(
        ...,
        description="Oracle WMS field data type (string, integer, number, etc.)",
    )
    required: bool = Field(
        default=False,
        description="Whether this field is required by Oracle WMS",
    )
    description: str | None = Field(
        None,
        description="Human-readable field description",
    )

    # Enhanced Oracle WMS field metadata
    max_length: int | None = Field(
        None,
        description="Maximum field length for string types",
    )
    nullable: bool = Field(
        default=True,
        description="Whether field can be null in Oracle WMS",
    )
    primary_key: bool = Field(
        default=False,
        description="Whether this field is part of primary key",
    )
    indexed: bool = Field(
        default=False,
        description="Whether this field is indexed in Oracle WMS",
    )
    format: str | None = Field(
        None,
        description="Field format (e.g., 'date-time', 'email', etc.)",
    )
    enum_values: list[str] | None = Field(
        None,
        description="Allowed enum values for this field",
    )


class FlextOracleWmsRecordModel(BaseModel):
    """Oracle WMS record model using flext-core standards."""

    data: dict[str, Any] = Field(
        default_factory=dict,
        description="Oracle WMS record data using flext-core validation",
    )
    entity: str = Field(
        ...,
        description="Oracle WMS entity name using flext-core types",
    )
    record_id: str | None = Field(
        None, description="Unique record identifier from Oracle WMS"
    )

    # Enhanced Oracle WMS record metadata
    extracted_at: datetime | None = Field(
        None,
        description="When this record was extracted from Oracle WMS",
    )
    mod_ts: datetime | None = Field(
        None,
        description="Last modification timestamp from Oracle WMS",
    )
    record_version: int | None = Field(
        None,
        description="Record version for optimistic locking",
    )
    checksum: str | None = Field(
        None,
        description="Data checksum for integrity validation",
    )
    flattened: bool = Field(
        default=False,
        description="Whether record data has been flattened",
    )
    original_structure: dict[str, Any] | None = Field(
        None,
        description="Original nested structure before flattening",
    )


# Models are ready for use with runtime type resolution

__all__ = [
    "FlextOracleWmsDiscoveryResult",
    "FlextOracleWmsEntity",
    "FlextOracleWmsEntityField",
    "FlextOracleWmsError",
    "FlextOracleWmsRecordModel",
    "FlextOracleWmsResponse",
]
