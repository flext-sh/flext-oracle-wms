"""Oracle WMS Essential Types - Only what's actually used.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Minimal Oracle WMS types - only what's actually needed.
"""

from __future__ import annotations

from typing import Annotated, Any, Literal, TypedDict

# Import validation from Pydantic
from pydantic import Field, StringConstraints

# =================================================================
# ESSENTIAL TYPES ONLY - ACTUALLY USED
# =================================================================

# Core record types - USED EVERYWHERE
TOracleWmsRecord = dict[str, Any]
TOracleWmsRecordBatch = list[TOracleWmsRecord]
TOracleWmsSchema = dict[str, dict[str, Any]]

# API types - USED BY CLIENT
TOracleWmsApiResponse = dict[str, Any]
TOracleWmsApiVersion = Literal["v10", "v11", "legacy"]

# Entity naming - USED BY CLIENT/DISCOVERY
TOracleWmsEntityId = Annotated[str, StringConstraints(min_length=1, max_length=100)]
TOracleWmsEntityName = Annotated[
    str, StringConstraints(min_length=1, max_length=50, pattern=r"^[a-z0-9_]+$")
]

# Filter types - USED BY FILTERING MODULE
TOracleWmsFilterValue = str | int | float | bool | list[str | int | float]
TOracleWmsFilters = dict[str, TOracleWmsFilterValue]

# Configuration essentials - USED BY CONFIG
TOracleWmsEnvironment = Annotated[str, StringConstraints(min_length=1, max_length=50)]
TOracleWmsTimeout = Annotated[float, Field(gt=0, le=300)]


# Pagination - USED BY HELPERS/CLIENT
class TOracleWmsPaginationInfo(TypedDict):
    """Pagination information for Oracle WMS API responses."""

    current_page: int
    total_pages: int
    total_results: int
    has_next: bool
    has_previous: bool
    next_url: str | None
    previous_url: str | None


# Discovery essentials - USED BY DISCOVERY
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
