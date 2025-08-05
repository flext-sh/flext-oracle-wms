"""Oracle WMS Type Definitions and Aliases.

This module provides comprehensive type definitions for Oracle WMS Cloud integration,
including type aliases, typed dictionaries, and validation constraints for enterprise
data processing and API operations.

Key Features:
    - Type-safe aliases for Oracle WMS data structures
    - Pydantic-based validation constraints for data integrity
    - Comprehensive type definitions for API responses and entities
    - Type safety for Oracle WMS entity operations and discovery
    - Integration with Python's typing system for IDE support

Architecture:
    Provides foundation type definitions used throughout the FLEXT Oracle WMS library:
    - Record and batch processing types for data operations
    - API response and version type definitions
    - Entity identification and naming constraints
    - Schema and metadata type definitions
    - Type-safe configuration and validation patterns

Type Categories:
    - Core Data Types: Record processing and batch operations
    - API Types: Response structures and version management
    - Entity Types: Entity identification and discovery operations
    - Schema Types: Dynamic schema and metadata processing
    - Validation Types: Type constraints and data validation

Integration:
    - Native Python typing system compatibility
    - Pydantic validation framework integration
    - MyPy static type checking support
    - IDE intellisense and type hint support
    - Enterprise development tooling compatibility

Author: FLEXT Development Team
Version: 0.9.0
License: MIT
"""

from __future__ import annotations

from typing import Annotated, Literal, TypedDict

# Import validation from Pydantic
from pydantic import Field, StringConstraints

# =================================================================
# ESSENTIAL TYPES ONLY - ACTUALLY USED
# =================================================================

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
