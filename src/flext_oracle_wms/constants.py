"""FLEXT WMS Constants - Generic WMS constants with patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from enum import StrEnum, unique
from types import MappingProxyType
from typing import TYPE_CHECKING, ClassVar, Final

from flext_api import c

if TYPE_CHECKING:
    from collections.abc import (
        Mapping,
    )

    from flext_oracle_wms import t


class FlextOracleWmsConstants(c):
    """Generic WMS constants class with composition patterns.

    Uses Python 3.13+ syntax, reduces declarations through patterns.
    One class per module following SOLID principles. Generic for any WMS system.
    """

    class OracleWms:
        """WMS connection constants - composed from base."""

        FLEXT_WMS_VERSION: Final[str] = "1.0.0"
        HTTP_BAD_REQUEST_THRESHOLD: Final[int] = 400
        API_ENDPOINTS: ClassVar[t.MappingKV[str, t.StrMapping]] = MappingProxyType({
            "test": {
                "name": "test",
                "method": "GET",
                "path": "/test/",
                "version": "v1",
                "category": "test",
                "description": "Test endpoint",
                "since_version": "6.1",
            },
        })

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
        DISCOVERY_SUCCESS: Final[str] = "discovery_success"
        DISCOVERY_FAILURE: Final[str] = "discovery_failure"

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

        @unique
        class Environment(StrEnum):
            """Oracle WMS deployment environments."""

            DEVELOPMENT = "dev"
            STAGING = "staging"
            PRODUCTION = "prod"

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

        class WmsEntities:
            """WMS entity configuration - patterns."""

            MAX_ENTITY_NAME_LENGTH: ClassVar[int] = 100

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


c = FlextOracleWmsConstants

__all__: t.StrSequence = ("FlextOracleWmsConstants", "c")
