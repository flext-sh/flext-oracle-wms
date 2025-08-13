"""FLEXT Oracle WMS - Enterprise Oracle WMS Cloud Integration Library.

This module provides enterprise-grade Oracle Warehouse Management System (WMS) Cloud
integration for the FLEXT data integration platform. It implements type-safe, async
REST API connectivity with comprehensive entity discovery, schema processing, and
data operations support.

Key Components:
    - FlextOracleWmsClient: Main client interface for Oracle WMS operations
    - FlextOracleWmsClientConfig: Type-safe configuration management
    - Authentication: Multi-method auth (Basic, Bearer, API Key) with enterprise SSO
    - Entity Discovery: Automatic discovery of WMS entities and schemas
    - Data Processing: Dynamic schema processing and data transformation
    - Error Handling: Comprehensive exception hierarchy with structured errors

Architecture:
    Built on FLEXT ecosystem foundation libraries (flext-core, flext-api,
    flext-observability) following Clean Architecture principles with proper
    separation of concerns and railway-oriented programming patterns.

Integration:
    - FlextResult pattern for consistent error handling
    - FLEXT dependency injection container support
    - Structured logging with correlation IDs
    - Enterprise caching and performance optimization
    - Singer protocol support for data pipeline integration

Example:
    Basic Oracle WMS client setup and entity discovery:

    >>> from flext_oracle_wms import FlextOracleWmsClient, FlextOracleWmsClientConfig
    >>> config = FlextOracleWmsClientConfig(
    ...     base_url="https://your-wms.oraclecloud.com",
    ...     username="your_username",
    ...     password="your_password",
    ... )
    >>> client = FlextOracleWmsClient(config)
    >>> result = await client.discover_entities()
    >>> if result.success:
    ...     # Use a proper logger in real code; prints here are for doc illustration only
    ...     logger = get_logger(__name__)
    ...     logger.info("Discovered WMS entities", count=len(result.data))

Author: FLEXT Development Team
Version: 0.9.0
License: MIT

"""

# =============================================================================
# CONSOLIDATED WMS MODULE IMPORTS - New PEP8 Structure
# =============================================================================

# WMS Constants - Core constants and enums
from flext_oracle_wms.wms_constants import (
    FlextOracleWmsApiPaths,
    FlextOracleWmsConstants,
    FlextOracleWmsDefaults,
    FlextOracleWmsErrorMessages,
    FlextOracleWmsResponseFields,
    FlextOracleWmsSemanticConstants,
    OracleWMSAuthMethod,
    OracleWMSEntityType,
    OracleWMSFilterOperator,
    OracleWMSPageMode,
    OracleWMSWriteMode,
)

# WMS Configuration - Configuration management
from flext_oracle_wms.wms_config import (
    FlextOracleWmsClientConfig,
    FlextOracleWmsModuleConfig,
    WMSAPIVersion,
    WMSRetryAttempts,
    load_config,
)

# WMS Models - Data models and types
from flext_oracle_wms.wms_models import (
    FlextOracleWmsApiCategory,
    FlextOracleWmsApiEndpoint,
    FlextOracleWmsApiResponse,
    FlextOracleWmsApiVersion,
    FlextOracleWmsDiscoveryResult,
    FlextOracleWmsEntity,
    TOracleWmsApiResponse,
    TOracleWmsApiVersion,
    TOracleWmsDiscoveryResult,
    TOracleWmsEntityId,
    TOracleWmsEntityInfo,
    TOracleWmsEntityName,
    TOracleWmsEnvironment,
    TOracleWmsFilterValue,
    TOracleWmsFilters,
    TOracleWmsPaginationInfo,
    TOracleWmsRecord,
    TOracleWmsRecordBatch,
    TOracleWmsSchema,
    TOracleWmsTimeout,
)

# WMS Exceptions - Exception hierarchy
from flext_oracle_wms.wms_exceptions import (
    FlextOracleWmsApiError,
    FlextOracleWmsAuthenticationError,
    FlextOracleWmsConfigurationError,
    FlextOracleWmsConnectionError,
    FlextOracleWmsDataValidationError,
    FlextOracleWmsEntityNotFoundError,
    FlextOracleWmsError,
    FlextOracleWmsInventoryError,
    FlextOracleWmsPickingError,
    FlextOracleWmsProcessingError,
    FlextOracleWmsSchemaError,
    FlextOracleWmsSchemaFlatteningError,
    FlextOracleWmsShipmentError,
    FlextOracleWmsTimeoutError,
    FlextOracleWmsValidationError,
)

# WMS Client - Client and authentication
from flext_oracle_wms.wms_client import (
    FlextOracleWmsAuthConfig,
    FlextOracleWmsAuthPlugin,
    FlextOracleWmsAuthenticator,
    FlextOracleWmsClient,
    FlextOracleWmsClientMock,
    create_oracle_wms_client,
    flext_oracle_wms_create_api_key_auth,
    flext_oracle_wms_create_basic_auth,
    flext_oracle_wms_create_bearer_auth,
)

# WMS Discovery - Entity discovery and schema processing
from flext_oracle_wms.wms_discovery import (
    FlextOracleWmsCacheConfig,
    FlextOracleWmsCacheManager,
    FlextOracleWmsDynamicSchemaProcessor,
    FlextOracleWmsEntityDiscovery,
    flext_oracle_wms_create_cache_manager,
    flext_oracle_wms_create_dynamic_schema_processor,
    flext_oracle_wms_create_entity_discovery,
)

