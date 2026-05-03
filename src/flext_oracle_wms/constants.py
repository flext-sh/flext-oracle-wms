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

        class WmsProcessing:
            """WMS processing constants - domain-specific."""

            DEFAULT_BATCH_SIZE: Final[int] = c.DEFAULT_SIZE
            MAX_BATCH_SIZE: Final[int] = c.MAX_ITEMS
            DEFAULT_PAGE_SIZE: Final[int] = c.DEFAULT_PAGE_SIZE
            MAX_SCHEMA_DEPTH: ClassVar[int] = 10

        class Filtering:
            """Filtering constants - minimal declaration."""

            MAX_FILTER_CONDITIONS: ClassVar[int] = 50

        class Authentication:
            """Auth constants - minimal."""

            MIN_TOKEN_LENGTH: ClassVar[int] = 10
            MIN_API_KEY_LENGTH: ClassVar[int] = 20


c = FlextOracleWmsConstants

__all__: tuple[str, ...] = ("FlextOracleWmsConstants", "c")
