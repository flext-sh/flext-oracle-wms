"""Oracle WMS Constants - Consolidated Constants and Enums.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Consolidated constants extending flext-core platform constants.
This module consolidates all Oracle WMS-specific constants, enums, and default values.
"""

from __future__ import annotations

from enum import StrEnum
from typing import ClassVar, Literal

from flext_core import FlextConstants

"""Constants and enums for Oracle WMS module.

Note: `FlextOracleWmsApiVersion` lives here to avoid circular imports
between `wms_constants` and `wms_models`.
"""

# =============================================================================
# ORACLE WMS-SPECIFIC SEMANTIC CONSTANTS - Modern Python 3.13 Structure
# =============================================================================


class FlextOracleWmsSemanticConstants(FlextConstants):
    """Oracle WMS semantic constants extending FlextConstants.

    Modern Python 3.13 constants following semantic grouping patterns.
    Extends the FLEXT ecosystem constants with Oracle WMS-specific
    values while maintaining full backward compatibility.
    """

    class Core:
        """Core Oracle WMS system constants."""

        NAME = "flext-oracle-wms"
        VERSION = "0.9.0"
        ECOSYSTEM_SIZE = 33
        DEFAULT_ENVIRONMENT = "default"

    class Api:
        """API configuration constants."""

        # API versions
        VERSIONS: ClassVar[list[str]] = ["v10", "v9", "v8"]
        DEFAULT_VERSION: Literal["v10"] = "v10"

        # Base paths
        LGF_API_BASE = "/wms/lgfapi"

        # Timeouts and limits
        DEFAULT_TIMEOUT = 30.0
        DEFAULT_MAX_RETRIES = 3
        DEFAULT_RETRY_DELAY = 1.0

        # HTTP status codes
        HTTP_OK = 200
        HTTP_BAD_REQUEST = 400
        HTTP_UNAUTHORIZED = 401
        HTTP_FORBIDDEN = 403
        MIN_HTTP_STATUS_CODE = 100
        MAX_HTTP_STATUS_CODE = 599

        AUTH_ERROR_CODES: ClassVar[tuple[int, ...]] = (401, 403)

    class Authentication:
        """Authentication configuration constants."""

        METHODS: ClassVar[list[str]] = ["basic", "bearer", "api_key"]
        MIN_TOKEN_LENGTH = 10
        MIN_API_KEY_LENGTH = 10

    class Entities:
        """Oracle WMS entity type constants."""

        CORE_ENTITIES: ClassVar[list[str]] = [
            "company",
            "facility",
            "location",
            "item",
        ]

        ORDER_ENTITIES: ClassVar[list[str]] = [
            "order_hdr",
            "order_dtl",
        ]

        INVENTORY_ENTITIES: ClassVar[list[str]] = [
            "inventory",
            "allocation",
        ]

        MOVEMENT_ENTITIES: ClassVar[list[str]] = [
            "pick_hdr",
            "pick_dtl",
        ]

        SHIPMENT_ENTITIES: ClassVar[list[str]] = [
            "shipment",
            "oblpn",
        ]

        # Entity validation
        MAX_ENTITY_NAME_LENGTH = 100
        ENTITY_NAME_PATTERN = r"^[a-z0-9_]+$"

    class Filtering:
        """Data filtering constants."""

        OPERATORS: ClassVar[list[str]] = [
            "eq",
            "ne",
            "gt",
            "ge",
            "lt",
            "le",
            "in",
            "not_in",
            "like",
            "not_like",
        ]

        MAX_FILTER_CONDITIONS = 50

    class Pagination:
        """Pagination configuration constants."""

        MODES: ClassVar[list[str]] = ["offset", "cursor", "token"]
        DEFAULT_PAGE_SIZE = 100
        MAX_PAGE_SIZE = 1000
        MIN_PAGE_SIZE = 1

    class Processing:
        """Data processing configuration constants."""

        WRITE_MODES: ClassVar[list[str]] = ["insert", "update", "upsert", "delete"]
        DEFAULT_BATCH_SIZE = 50
        MAX_BATCH_SIZE = 500

        # Rate limiting
        DEFAULT_RATE_LIMIT = 60  # requests per minute
        MIN_REQUEST_DELAY = 0.1  # seconds

        # Schema discovery
        DEFAULT_SAMPLE_SIZE = 100
        MIN_CONFIDENCE_THRESHOLD = 0.7
        MAX_SCHEMA_DEPTH = 10

    class Connections:
        """Connection management constants."""

        DEFAULT_POOL_SIZE = 5
        MAX_POOL_SIZE = 20
        DEFAULT_CONNECT_TIMEOUT = 10
        DEFAULT_READ_TIMEOUT = 30

    class Caching:
        """Caching configuration constants."""

        DEFAULT_CACHE_TTL = 300  # 5 minutes
        MAX_CACHE_SIZE = 1000

    class Paths:
        """API path constants."""

        # Entity paths
        ENTITY_DISCOVERY = "/entity/"
        ENTITY_DATA = "/entity/{entity_name}/"
        ENTITY_BY_ID = "/entity/{entity_name}/{entity_id}/"

        # Metadata paths
        METADATA_BASE = "/metadata"
        SCHEMA_BASE = "/schema"

        # Operation paths
        INIT_STAGE = "/init_stage_interface/"
        RUN_STAGE = "/run_stage_interface/"

        # Status paths
        STATUS_CHECK = "/status/"
        HEALTH_CHECK = "/health/"

    class ResponseFields:
        """Standard response field names."""

        # Pagination fields
        RESULT_COUNT = "result_count"
        PAGE_COUNT = "page_count"
        PAGE_NUMBER = "page_nbr"
        NEXT_PAGE = "next_page"
        PREVIOUS_PAGE = "previous_page"
        RESULTS = "results"

        # Data fields
        DATA = "data"
        ID = "id"
        URL = "url"

        # Metadata fields
        CREATE_USER = "create_user"
        CREATE_TS = "create_ts"
        MOD_USER = "mod_user"
        MOD_TS = "mod_ts"

        # Status fields
        STATUS = "status"
        MESSAGE = "message"
        ERROR = "error"

    class ErrorMessages:
        """Standard error messages for Oracle WMS operations."""

        # Connection errors
        CONNECTION_FAILED = "Failed to connect to Oracle WMS"
        AUTHENTICATION_FAILED = "Authentication failed"
        TIMEOUT_ERROR = "Request timeout"

        # API errors
        API_ERROR = "Oracle WMS API error"
        INVALID_ENDPOINT = "Invalid API endpoint"
        INVALID_RESPONSE = "Invalid API response format"

        # Entity errors
        ENTITY_NOT_FOUND = "Entity not found"
        INVALID_ENTITY_TYPE = "Invalid entity type"
        ENTITY_VALIDATION_FAILED = "Entity validation failed"

        # Data errors
        INVALID_DATA_FORMAT = "Invalid data format"
        DATA_VALIDATION_FAILED = "Data validation failed"
        SCHEMA_GENERATION_FAILED = "Schema generation failed"

        # Processing errors
        FLATTENING_FAILED = "Data flattening failed"
        DISCOVERY_FAILED = "Entity discovery failed"
        PROCESSING_FAILED = "Data processing failed"


