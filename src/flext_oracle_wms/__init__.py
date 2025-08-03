"""Oracle WMS Library - Enterprise integration using flext-core and flext-api patterns.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Complete Oracle WMS integration library with maximum flext-core/flext-api reuse.
"""

# Core client - the main thing users need
# API Catalog - declarative APIs
from flext_oracle_wms.api_catalog import (
    FLEXT_ORACLE_WMS_APIS,
    FlextOracleWmsApiCategory,
    FlextOracleWmsApiEndpoint,
)

# Authentication - enterprise auth patterns using flext-api
from flext_oracle_wms.authentication import (
    FlextOracleWmsAuthConfig,
    FlextOracleWmsAuthenticator,
    FlextOracleWmsAuthPlugin,
)

# Cache - enterprise caching using flext-core patterns
from flext_oracle_wms.cache import (
    FlextOracleWmsCacheConfig,
    FlextOracleWmsCacheManager,
)
from flext_oracle_wms.client import (
    FlextOracleWmsClient,
    FlextOracleWmsClientMock,
    create_oracle_wms_client,
)

# Configuration - essential for setup
from flext_oracle_wms.config import (
    FlextOracleWmsClientConfig,
    FlextOracleWmsModuleConfig,
)

# Constants - enums and defaults
from flext_oracle_wms.constants import (
    FlextOracleWmsApiPaths,
    FlextOracleWmsDefaults,
    FlextOracleWmsErrorMessages,
    FlextOracleWmsResponseFields,
    OracleWMSAuthMethod,
    OracleWMSEntityType,
    OracleWMSFilterOperator,
    OracleWMSPageMode,
    OracleWMSWriteMode,
)

# Discovery - entity discovery using flext-api
from flext_oracle_wms.discovery import (
    FlextOracleWmsEntityDiscovery,
    flext_oracle_wms_create_entity_discovery,
)

# Dynamic processing - schema discovery and processing
from flext_oracle_wms.dynamic import (
    FlextOracleWmsDynamicSchemaProcessor,
    flext_oracle_wms_create_dynamic_schema_processor,
)

# Exceptions - comprehensive error handling
from flext_oracle_wms.exceptions import (
    FlextOracleWmsApiError,
    FlextOracleWmsAuthenticationError,
    FlextOracleWmsConnectionError,
    FlextOracleWmsDataValidationError,
    FlextOracleWmsEntityNotFoundError,
    FlextOracleWmsError,
    FlextOracleWmsSchemaError,
    FlextOracleWmsSchemaFlatteningError,
)

# Filtering - advanced record filtering
from flext_oracle_wms.filtering import (
    FlextOracleWmsFilter,
    flext_oracle_wms_create_filter,
    flext_oracle_wms_filter_by_field,
    flext_oracle_wms_filter_by_id_range,
)

# Data flattening - nested data handling (imported selectively as needed)
# Helper functions - utility functions
from flext_oracle_wms.helpers import (
    flext_oracle_wms_build_entity_url,
    flext_oracle_wms_chunk_records,
    flext_oracle_wms_extract_environment_from_url,
    flext_oracle_wms_extract_pagination_info,
    flext_oracle_wms_format_timestamp,
    flext_oracle_wms_normalize_url,
    flext_oracle_wms_validate_api_response,
    flext_oracle_wms_validate_entity_name,
)

# Models - using FlextValueObject
from flext_oracle_wms.models import (
    FlextOracleWmsApiResponse,
    FlextOracleWmsDiscoveryResult,
    FlextOracleWmsEntity,
)

# Types - standardized type definitions
from flext_oracle_wms.types import (
    TOracleWmsApiResponse,
    TOracleWmsApiVersion,
    TOracleWmsDiscoveryResult,
    TOracleWmsEntityId,
    TOracleWmsEntityInfo,
    TOracleWmsEntityName,
    TOracleWmsEnvironment,
    TOracleWmsFilters,
    TOracleWmsFilterValue,
    TOracleWmsPaginationInfo,
    TOracleWmsRecord,
    TOracleWmsRecordBatch,
    TOracleWmsSchema,
    TOracleWmsTimeout,
)

