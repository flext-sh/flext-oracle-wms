"""FLEXT WMS Constants - Generic WMS constants with patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from enum import StrEnum
from typing import ClassVar, Final, Literal

from flext_core import c as c_core


class FlextOracleWmsConstants(c_core):
    """Generic WMS constants class with composition patterns.

    Uses Python 3.13+ syntax, reduces declarations through patterns.
    One class per module following SOLID principles. Generic for any WMS system.
    """

    # Core domain constants using advanced patterns
    FLEXT_WMS_VERSION: Final[str] = "0.9.0"

    # Application metadata - composed into single dict
    APP_METADATA: Final[dict[str, str]] = {
        "name": "flext-wms",
        "description": "FLEXT Generic WMS Integration",
        "author": "FLEXT Team",
        "license": "MIT",
    }

    # API configuration - composed patterns
    API_CONFIG: Final[dict[str, str | int]] = {
        "version_default": "v1",
        "base_url_default": "https://api.wms.example.com",
        "timeout_default": c_core.Defaults.TIMEOUT * 2,
        "max_retries": 3,
        "rate_limit_per_minute": 1000,
    }

    # Authentication constants - advanced composition
    # AUTH_CONFIG is created after OracleWMSAuthMethod StrEnum definition (see below)
    AUTH_CONFIG: ClassVar[dict[str, str | object]]

    # Entity types - will be generated from WmsEntityType StrEnum after definition

    # Batch and performance - advanced dict composition
    PROCESSING_CONFIG: Final[dict[str, int]] = {
        "default_batch_size": c_core.Defaults.PAGE_SIZE * 10,
        "max_batch_size": c_core.Defaults.PAGE_SIZE * 100,
        "default_page_size": c_core.Defaults.PAGE_SIZE,
        "cache_ttl_default": 3600,
        "cache_max_size": 10000,
        "cache_cleanup_interval": 300,
        "max_retry_attempts": 3,
        "retry_delay_base": 1,
        "retry_delay_max": 60,
        "performance_warning_threshold": 5000,
        "performance_critical_threshold": 10000,
    }

    # Environment configuration
    ENVIRONMENTS: Final[dict[str, str]] = {
        "default": "default",
        "test": "test",
        "production": "production",
    }

    # Nested classes with advanced composition
    class OracleWms:
        """WMS connection constants - composed from base."""

        DEFAULT_TIMEOUT: Final[int] = c_core.Network.DEFAULT_TIMEOUT
        DEFAULT_MAX_RETRIES: Final[int] = c_core.Reliability.MAX_RETRY_ATTEMPTS
        DEFAULT_RETRY_DELAY: Final[int] = c_core.Reliability.DEFAULT_RETRY_DELAY_SECONDS
        DEFAULT_POOL_SIZE: Final[int] = c_core.Network.DEFAULT_CONNECTION_POOL_SIZE
        MAX_POOL_SIZE: Final[int] = c_core.Network.MAX_CONNECTION_POOL_SIZE

    class WmsEntities:
        """WMS entity configuration - patterns."""

        MAX_ENTITY_NAME_LENGTH: ClassVar[int] = 100
        ENTITY_NAME_PATTERN: ClassVar[str] = r"^[a-zA-Z][a-zA-Z0-9_]*$"
        # TYPES is generated from WmsEntityType StrEnum after definition (see below)
        TYPES: ClassVar[tuple[str, ...]]

    class WmsProcessing:
        """WMS processing constants - domain-specific."""

        DEFAULT_BATCH_SIZE: Final[int] = c_core.Performance.BatchProcessing.DEFAULT_SIZE
        MAX_BATCH_SIZE: Final[int] = c_core.Performance.BatchProcessing.MAX_ITEMS
        DEFAULT_PAGE_SIZE: Final[int] = c_core.Pagination.DEFAULT_PAGE_SIZE
        MAX_SCHEMA_DEPTH: ClassVar[int] = 10

    class Filtering:
        """Filtering constants - minimal declaration."""

        MAX_FILTER_CONDITIONS: ClassVar[int] = 50

    class ErrorMessages:
        """Error messages - composed dict pattern."""

        MESSAGES: ClassVar[dict[str, str]] = {
            "entity_validation_failed": "Entity validation failed",
            "discovery_failed": "Entity discovery failed",
            "invalid_response": "Invalid API response",
            "connection_failed": "Connection to WMS failed",
            "authentication_failed": "Authentication failed",
        }

    class ResponseFields:
        """Response fields - composed pattern."""

        FIELDS: ClassVar[dict[str, str]] = {
            "result_count": "result_count",
            "results": "results",
            "data": "data",
            "total_count": "total_count",
            "page_number": "page_number",
            "page_count": "page_count",
            "next_page": "next_page",
            "previous_page": "previous_page",
        }

    class Authentication:
        """Auth constants - minimal."""

        MIN_TOKEN_LENGTH: ClassVar[int] = 10
        MIN_API_KEY_LENGTH: ClassVar[int] = 20

    class WmsPagination:
        """Pagination constants."""

        DEFAULT_PAGE_SIZE: ClassVar[int] = 100

    class Api:
        """API constants - composed."""

        CONFIG: ClassVar[dict[str, int]] = {
            "default_timeout": 60,
            "min_http_status_code": 200,
            "max_http_status_code": 599,
        }

    # Enums - advanced StrEnum composition
    class WmsEntityType(StrEnum):
        """Entity types.

        DRY Pattern: This StrEnum is the single source of truth for WMS entity types.
        All entity type-related constants and Literal types MUST reference this enum.
        """

        INVENTORY = "inventory"
        ORDERS = "orders"
        SHIPMENTS = "shipments"
        PICKING = "picking"
        LOCATIONS = "locations"
        ITEMS = "items"
        PRODUCTS = "products"
        WAREHOUSES = "warehouses"

    # Generate ENTITY_TYPES list from StrEnum for backward compatibility
    ENTITY_TYPES: Final[tuple[str, ...]] = tuple(
        member.value for member in WmsEntityType.__members__.values()
    )

    # Generate WmsEntities.TYPES from StrEnum (uppercase for backward compatibility)
    # Set class attribute after enum definition
    WmsEntities.TYPES = tuple(
        member.name for member in WmsEntityType.__members__.values()
    )

    # PEP 695 Literal type referencing StrEnum members
    type WmsEntityTypeLiteral = Literal[
        WmsEntityType.INVENTORY,
        WmsEntityType.ORDERS,
        WmsEntityType.SHIPMENTS,
        WmsEntityType.PICKING,
        WmsEntityType.LOCATIONS,
        WmsEntityType.ITEMS,
        WmsEntityType.PRODUCTS,
        WmsEntityType.WAREHOUSES,
    ]

    class WmsApiVersion(StrEnum):
        """API versions.

        DRY Pattern: This StrEnum is the single source of truth for WMS API versions.
        All API version-related constants and Literal types MUST reference this enum.
        """

        V1 = "v1"
        V2 = "v2"
        V3 = "v3"
        LEGACY = "legacy"

    # PEP 695 Literal type referencing StrEnum members
    type WmsApiVersionLiteral = Literal[
        WmsApiVersion.V1,
        WmsApiVersion.V2,
        WmsApiVersion.V3,
        WmsApiVersion.LEGACY,
    ]

    class WmsApiCategory(StrEnum):
        """API categories.

        DRY Pattern: This StrEnum is the single source of truth for WMS API categories.
        All API category-related constants and Literal types MUST reference this enum.
        """

        INVENTORY = "inventory"
        ORDERS = "orders"
        SHIPPING = "shipping"
        RECEIVING = "receiving"
        REPORTING = "reporting"

    # PEP 695 Literal type referencing StrEnum members
    type WmsApiCategoryLiteral = Literal[
        WmsApiCategory.INVENTORY,
        WmsApiCategory.ORDERS,
        WmsApiCategory.SHIPPING,
        WmsApiCategory.RECEIVING,
        WmsApiCategory.REPORTING,
    ]

    class WmsOperationStatus(StrEnum):
        """Operation status values.

        DRY Pattern: This StrEnum is the single source of truth for WMS operation statuses.
        All operation status-related constants and Literal types MUST reference this enum.
        """

        PENDING = "pending"
        RUNNING = "running"
        SUCCESS = "success"
        ERROR = "error"
        TIMEOUT = "timeout"
        CANCELLED = "cancelled"

    # PEP 695 Literal type referencing StrEnum members
    type WmsOperationStatusLiteral = Literal[
        WmsOperationStatus.PENDING,
        WmsOperationStatus.RUNNING,
        WmsOperationStatus.SUCCESS,
        WmsOperationStatus.ERROR,
        WmsOperationStatus.TIMEOUT,
        WmsOperationStatus.CANCELLED,
    ]

    class WmsDataQuality(StrEnum):
        """Data quality levels.

        DRY Pattern: This StrEnum is the single source of truth for WMS data quality levels.
        All data quality-related constants and Literal types MUST reference this enum.
        """

        HIGH = "high"
        MEDIUM = "medium"
        LOW = "low"
        UNKNOWN = "unknown"

    # PEP 695 Literal type referencing StrEnum members
    type WmsDataQualityLiteral = Literal[
        WmsDataQuality.HIGH,
        WmsDataQuality.MEDIUM,
        WmsDataQuality.LOW,
        WmsDataQuality.UNKNOWN,
    ]

    class WmsFilterOperator(StrEnum):
        """Filter operators.

        DRY Pattern: This StrEnum is the single source of truth for WMS filter operators.
        All filter operator-related constants and Literal types MUST reference this enum.
        """

        EQ = "eq"
        NE = "ne"
        GT = "gt"
        GTE = "gte"
        LT = "lt"
        LTE = "lte"
        IN = "in"
        NOT_IN = "not_in"
        CONTAINS = "contains"
        STARTS_WITH = "starts_with"
        ENDS_WITH = "ends_with"

    # PEP 695 Literal type referencing StrEnum members
    type WmsFilterOperatorLiteral = Literal[
        WmsFilterOperator.EQ,
        WmsFilterOperator.NE,
        WmsFilterOperator.GT,
        WmsFilterOperator.GTE,
        WmsFilterOperator.LT,
        WmsFilterOperator.LTE,
        WmsFilterOperator.IN,
        WmsFilterOperator.NOT_IN,
        WmsFilterOperator.CONTAINS,
        WmsFilterOperator.STARTS_WITH,
        WmsFilterOperator.ENDS_WITH,
    ]

    class WmsPageMode(StrEnum):
        """Page modes.

        DRY Pattern: This StrEnum is the single source of truth for WMS page modes.
        All page mode-related constants and Literal types MUST reference this enum.
        """

        APPEND = "append"
        REPLACE = "replace"
        MERGE = "merge"

    # PEP 695 Literal type referencing StrEnum members
    type WmsPageModeLiteral = Literal[
        WmsPageMode.APPEND,
        WmsPageMode.REPLACE,
        WmsPageMode.MERGE,
    ]

    class WmsWriteMode(StrEnum):
        """Write modes.

        DRY Pattern: This StrEnum is the single source of truth for WMS write modes.
        All write mode-related constants and Literal types MUST reference this enum.
        """

        INSERT = "insert"
        UPDATE = "update"
        UPSERT = "upsert"
        DELETE = "delete"

    # PEP 695 Literal type referencing StrEnum members
    type WmsWriteModeLiteral = Literal[
        WmsWriteMode.INSERT,
        WmsWriteMode.UPDATE,
        WmsWriteMode.UPSERT,
        WmsWriteMode.DELETE,
    ]

    class EndpointDiscoveryStrategy(StrEnum):
        """Discovery strategy enum.

        DRY Pattern: This StrEnum is the single source of truth for discovery strategies.
        All discovery strategy-related constants and Literal types MUST reference this enum.
        """

        API_BASED = "api_based"
        SCHEMA_BASED = "schema_based"


# Module-level enums for direct import - advanced composition
class OracleWMSAuthMethod(StrEnum):
    """Auth methods.

    DRY Pattern: This StrEnum is the single source of truth for Oracle WMS authentication methods.
    All authentication method-related constants and Literal types MUST reference this enum.
    """

    BASIC = "basic"
    OAUTH2 = "oauth2"
    API_KEY = "api_key"
    BEARER = "bearer"


# Generate AUTH_CONFIG with auth method values from StrEnum
# Set class attribute after enum definition
FlextOracleWmsConstants.AUTH_CONFIG = {
    "basic": OracleWMSAuthMethod.BASIC,
    "oauth2": OracleWMSAuthMethod.OAUTH2,
    "api_key": OracleWMSAuthMethod.API_KEY,
    "bearer": OracleWMSAuthMethod.BEARER,
    "oauth2_token_endpoint": "/oauth2/token",
    "oauth2_scope_default": "read write",
}

# PEP 695 Literal type referencing StrEnum members
type OracleWMSAuthMethodLiteral = Literal[
    OracleWMSAuthMethod.BASIC,
    OracleWMSAuthMethod.OAUTH2,
    OracleWMSAuthMethod.API_KEY,
    OracleWMSAuthMethod.BEARER,
]


# Module-level aliases for backward compatibility
# Note: Cannot inherit from nested StrEnum classes, use type aliases instead
WmsFilterOperator = FlextOracleWmsConstants.WmsFilterOperator
WmsApiVersion = FlextOracleWmsConstants.WmsApiVersion
WmsApiCategory = FlextOracleWmsConstants.WmsApiCategory


c = FlextOracleWmsConstants

__all__ = [
    "FlextOracleWmsConstants",
    "OracleWMSAuthMethod",
    "WmsApiCategory",
    "WmsApiVersion",
    "WmsFilterOperator",
    "c",
]