class FlextOracleWmsConstants(FlextOracleWmsSemanticConstants):
    """Oracle WMS constants with backward compatibility.

    Legacy compatibility layer providing both modern semantic access
    and traditional flat constant access patterns for smooth migration.
    """

    # Modern semantic access (Primary API) - direct references
    Core = FlextOracleWmsSemanticConstants.Core
    Api = FlextOracleWmsSemanticConstants.Api
    Authentication = FlextOracleWmsSemanticConstants.Authentication
    Entities = FlextOracleWmsSemanticConstants.Entities
    Filtering = FlextOracleWmsSemanticConstants.Filtering
    Pagination = FlextOracleWmsSemanticConstants.Pagination
    Processing = FlextOracleWmsSemanticConstants.Processing
    Connections = FlextOracleWmsSemanticConstants.Connections
    Caching = FlextOracleWmsSemanticConstants.Caching
    Paths = FlextOracleWmsSemanticConstants.Paths
    ResponseFields = FlextOracleWmsSemanticConstants.ResponseFields
    ErrorMessages = FlextOracleWmsSemanticConstants.ErrorMessages


# =================================================================
# ENUM CLASSES - Core Oracle WMS Enums
# =================================================================


class OracleWMSAuthMethod(StrEnum):
    """Oracle WMS authentication methods."""

    BASIC = "basic"
    BEARER = "bearer"
    API_KEY = "api_key"


