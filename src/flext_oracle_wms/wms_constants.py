"""FLEXT Oracle WMS Constants - Domain-specific Oracle WMS constants.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from enum import StrEnum
from typing import Final

from flext_core import FlextConstants, FlextTypes

# Python 3.13+ Type Aliases - ONLY Oracle WMS-specific
# Note: Using enum classes instead of type aliases for better runtime behavior


class FlextOracleWmsConstants(FlextConstants):
    """Single unified Oracle WMS constants class following FLEXT standards.

    Contains all constants for Oracle WMS domain operations.
    Follows FLEXT pattern: one class per module with nested subclasses.
    All constants are flat class attributes inheriting from FlextConstants.
    """

    # =========================================================================
    # VERSION METADATA (DOMAIN-SPECIFIC ONLY)
    # =========================================================================

    FLEXT_ORACLE_WMS_VERSION: Final[str] = "0.9.0"  # Domain-specific version

    # =========================================================================
    # DOMAIN-SPECIFIC CONSTANTS ONLY - FLAT CLASS STRUCTURE
    # =========================================================================

    # Application metadata constants
    APPLICATION_NAME: Final[str] = "flext-oracle-wms"
    APPLICATION_DESCRIPTION: Final[str] = "FLEXT Oracle WMS Cloud Integration"
    APPLICATION_AUTHOR: Final[str] = "FLEXT Team"
    APPLICATION_LICENSE: Final[str] = "MIT"

    # Oracle WMS API constants
    API_VERSION_DEFAULT: Final[str] = "v2"
    API_BASE_URL_DEFAULT: Final[str] = "https://wms.oraclecloud.com"
    API_TIMEOUT_DEFAULT: Final[int] = FlextConstants.Defaults.TIMEOUT * 2  # 60 seconds
    API_MAX_RETRIES: Final[int] = 3
    API_RATE_LIMIT_PER_MINUTE: Final[int] = 1000

    # Authentication constants
    AUTH_METHOD_BASIC: Final[str] = "basic"
    AUTH_METHOD_OAUTH2: Final[str] = "oauth2"
    AUTH_METHOD_API_KEY: Final[str] = "api_key"
    OAUTH2_TOKEN_ENDPOINT: Final[str] = "/oauth2/token"
    OAUTH2_SCOPE_DEFAULT: Final[str] = "wms.read wms.write"

    # Entity types
    ENTITY_TYPE_INVENTORY: Final[str] = "inventory"
    ENTITY_TYPE_ORDER: Final[str] = "order"
    ENTITY_TYPE_SHIPMENT: Final[str] = "shipment"
    ENTITY_TYPE_PICKING: Final[str] = "picking"
    ENTITY_TYPE_LOCATION: Final[str] = "location"
    ENTITY_TYPE_ITEM: Final[str] = "item"

    # Batch processing constants
    DEFAULT_BATCH_SIZE: Final[int] = FlextConstants.Defaults.PAGE_SIZE * 10  # 1000
    MAX_BATCH_SIZE: Final[int] = FlextConstants.Defaults.PAGE_SIZE * 100  # 10000
    DEFAULT_PAGE_SIZE: Final[int] = FlextConstants.Defaults.PAGE_SIZE  # 100

    # Cache constants
    CACHE_TTL_DEFAULT: Final[int] = 3600  # 1 hour
    CACHE_MAX_SIZE: Final[int] = 10000
    CACHE_CLEANUP_INTERVAL: Final[int] = 300  # 5 minutes

    # Error handling constants
    MAX_RETRY_ATTEMPTS: Final[int] = 3
    RETRY_DELAY_BASE: Final[int] = 1  # seconds
    RETRY_DELAY_MAX: Final[int] = 60  # seconds

    # Performance thresholds
    PERFORMANCE_WARNING_THRESHOLD: Final[int] = 5000  # 5 seconds
    PERFORMANCE_CRITICAL_THRESHOLD: Final[int] = 10000  # 10 seconds

    # Environment constants
    DEFAULT_ENVIRONMENT: Final[str] = "default"
    TEST_ENVIRONMENT: Final[str] = "test"
    PRODUCTION_ENVIRONMENT: Final[str] = "production"

    # API constants
    class Api:
        """Oracle WMS API constants."""

        DEFAULT_TIMEOUT: Final[int] = 60  # seconds
        MIN_HTTP_STATUS_CODE: Final[int] = 200
        MAX_HTTP_STATUS_CODE: Final[int] = 599

    # =========================================================================
    # DOMAIN-SPECIFIC ENUMS - NOT available in FlextConstants
    # =========================================================================

    class OracleWMSEntityType(StrEnum):
        """Oracle WMS entity types - domain-specific to warehouse management."""

        INVENTORY = "inventory"
        ORDER = "order"
        SHIPMENT = "shipment"
        PICKING = "picking"
        LOCATION = "location"
        ITEM = "item"

    class OracleWMSApiVersion(StrEnum):
        """Oracle WMS API versions."""

        V1 = "v1"
        V2 = "v2"
        LGF_V10 = "v10"
        LEGACY = "legacy"

    class OracleWMSAuthMethod(StrEnum):
        """Oracle WMS authentication methods."""

        BASIC = "basic"
        OAUTH2 = "oauth2"
        API_KEY = "api_key"

    class OracleWMSOperationStatus(StrEnum):
        """Oracle WMS operation status enumeration."""

        PENDING = "pending"
        RUNNING = "running"
        SUCCESS = "success"
        ERROR = "error"
        TIMEOUT = "timeout"
        CANCELLED = "cancelled"

    class OracleWMSDataQuality(StrEnum):
        """Oracle WMS data quality levels."""

        HIGH = "high"
        MEDIUM = "medium"
        LOW = "low"
        UNKNOWN = "unknown"

    class OracleWMSFilterOperator(StrEnum):
        """Oracle WMS filter operators."""

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

    class OracleWMSPageMode(StrEnum):
        """Oracle WMS page mode enumeration."""

        APPEND = "append"
        REPLACE = "replace"
        MERGE = "merge"

    class OracleWMSWriteMode(StrEnum):
        """Oracle WMS write mode enumeration."""

        INSERT = "insert"
        UPDATE = "update"
        UPSERT = "upsert"
        DELETE = "delete"

    # =========================================================================
    # DOMAIN-SPECIFIC CONSTANTS ONLY - NESTED CLASS STRUCTURE
    # =========================================================================

    class Connection:
        """Oracle WMS connection and API configuration constants."""

        DEFAULT_TIMEOUT = FlextConstants.Network.DEFAULT_TIMEOUT
        DEFAULT_MAX_RETRIES = FlextConstants.Reliability.MAX_RETRY_ATTEMPTS
        DEFAULT_RETRY_DELAY = FlextConstants.Reliability.DEFAULT_RETRY_DELAY_SECONDS

    class Entities:
        """Oracle WMS entity types and definitions."""

        TYPES: Final[FlextTypes.StringList] = [
            "INVENTORY",
            "SHIPMENT",
            "PICKING",
            "RECEIVING",
            "WAREHOUSE",
        ]

        MAX_ENTITY_NAME_LENGTH: Final[int] = 100
        ENTITY_NAME_PATTERN: Final[str] = r"^[a-zA-Z][a-zA-Z0-9_]*$"

    class Processing:
        """Oracle WMS data processing configuration constants."""

        DEFAULT_BATCH_SIZE = FlextConstants.Performance.BatchProcessing.DEFAULT_SIZE
        MAX_BATCH_SIZE = FlextConstants.Performance.BatchProcessing.MAX_ITEMS
        DEFAULT_PAGE_SIZE = FlextConstants.Performance.DEFAULT_PAGE_SIZE
        MAX_SCHEMA_DEPTH: Final[int] = 10

    class Filtering:
        """Oracle WMS filtering configuration constants."""

        MAX_FILTER_CONDITIONS: Final[int] = 50

    class ErrorMessages:
        """Oracle WMS error message constants."""

        ENTITY_VALIDATION_FAILED: Final[str] = "Entity validation failed"
        DISCOVERY_FAILED: Final[str] = "Entity discovery failed"
        INVALID_RESPONSE: Final[str] = "Invalid API response"

    class ResponseFields:
        """Oracle WMS API response field constants."""

        RESULT_COUNT: Final[str] = "result_count"
        RESULTS: Final[str] = "results"
        TOTAL_COUNT: Final[str] = "total_count"
        PAGE_NUMBER: Final[str] = "page_number"
        PAGE_COUNT: Final[str] = "page_count"
        NEXT_PAGE: Final[str] = "next_page"
        PREVIOUS_PAGE: Final[str] = "previous_page"

    class Authentication:
        """Oracle WMS authentication constants."""

        MIN_TOKEN_LENGTH: Final[int] = 10
        MIN_API_KEY_LENGTH: Final[int] = 20

    class Pagination:
        """Oracle WMS pagination constants."""

        DEFAULT_PAGE_SIZE: Final[int] = 100


# Export aliases for backward compatibility
FlextOracleWmsApiVersion = FlextOracleWmsConstants.OracleWMSApiVersion
FlextOracleWmsDefaults = FlextOracleWmsConstants
FlextOracleWmsSemanticConstants = FlextOracleWmsConstants
OracleWMSEntityType = FlextOracleWmsConstants.OracleWMSEntityType
OracleWMSFilterOperator = FlextOracleWmsConstants.OracleWMSFilterOperator
OracleWMSAuthMethod = FlextOracleWmsConstants.OracleWMSAuthMethod
OracleWMSPageMode = FlextOracleWmsConstants.OracleWMSPageMode
OracleWMSWriteMode = FlextOracleWmsConstants.OracleWMSWriteMode
OracleWMSAuthMethod = FlextOracleWmsConstants.OracleWMSAuthMethod
OracleWMSApiVersion = FlextOracleWmsConstants.OracleWMSApiVersion
OracleWMSDataQuality = FlextOracleWmsConstants.OracleWMSDataQuality
OracleWMSOperationStatus = FlextOracleWmsConstants.OracleWMSOperationStatus

__all__ = [
    "FlextOracleWmsApiVersion",
    "FlextOracleWmsConstants",
    "FlextOracleWmsDefaults",
    "FlextOracleWmsSemanticConstants",
    "OracleWMSApiVersion",
    "OracleWMSAuthMethod",
    "OracleWMSDataQuality",
    "OracleWMSEntityType",
    "OracleWMSFilterOperator",
    "OracleWMSOperationStatus",
]