# Version information
__version__ = "0.9.0"
__author__ = "FLEXT Contributors"
__description__ = (
    "Oracle WMS integration library using flext-core and flext-api patterns"
)

# Public API - explicitly defined for clarity
__all__ = [
    # API Catalog
    "FLEXT_ORACLE_WMS_APIS",
    "FlextOracleWmsApiCategory",
    "FlextOracleWmsApiEndpoint",
    # Exceptions
    "FlextOracleWmsApiError",
    # Constants
    "FlextOracleWmsApiPaths",
    # Models
    "FlextOracleWmsApiResponse",
    # Authentication
    "FlextOracleWmsAuthConfig",
    "FlextOracleWmsAuthPlugin",
    "FlextOracleWmsAuthenticationError",
    "FlextOracleWmsAuthenticator",
    # Cache
    "FlextOracleWmsCacheConfig",
    "FlextOracleWmsCacheManager",
    # Core client
    "FlextOracleWmsClient",
    # Configuration
    "FlextOracleWmsClientConfig",
    "FlextOracleWmsClientMock",
    "FlextOracleWmsConnectionError",
    # Data flattening (imported selectively as needed)
    "FlextOracleWmsDataValidationError",
    "FlextOracleWmsDefaults",
    "FlextOracleWmsDiscoveryResult",
    # Dynamic processing
    "FlextOracleWmsDynamicSchemaProcessor",
    "FlextOracleWmsEntity",
    # Discovery
    "FlextOracleWmsEntityDiscovery",
    "FlextOracleWmsEntityNotFoundError",
    "FlextOracleWmsError",
    "FlextOracleWmsErrorMessages",
    # Filtering
    "FlextOracleWmsFilter",
    "FlextOracleWmsModuleConfig",
    "FlextOracleWmsResponseFields",
    "FlextOracleWmsSchemaError",
    "FlextOracleWmsSchemaFlatteningError",
    "OracleWMSAuthMethod",
    "OracleWMSEntityType",
    "OracleWMSFilterOperator",
    "OracleWMSPageMode",
    "OracleWMSWriteMode",
    # Essential Types
    "TOracleWmsApiResponse",
    "TOracleWmsApiVersion",
    "TOracleWmsDiscoveryResult",
    "TOracleWmsEntityId",
    "TOracleWmsEntityInfo",
    "TOracleWmsEntityName",
    "TOracleWmsEnvironment",
    "TOracleWmsFilterValue",
    "TOracleWmsFilters",
    "TOracleWmsPaginationInfo",
    "TOracleWmsRecord",
    "TOracleWmsRecordBatch",
    "TOracleWmsSchema",
    "TOracleWmsTimeout",
    "__author__",
    "__description__",
    # Metadata
    "__version__",
    "create_oracle_wms_client",
    # Helper functions
    "flext_oracle_wms_build_entity_url",
    "flext_oracle_wms_chunk_records",
    "flext_oracle_wms_create_api_key_auth",
    "flext_oracle_wms_create_basic_auth",
    "flext_oracle_wms_create_bearer_auth",
    "flext_oracle_wms_create_cache_manager",
    "flext_oracle_wms_create_dynamic_schema_processor",
    "flext_oracle_wms_create_entity_discovery",
    "flext_oracle_wms_create_filter",
    "flext_oracle_wms_extract_environment_from_url",
    "flext_oracle_wms_extract_pagination_info",
    "flext_oracle_wms_filter_by_field",
    "flext_oracle_wms_filter_by_id_range",
    "flext_oracle_wms_format_timestamp",
    "flext_oracle_wms_normalize_url",
    "flext_oracle_wms_validate_api_response",
    "flext_oracle_wms_validate_entity_name",
]