class FlextOracleWmsApiVersion(StrEnum):
    """Oracle WMS API versions."""

    LEGACY = "legacy"  # /wms/api/
    LGF_V10 = "v10"  # /wms/lgfapi/v10/


class OracleWMSEntityType(StrEnum):
    """Oracle WMS entity types."""

    # Core entities
    COMPANY = "company"
    FACILITY = "facility"
    LOCATION = "location"
    ITEM = "item"

    # Order entities
    ORDER_HDR = "order_hdr"
    ORDER_DTL = "order_dtl"

    # Inventory entities
    INVENTORY = "inventory"
    ALLOCATION = "allocation"

    # Movement entities
    PICK_HDR = "pick_hdr"
    PICK_DTL = "pick_dtl"

    # Shipment entities
    SHIPMENT = "shipment"
    OBLPN = "oblpn"


class OracleWMSFilterOperator(StrEnum):
    """Oracle WMS filter operators."""

    EQ = "eq"
    NE = "ne"
    GT = "gt"
    GE = "ge"
    LT = "lt"
    LE = "le"
    IN = "in"
    NOT_IN = "not_in"
    LIKE = "like"
    NOT_LIKE = "not_like"


class OracleWMSPageMode(StrEnum):
    """Oracle WMS pagination modes."""

    OFFSET = "offset"
    CURSOR = "cursor"
    TOKEN = "token"


class OracleWMSWriteMode(StrEnum):
    """Oracle WMS write modes."""

    INSERT = "insert"
    UPDATE = "update"
    UPSERT = "upsert"
    DELETE = "delete"


# =============================================================================
# LEGACY COMPATIBILITY CLASSES
# =============================================================================