# WMS Operations - Data operations and utilities
from flext_oracle_wms.wms_operations import (
    FlextOracleWmsDataPlugin,
    FlextOracleWmsFilter,
    FlextOracleWmsFlattener,
    FlextOracleWmsPlugin,
    FlextOracleWmsPluginContext,
    FlextOracleWmsPluginRegistry,
    create_oracle_wms_data_plugin,
    create_oracle_wms_plugin_registry,
    flext_oracle_wms_build_entity_url,
    flext_oracle_wms_chunk_records,
    flext_oracle_wms_create_filter,
    flext_oracle_wms_extract_environment_from_url,
    flext_oracle_wms_extract_pagination_info,
    flext_oracle_wms_filter_by_field,
    flext_oracle_wms_filter_by_id_range,
    flext_oracle_wms_format_timestamp,
    flext_oracle_wms_normalize_url,
    flext_oracle_wms_validate_api_response,
    flext_oracle_wms_validate_entity_name,
)

# WMS API - API catalog and mock server
from flext_oracle_wms.wms_api import (
    FLEXT_ORACLE_WMS_APIS,
    OracleWmsMockServer,
    get_mock_server,
)

# Version information
__version__ = "0.9.0"
__version_info__ = tuple(int(x) for x in __version__.split(".") if x.isdigit())
__author__ = "FLEXT Contributors"
__description__ = (
    "Oracle WMS integration library using flext-core and flext-api patterns"
)

# =============================================================================
# PUBLIC API - Explicitly defined for clarity and backward compatibility
# =============================================================================

__all__: list[str] = [
    # API Catalog
    "FLEXT_ORACLE_WMS_APIS",
    "FlextOracleWmsApiCategory",
    "FlextOracleWmsApiEndpoint",
    "FlextOracleWmsApiVersion",
    # Constants
    "FlextOracleWmsApiPaths",
    "FlextOracleWmsConstants",
    "FlextOracleWmsDefaults",
    "FlextOracleWmsErrorMessages",
    "FlextOracleWmsResponseFields",
    "FlextOracleWmsSemanticConstants",
    "OracleWMSAuthMethod",
    "OracleWMSEntityType",
    "OracleWMSFilterOperator",
    "OracleWMSPageMode",
    "OracleWMSWriteMode",
    # Configuration
    "FlextOracleWmsClientConfig",
    "FlextOracleWmsModuleConfig",
    "WMSAPIVersion",
    "WMSRetryAttempts",
    "load_config",
    # Models
    "FlextOracleWmsApiResponse",
    "FlextOracleWmsDiscoveryResult",
    "FlextOracleWmsEntity",
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
    # Exceptions
    "FlextOracleWmsApiError",
    "FlextOracleWmsAuthenticationError",
    "FlextOracleWmsConfigurationError",
    "FlextOracleWmsConnectionError",
    "FlextOracleWmsDataValidationError",
    "FlextOracleWmsEntityNotFoundError",
    "FlextOracleWmsError",
    "FlextOracleWmsInventoryError",
    "FlextOracleWmsPickingError",
    "FlextOracleWmsProcessingError",
    "FlextOracleWmsSchemaError",
    "FlextOracleWmsSchemaFlatteningError",
    "FlextOracleWmsShipmentError",
    "FlextOracleWmsTimeoutError",
    "FlextOracleWmsValidationError",
    # Authentication
    "FlextOracleWmsAuthConfig",
    "FlextOracleWmsAuthPlugin",
    "FlextOracleWmsAuthenticator",
    # Core Client
    "FlextOracleWmsClient",
    "FlextOracleWmsClientMock",
    # Discovery and Cache
    "FlextOracleWmsCacheConfig",
    "FlextOracleWmsCacheManager",
    "FlextOracleWmsDynamicSchemaProcessor",
    "FlextOracleWmsEntityDiscovery",
    # Data Operations
    "FlextOracleWmsDataPlugin",
    "FlextOracleWmsFilter",
    "FlextOracleWmsFlattener",
    "FlextOracleWmsPlugin",
    "FlextOracleWmsPluginContext",
    "FlextOracleWmsPluginRegistry",
    # Mock Server
    "OracleWmsMockServer",
    "get_mock_server",
    # Factory Functions
    "create_oracle_wms_client",
    "create_oracle_wms_data_plugin",
    "create_oracle_wms_plugin_registry",
    "flext_oracle_wms_create_api_key_auth",
    "flext_oracle_wms_create_basic_auth",
    "flext_oracle_wms_create_bearer_auth",
    "flext_oracle_wms_create_cache_manager",
    "flext_oracle_wms_create_dynamic_schema_processor",
    "flext_oracle_wms_create_entity_discovery",
    "flext_oracle_wms_create_filter",
    # Helper Functions
    "flext_oracle_wms_build_entity_url",
    "flext_oracle_wms_chunk_records",
    "flext_oracle_wms_extract_environment_from_url",
    "flext_oracle_wms_extract_pagination_info",
    "flext_oracle_wms_filter_by_field",
    "flext_oracle_wms_filter_by_id_range",
    "flext_oracle_wms_format_timestamp",
    "flext_oracle_wms_normalize_url",
    "flext_oracle_wms_validate_api_response",
    "flext_oracle_wms_validate_entity_name",
    # Metadata
    "__version__",
    "__version_info__",
    "__author__",
    "__description__",
]
