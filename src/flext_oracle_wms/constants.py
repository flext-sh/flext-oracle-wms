"""FLEXT WMS Constants - Generic WMS constants with patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Mapping,
)
from enum import StrEnum, unique
from types import MappingProxyType
from typing import TYPE_CHECKING, ClassVar, Final

from flext_api import c

if TYPE_CHECKING:
    from flext_oracle_wms import t


class FlextOracleWmsConstants(c):
    """Generic WMS constants class with composition patterns.

    Uses Python 3.13+ syntax, reduces declarations through patterns.
    One class per module following SOLID principles. Generic for any WMS system.
    """

    class OracleWms:
        """WMS connection constants - composed from base."""

        FLEXT_WMS_VERSION: Final[str] = "1.0.0"

        API_CONFIG: ClassVar[t.HeaderMapping] = MappingProxyType({
            "version_default": "v1",
            "base_url_default": "http://localhost:8080",
            "timeout_default": 30,
            "max_retries": 3,
        })

        PROCESSING_CONFIG: ClassVar[t.IntMapping] = MappingProxyType({
            "default_batch_size": c.DEFAULT_SIZE,
            "max_batch_size": c.MAX_ITEMS,
            "default_page_size": c.DEFAULT_PAGE_SIZE,
        })

        ENVIRONMENTS: ClassVar[t.StrMapping] = MappingProxyType({
            "default": "http://localhost:8080",
            "test": "https://test-wms.example.com",
            "production": "https://prod-wms.example.com",
        })

        DEFAULT_TIMEOUT: Final[int] = c.DEFAULT_TIMEOUT_SECONDS
        DEFAULT_MAX_RETRIES: Final[int] = c.MAX_RETRY_ATTEMPTS
        DEFAULT_RETRY_DELAY: Final[int] = c.DEFAULT_RETRY_DELAY_SECONDS
        MAX_POOL_SIZE: Final[int] = c.HTTP_STATUS_MIN

        @unique
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

        @unique
        class WmsApiVersion(StrEnum):
            """API versions.

            DRY Pattern: This StrEnum is the single source of truth for WMS API versions.
            All API version-related constants and Literal types MUST reference this enum.
            """

            V1 = "v1"
            V2 = "v2"
            V3 = "v3"
            LEGACY = "legacy"

        @unique
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

        @unique
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

        @unique
        class WmsDataQuality(StrEnum):
            """Data quality levels.

            DRY Pattern: This StrEnum is the single source of truth for WMS data quality levels.
            All data quality-related constants and Literal types MUST reference this enum.
            """

            HIGH = "high"
            MEDIUM = "medium"
            LOW = "low"
            UNKNOWN = "unknown"

        @unique
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

        @unique
        class WmsPageMode(StrEnum):
            """Page modes.

            DRY Pattern: This StrEnum is the single source of truth for WMS page modes.
            All page mode-related constants and Literal types MUST reference this enum.
            """

            APPEND = "append"
            REPLACE = "replace"
            MERGE = "merge"

        @unique
        class WmsWriteMode(StrEnum):
            """Write modes.

            DRY Pattern: This StrEnum is the single source of truth for WMS write modes.
            All write mode-related constants and Literal types MUST reference this enum.
            """

            INSERT = "insert"
            UPDATE = "update"
            UPSERT = "upsert"
            DELETE = "delete"

        @unique
        class EndpointDiscoveryStrategy(StrEnum):
            """Discovery strategy enum.

            DRY Pattern: This StrEnum is the single source of truth for discovery strategies.
            All discovery strategy-related constants and Literal types MUST reference this enum.
            """

            API_BASED = "api_based"
            SCHEMA_BASED = "schema_based"

        @unique
        class OracleWMSAuthMethod(StrEnum):
            """Auth methods.

            DRY Pattern: This StrEnum is the single source of truth for Oracle WMS authentication methods.
            All authentication method-related constants and Literal types MUST reference this enum.
            """

            BASIC = "basic"
            OAUTH2 = "oauth2"
            API_KEY = "api_key"
            BEARER = "bearer"

        AUTH_CONFIG: ClassVar[Mapping[str, str | OracleWMSAuthMethod]] = (
            MappingProxyType({
                "basic": OracleWMSAuthMethod.BASIC,
                "oauth2": OracleWMSAuthMethod.OAUTH2,
                "api_key": OracleWMSAuthMethod.API_KEY,
                "bearer": OracleWMSAuthMethod.BEARER,
                "oauth2_token_endpoint": "/oauth2/token",
                "oauth2_scope_default": "read write",
            })
        )

        @unique
        class ProjectType(StrEnum):
            """Project type literals for package metadata."""

            WMS_SERVICE = "wms-service"
            WAREHOUSE_MANAGEMENT = "warehouse-management"
            INVENTORY_SYSTEM = "inventory-system"
            SHIPPING_SERVICE = "shipping-service"
            PICKING_SYSTEM = "picking-system"
            WMS_INTEGRATION = "wms-integration"
            WAREHOUSE_API = "warehouse-api"
            LOGISTICS_PLATFORM = "logistics-platform"
            INVENTORY_TRACKER = "inventory-tracker"
            WAREHOUSE_MONITOR = "warehouse-monitor"
            WMS_CONNECTOR = "wms-connector"
            FULFILLMENT_ENGINE = "fulfillment-engine"
            WAREHOUSE_ANALYTICS = "warehouse-analytics"
            WMS_CLIENT = "wms-client"
            LOGISTICS_SERVICE = "logistics-service"
            WAREHOUSE_OPTIMIZER = "warehouse-optimizer"

        class WmsEntities:
            """WMS entity configuration - patterns."""

            MAX_ENTITY_NAME_LENGTH: ClassVar[int] = 100
            ENTITY_NAME_PATTERN: ClassVar[str] = "^[a-zA-Z][a-zA-Z0-9_]*$"
            TYPES: ClassVar[tuple[str, ...]]

        class WmsProcessing:
            """WMS processing constants - domain-specific."""

            DEFAULT_BATCH_SIZE: Final[int] = c.DEFAULT_SIZE
            MAX_BATCH_SIZE: Final[int] = c.MAX_ITEMS
            DEFAULT_PAGE_SIZE: Final[int] = c.DEFAULT_PAGE_SIZE
            MAX_SCHEMA_DEPTH: ClassVar[int] = 10

        class Filtering:
            """Filtering constants - minimal declaration."""

            MAX_FILTER_CONDITIONS: ClassVar[int] = 50

        class ErrorMessages:
            """Error messages - composed dict pattern."""

            MESSAGES: ClassVar[t.StrMapping] = MappingProxyType({
                "entity_validation_failed": "Entity validation failed",
                "discovery_failed": "Entity discovery failed",
                "invalid_response": "Invalid API response",
                "connection_failed": "Connection to WMS failed",
                "authentication_failed": "Authentication failed",
            })

        class ResponseFields:
            """Response fields - composed pattern."""

            FIELDS: ClassVar[t.StrMapping] = MappingProxyType({
                "result_count": "result_count",
                "results": "results",
                "data": "data",
                "total_count": "total_count",
                "page_number": "page_number",
                "page_count": "page_count",
                "next_page": "next_page",
                "previous_page": "previous_page",
            })

        class Authentication:
            """Auth constants - minimal."""

            MIN_TOKEN_LENGTH: ClassVar[int] = 10
            MIN_API_KEY_LENGTH: ClassVar[int] = 20

        class WmsPagination:
            """Pagination constants."""

            DEFAULT_PAGE_SIZE: ClassVar[int] = 100

            class Method:
                """HTTP method constants inherited from flext-api canonical API constants."""

                GET: Final[str] = c.Api.Method.GET
                POST: Final[str] = c.Api.Method.POST
                PUT: Final[str] = c.Api.Method.PUT
                DELETE: Final[str] = c.Api.Method.DELETE

            CONFIG: ClassVar[t.IntMapping] = MappingProxyType({
                "default_timeout": 60,
                "min_http_status_code": 200,
                "max_http_status_code": 599,
            })


c = FlextOracleWmsConstants

__all__: list[str] = ["FlextOracleWmsConstants", "c"]