class FlextOracleWmsDefaults:
    """Default values for Oracle WMS operations (DEPRECATED - use FlextOracleWmsConstants)."""

    # API Configuration
    DEFAULT_API_VERSION = FlextOracleWmsSemanticConstants.Api.DEFAULT_VERSION
    DEFAULT_TIMEOUT = FlextOracleWmsSemanticConstants.Api.DEFAULT_TIMEOUT
    DEFAULT_MAX_RETRIES = FlextOracleWmsSemanticConstants.Api.DEFAULT_MAX_RETRIES
    DEFAULT_RETRY_DELAY = FlextOracleWmsSemanticConstants.Api.DEFAULT_RETRY_DELAY

    # Authentication
    MIN_TOKEN_LENGTH = FlextOracleWmsSemanticConstants.Authentication.MIN_TOKEN_LENGTH
    MIN_API_KEY_LENGTH = (
        FlextOracleWmsSemanticConstants.Authentication.MIN_API_KEY_LENGTH
    )

    # Pagination
    DEFAULT_PAGE_SIZE = FlextOracleWmsSemanticConstants.Pagination.DEFAULT_PAGE_SIZE
    MAX_PAGE_SIZE = FlextOracleWmsSemanticConstants.Pagination.MAX_PAGE_SIZE
    MIN_PAGE_SIZE = FlextOracleWmsSemanticConstants.Pagination.MIN_PAGE_SIZE

    # Batch Processing
    DEFAULT_BATCH_SIZE = FlextOracleWmsSemanticConstants.Processing.DEFAULT_BATCH_SIZE
    MAX_BATCH_SIZE = FlextOracleWmsSemanticConstants.Processing.MAX_BATCH_SIZE

    # Rate Limiting
    DEFAULT_RATE_LIMIT = FlextOracleWmsSemanticConstants.Processing.DEFAULT_RATE_LIMIT
    MIN_REQUEST_DELAY = FlextOracleWmsSemanticConstants.Processing.MIN_REQUEST_DELAY

    # Schema Discovery
    DEFAULT_SAMPLE_SIZE = FlextOracleWmsSemanticConstants.Processing.DEFAULT_SAMPLE_SIZE
    MIN_CONFIDENCE_THRESHOLD = (
        FlextOracleWmsSemanticConstants.Processing.MIN_CONFIDENCE_THRESHOLD
    )
    MAX_SCHEMA_DEPTH = FlextOracleWmsSemanticConstants.Processing.MAX_SCHEMA_DEPTH

    # Connections
    DEFAULT_POOL_SIZE = FlextOracleWmsSemanticConstants.Connections.DEFAULT_POOL_SIZE
    MAX_POOL_SIZE = FlextOracleWmsSemanticConstants.Connections.MAX_POOL_SIZE
    DEFAULT_CONNECT_TIMEOUT = (
        FlextOracleWmsSemanticConstants.Connections.DEFAULT_CONNECT_TIMEOUT
    )
    DEFAULT_READ_TIMEOUT = (
        FlextOracleWmsSemanticConstants.Connections.DEFAULT_READ_TIMEOUT
    )

    # Caching
    DEFAULT_CACHE_TTL = FlextOracleWmsSemanticConstants.Caching.DEFAULT_CACHE_TTL
    MAX_CACHE_SIZE = FlextOracleWmsSemanticConstants.Caching.MAX_CACHE_SIZE

    # Entity Validation
    MAX_ENTITY_NAME_LENGTH = (
        FlextOracleWmsSemanticConstants.Entities.MAX_ENTITY_NAME_LENGTH
    )
    ENTITY_NAME_PATTERN = FlextOracleWmsSemanticConstants.Entities.ENTITY_NAME_PATTERN

    # Filter Limits
    MAX_FILTER_CONDITIONS = (
        FlextOracleWmsSemanticConstants.Filtering.MAX_FILTER_CONDITIONS
    )

    # HTTP status codes
    HTTP_OK = FlextOracleWmsSemanticConstants.Api.HTTP_OK
    HTTP_BAD_REQUEST = FlextOracleWmsSemanticConstants.Api.HTTP_BAD_REQUEST
    HTTP_UNAUTHORIZED = FlextOracleWmsSemanticConstants.Api.HTTP_UNAUTHORIZED
    HTTP_FORBIDDEN = FlextOracleWmsSemanticConstants.Api.HTTP_FORBIDDEN
    MIN_HTTP_STATUS_CODE = FlextOracleWmsSemanticConstants.Api.MIN_HTTP_STATUS_CODE
    MAX_HTTP_STATUS_CODE = FlextOracleWmsSemanticConstants.Api.MAX_HTTP_STATUS_CODE

    # Core constants
    DEFAULT_ENVIRONMENT = FlextOracleWmsSemanticConstants.Core.DEFAULT_ENVIRONMENT

    # Authentication status codes
    AUTH_ERROR_CODES = FlextOracleWmsSemanticConstants.Api.AUTH_ERROR_CODES


# Legacy class aliases for backward compatibility
FlextOracleWmsErrorMessages = FlextOracleWmsSemanticConstants.ErrorMessages
FlextOracleWmsApiPaths = FlextOracleWmsSemanticConstants.Paths
FlextOracleWmsResponseFields = FlextOracleWmsSemanticConstants.ResponseFields


# =============================================================================
# EXPORTS
# =============================================================================

__all__: list[str] = [
    "FlextOracleWmsApiPaths",
    "FlextOracleWmsApiVersion",
    "FlextOracleWmsConstants",
    # Legacy Compatibility
    "FlextOracleWmsDefaults",
    "FlextOracleWmsErrorMessages",
    "FlextOracleWmsResponseFields",
    # Modern Semantic Constants (Primary API)
    "FlextOracleWmsSemanticConstants",
    # Enum Classes
    "OracleWMSAuthMethod",
    "OracleWMSEntityType",
    "OracleWMSFilterOperator",
    "OracleWMSPageMode",
    "OracleWMSWriteMode",
]
