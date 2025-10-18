"""FLEXT Oracle WMS Constants - Single unified class with advanced patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from enum import StrEnum
from typing import ClassVar, Final

from flext_core import FlextConstants


class FlextOracleWmsConstants(FlextConstants):
    """Single unified Oracle WMS constants class with advanced composition patterns.

    Uses Python 3.13+ syntax, reduces declarations through advanced patterns.
    One class per module following SOLID principles.
    """

    # Core domain constants using advanced patterns
    FLEXT_ORACLE_WMS_VERSION: Final[str] = "0.9.0"

    # Application metadata - composed into single dict
    APP_METADATA: Final[dict[str, str]] = {
        "name": "flext-oracle-wms",
        "description": "FLEXT Oracle WMS Cloud Integration",
        "author": "FLEXT Team",
        "license": "MIT",
    }

    # API configuration - composed patterns
    API_CONFIG: Final[dict[str, str | int]] = {
        "version_default": "v2",
        "base_url_default": "https://wms.oraclecloud.com",
        "timeout_default": FlextConstants.Defaults.TIMEOUT * 2,
        "max_retries": 3,
        "rate_limit_per_minute": 1000,
    }

    # Authentication constants - advanced composition
    AUTH_CONFIG: Final[dict[str, str]] = {
        "basic": "basic",
        "oauth2": "oauth2",
        "api_key": "api_key",
        "oauth2_token_endpoint": "/oauth2/token",
        "oauth2_scope_default": "wms.read wms.write",
    }

    # Entity types - composed list with advanced patterns
    ENTITY_TYPES: Final[list[str]] = [
        "inventory",
        "order",
        "shipment",
        "picking",
        "location",
        "item",
    ]

    # Batch and performance - advanced dict composition
    PROCESSING_CONFIG: Final[dict[str, int]] = {
        "default_batch_size": FlextConstants.Defaults.PAGE_SIZE * 10,
        "max_batch_size": FlextConstants.Defaults.PAGE_SIZE * 100,
        "default_page_size": FlextConstants.Defaults.PAGE_SIZE,
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
    class Connection:
        """Oracle WMS connection constants - composed from base."""

        DEFAULT_TIMEOUT: Final[int] = FlextConstants.Network.DEFAULT_TIMEOUT
        DEFAULT_MAX_RETRIES: Final[int] = FlextConstants.Reliability.MAX_RETRY_ATTEMPTS
        DEFAULT_RETRY_DELAY: Final[int] = (
            FlextConstants.Reliability.DEFAULT_RETRY_DELAY_SECONDS
        )
        DEFAULT_POOL_SIZE: Final[int] = (
            FlextConstants.Network.DEFAULT_CONNECTION_POOL_SIZE
        )
        MAX_POOL_SIZE: Final[int] = FlextConstants.Network.MAX_CONNECTION_POOL_SIZE

    class WmsEntities:
        """Oracle WMS entity configuration - advanced patterns."""

        TYPES: ClassVar[list[str]] = [
            "INVENTORY",
            "SHIPMENT",
            "PICKING",
            "RECEIVING",
            "WAREHOUSE",
        ]
        MAX_ENTITY_NAME_LENGTH: ClassVar[int] = 100
        ENTITY_NAME_PATTERN: ClassVar[str] = r"^[a-zA-Z][a-zA-Z0-9_]*$"

    class WmsProcessing:
        """WMS processing constants - domain-specific."""

        DEFAULT_BATCH_SIZE: Final[int] = (
            FlextConstants.Performance.BatchProcessing.DEFAULT_SIZE
        )
        MAX_BATCH_SIZE: Final[int] = (
            FlextConstants.Performance.BatchProcessing.MAX_ITEMS
        )
        DEFAULT_PAGE_SIZE: Final[int] = FlextConstants.Pagination.DEFAULT_PAGE_SIZE
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
        }

    class ResponseFields:
        """Response fields - composed pattern."""

        FIELDS: ClassVar[dict[str, str]] = {
            "result_count": "result_count",
            "results": "results",
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
    class OracleWMSEntityType(StrEnum):
        """Entity types - composed from list."""

        INVENTORY = "inventory"
        ORDER = "order"
        SHIPMENT = "shipment"
        PICKING = "picking"
        LOCATION = "location"
        ITEM = "item"

    class OracleWMSApiVersion(StrEnum):
        """API versions."""

        V1 = "v1"
        V2 = "v2"
        LGF_V10 = "v10"
        LEGACY = "legacy"

    class OracleWMSApiCategory(StrEnum):
        """API categories."""

        SETUP_TRANSACTIONAL = "setup_transactional"
        AUTOMATION_OPERATIONS = "automation_operations"
        DATA_EXTRACT = "data_extract"
        ENTITY_OPERATIONS = "entity_operations"

    class OracleWMSOperationStatus(StrEnum):
        """Operation status - advanced patterns."""

        PENDING = "pending"
        RUNNING = "running"
        SUCCESS = "success"
        ERROR = "error"
        TIMEOUT = "timeout"
        CANCELLED = "cancelled"

    class OracleWMSDataQuality(StrEnum):
        """Data quality levels."""

        HIGH = "high"
        MEDIUM = "medium"
        LOW = "low"
        UNKNOWN = "unknown"

    class OracleWMSFilterOperator(StrEnum):
        """Filter operators - composed."""

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
        """Page modes."""

        APPEND = "append"
        REPLACE = "replace"
        MERGE = "merge"

    class OracleWMSWriteMode(StrEnum):
        """Write modes."""

        INSERT = "insert"
        UPDATE = "update"
        UPSERT = "upsert"
        DELETE = "delete"


# Module-level enums for direct import - advanced composition
class OracleWMSAuthMethod(StrEnum):
    """Auth methods - composed from dict."""

    BASIC = "basic"
    OAUTH2 = "oauth2"
    API_KEY = "api_key"
    BEARER = "bearer"


class OracleWMSFilterOperator(StrEnum):
    """Filter operators - alias to nested."""

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


# Backward compatibility aliases - advanced pattern
FlextOracleWmsApiVersion = FlextOracleWmsConstants.OracleWMSApiVersion
FlextOracleWmsApiCategory = FlextOracleWmsConstants.OracleWMSApiCategory

__all__ = [
    "FlextOracleWmsApiCategory",
    "FlextOracleWmsApiVersion",
    "FlextOracleWmsConstants",
    "OracleWMSAuthMethod",
    "OracleWMSFilterOperator",
]
