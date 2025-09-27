"""Enterprise Oracle WMS Cloud integration library for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

# from flext_oracle_wms.dynamic import flext_oracle_wms_create_dynamic_schema_processor
from flext_oracle_wms.filtering import (
    FlextOracleWmsFilter,
    flext_oracle_wms_create_filter,
    flext_oracle_wms_filter_by_field,
    flext_oracle_wms_filter_by_id_range,
)
from flext_oracle_wms.flattening import (
    FlextOracleWmsDataFlattener,
    flext_oracle_wms_create_data_flattener,
)
from flext_oracle_wms.typings import FlextOracleWmsTypes
from flext_oracle_wms.utilities import FlextOracleWmsUtilities
from flext_oracle_wms.wms_api import (
    FLEXT_ORACLE_WMS_APIS,
    FlextOracleWmsApiCategory,
    FlextOracleWmsApiEndpoint,
    OracleWmsMockServer,
    get_mock_server,
)
from flext_oracle_wms.wms_client import (
    FlextOracleWmsAuthConfig,
    FlextOracleWmsAuthenticator,
    FlextOracleWmsAuthPlugin,
    FlextOracleWmsClient,
    FlextOracleWmsClientMock,
    create_oracle_wms_client,
)
from flext_oracle_wms.wms_config import (
    FlextOracleWmsConfig,
)
from flext_oracle_wms.wms_constants import (
    FlextOracleWmsApiVersion,
    FlextOracleWmsConstants,
    OracleWMSAuthMethod,
    OracleWMSEntityType,
    OracleWMSFilterOperator,
    OracleWMSPageMode,
    OracleWMSWriteMode,
)
from flext_oracle_wms.wms_discovery import (
    DISCOVERY_FAILURE,
    DISCOVERY_SUCCESS,
    DiscoveryContext,
    EndpointDiscoveryStrategy,
    EntityResponseParser,
    FlextOracleWmsCacheConfig,
    FlextOracleWmsCacheEntry,
    FlextOracleWmsCacheManager,
    FlextOracleWmsCacheStats,
    FlextOracleWmsDynamicSchemaProcessor,
    FlextOracleWmsEntityDiscovery,
)
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
from flext_oracle_wms.wms_models import (
    FlextOracleWmsApiResponse,
    FlextOracleWmsDiscoveryResult,
    FlextOracleWmsEntity,
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
from flext_oracle_wms.wms_operations import (
    FlextOracleWmsDataPlugin,
    FlextOracleWmsFlattener,
    FlextOracleWmsPlugin,
    FlextOracleWmsPluginContext,
    FlextOracleWmsPluginRegistry,
    FlextOracleWmsUnifiedOperations,
    create_oracle_wms_data_plugin,
    create_oracle_wms_plugin_registry,
    flext_oracle_wms_build_entity_url,
    flext_oracle_wms_chunk_records,
    flext_oracle_wms_extract_environment_from_url,
    flext_oracle_wms_extract_pagination_info,
    flext_oracle_wms_format_timestamp,
    flext_oracle_wms_normalize_url,
    flext_oracle_wms_validate_api_response,
    flext_oracle_wms_validate_entity_name,
)

# WMS Filtering - Filter operations

# WMS Flattening - Data flattening operations

# WMS Constants - Core constants and enums
# WMS API - API catalog and mock server

# WMS Client - Client and authentication

# WMS Configuration - Single source of truth

# WMS Discovery - Entity discovery and schema processing

# WMS Exceptions - Exception hierarchy

# WMS Models - Data models and types

# WMS Operations - Unified operations consolidating filtering, flattening, and utilities
# WMS Operations - Data operations and utilities

# Version information
__version__ = "0.9.0"
__version_info__ = tuple(int(x) for x in __version__.split(".") if x.isdigit())
__author__ = "FLEXT Contributors"
__description__ = (
    "Oracle WMS integration library using flext-core and flext-api patterns"
)


__all__: FlextOracleWmsTypes.Core.StringList = [
    "DISCOVERY_FAILURE",
    "DISCOVERY_SUCCESS",
    "FLEXT_ORACLE_WMS_APIS",
    "DiscoveryContext",
    "EndpointDiscoveryStrategy",
    "EntityResponseParser",
    "FlextOracleWmsApiCategory",
    "FlextOracleWmsApiEndpoint",
    "FlextOracleWmsApiError",
    "FlextOracleWmsApiResponse",
    "FlextOracleWmsApiVersion",
    "FlextOracleWmsAuthConfig",
    "FlextOracleWmsAuthPlugin",
    "FlextOracleWmsAuthenticationError",
    "FlextOracleWmsAuthenticator",
    "FlextOracleWmsCacheConfig",
    "FlextOracleWmsCacheEntry",
    "FlextOracleWmsCacheManager",
    "FlextOracleWmsCacheStats",
    "FlextOracleWmsClient",
    "FlextOracleWmsClientMock",
    "FlextOracleWmsConfig",
    "FlextOracleWmsConfigurationError",
    "FlextOracleWmsConnectionError",
    "FlextOracleWmsConstants",
    "FlextOracleWmsDataFlattener",
    "FlextOracleWmsDataPlugin",
    "FlextOracleWmsDataValidationError",
    "FlextOracleWmsDiscoveryResult",
    "FlextOracleWmsDynamicSchemaProcessor",
    "FlextOracleWmsEntity",
    "FlextOracleWmsEntityDiscovery",
    "FlextOracleWmsEntityNotFoundError",
    "FlextOracleWmsError",
    "FlextOracleWmsFilter",
    "FlextOracleWmsFlattener",
    "FlextOracleWmsInventoryError",
    "FlextOracleWmsPickingError",
    "FlextOracleWmsPlugin",
    "FlextOracleWmsPluginContext",
    "FlextOracleWmsPluginRegistry",
    "FlextOracleWmsProcessingError",
    "FlextOracleWmsSchemaError",
    "FlextOracleWmsSchemaFlatteningError",
    "FlextOracleWmsShipmentError",
    "FlextOracleWmsTimeoutError",
    "FlextOracleWmsUnifiedOperations",
    "FlextOracleWmsUtilities",
    "FlextOracleWmsValidationError",
    "OracleWMSAuthMethod",
    "OracleWMSEntityType",
    "OracleWMSFilterOperator",
    "OracleWMSPageMode",
    "OracleWMSWriteMode",
    "OracleWmsMockServer",
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
    "__version__",
    "__version_info__",
    "create_oracle_wms_client",
    "create_oracle_wms_data_plugin",
    "create_oracle_wms_plugin_registry",
    "flext_oracle_wms_build_entity_url",
    "flext_oracle_wms_chunk_records",
    "flext_oracle_wms_create_data_flattener",
    # "flext_oracle_wms_create_dynamic_schema_processor",
    "flext_oracle_wms_create_filter",
    "flext_oracle_wms_extract_environment_from_url",
    "flext_oracle_wms_extract_pagination_info",
    "flext_oracle_wms_filter_by_field",
    "flext_oracle_wms_filter_by_id_range",
    "flext_oracle_wms_format_timestamp",
    "flext_oracle_wms_normalize_url",
    "flext_oracle_wms_validate_api_response",
    "flext_oracle_wms_validate_entity_name",
    "get_mock_server",
]
