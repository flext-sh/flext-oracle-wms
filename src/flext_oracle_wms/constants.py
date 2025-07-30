"""Oracle WMS Constants using flext-core patterns.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Essential constants for Oracle WMS operations.
"""

from __future__ import annotations

from enum import StrEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flext_oracle_wms.types import TOracleWmsApiVersion

# =================================================================
# API CONSTANTS
# =================================================================


class OracleWMSAuthMethod(StrEnum):
    """Oracle WMS authentication methods."""

    BASIC = "basic"
    BEARER = "bearer"
    API_KEY = "api_key"


class FlextOracleWmsApiVersion(StrEnum):
    """Oracle WMS API versions."""

    LGF_V10 = "v10"
    LGF_V9 = "v9"
    LGF_V8 = "v8"


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
    TOKEN = "token"  # noqa: S105


class OracleWMSWriteMode(StrEnum):
    """Oracle WMS write modes."""

    INSERT = "insert"
    UPDATE = "update"
    UPSERT = "upsert"
    DELETE = "delete"


# =================================================================
# DEFAULT VALUES
# =================================================================


class FlextOracleWmsDefaults:
    """Default values for Oracle WMS operations."""

    # API Configuration
    DEFAULT_API_VERSION: TOracleWmsApiVersion = "v10"
    DEFAULT_TIMEOUT = 30.0
    DEFAULT_MAX_RETRIES = 3
    DEFAULT_RETRY_DELAY = 1.0

    # Authentication
    MIN_TOKEN_LENGTH = 10
    MIN_API_KEY_LENGTH = 10

    # Pagination
    DEFAULT_PAGE_SIZE = 100
    MAX_PAGE_SIZE = 1000
    MIN_PAGE_SIZE = 1

    # Batch Processing
    DEFAULT_BATCH_SIZE = 50
    MAX_BATCH_SIZE = 500

    # Rate Limiting
    DEFAULT_RATE_LIMIT = 60  # requests per minute
    MIN_REQUEST_DELAY = 0.1  # seconds

    # Schema Discovery
    DEFAULT_SAMPLE_SIZE = 100
    MIN_CONFIDENCE_THRESHOLD = 0.7
    MAX_SCHEMA_DEPTH = 10

    # Connections
    DEFAULT_POOL_SIZE = 5
    MAX_POOL_SIZE = 20

    # Caching
    DEFAULT_CACHE_TTL = 300  # 5 minutes
    MAX_CACHE_SIZE = 1000

    # Timeouts
    DEFAULT_CONNECT_TIMEOUT = 10
    DEFAULT_READ_TIMEOUT = 30

    # Environment Configuration
    DEFAULT_ENVIRONMENT = "default"

    # Entity Validation
    MAX_ENTITY_NAME_LENGTH = 100
    ENTITY_NAME_PATTERN = r"^[a-z0-9_]+$"

    # Filter Limits
    MAX_FILTER_CONDITIONS = 50

    # HTTP Status Code Limits
    MIN_HTTP_STATUS_CODE = 100
    MAX_HTTP_STATUS_CODE = 599

    # HTTP status codes
    HTTP_OK = 200
    HTTP_BAD_REQUEST = 400
    HTTP_UNAUTHORIZED = 401
    HTTP_FORBIDDEN = 403

    # Authentication status codes
    AUTH_ERROR_CODES = (HTTP_UNAUTHORIZED, HTTP_FORBIDDEN)


# =================================================================
# ERROR MESSAGES
# =================================================================


class FlextOracleWmsErrorMessages:
    """Standard error messages for Oracle WMS operations."""

    # Connection Errors
    CONNECTION_FAILED = "Failed to connect to Oracle WMS"
    AUTHENTICATION_FAILED = "Authentication failed"
    TIMEOUT_ERROR = "Request timeout"

    # API Errors
    API_ERROR = "Oracle WMS API error"
    INVALID_ENDPOINT = "Invalid API endpoint"
    INVALID_RESPONSE = "Invalid API response format"

    # Entity Errors
    ENTITY_NOT_FOUND = "Entity not found"
    INVALID_ENTITY_TYPE = "Invalid entity type"
    ENTITY_VALIDATION_FAILED = "Entity validation failed"

    # Data Errors
    INVALID_DATA_FORMAT = "Invalid data format"
    DATA_VALIDATION_FAILED = "Data validation failed"
    SCHEMA_GENERATION_FAILED = "Schema generation failed"

    # Processing Errors
    FLATTENING_FAILED = "Data flattening failed"
    DISCOVERY_FAILED = "Entity discovery failed"
    PROCESSING_FAILED = "Data processing failed"


# =================================================================
# API PATHS
# =================================================================


class FlextOracleWmsApiPaths:
    """Standard API paths for Oracle WMS."""

    # Base paths
    LGF_API_BASE = "/wms/lgfapi"

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


# =================================================================
# RESPONSE FORMATS
# =================================================================


class FlextOracleWmsResponseFields:
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
