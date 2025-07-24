"""Enterprise Oracle WMS client library for FLEXT data integration platform.

This library provides comprehensive Oracle WMS integration capabilities with:
- Python 3.13 type safety and flext-core integration
- Mandatory flattening/deflattening capabilities for Singer SDK compliance
- Advanced filtering with all required operators
  (eq, neq, gt, gte, lt, lte, in, nin, like)
- Dynamic schema discovery and entity processing
- Pagination modes: "api" (offset-based) and "sequenced" (cursor-based)
- Complete Oracle WMS API integration (NOT Oracle Database)

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

__version__ = "2.0.0"

# Core Oracle WMS client and configuration (NEW CLASSES)
# Legacy client for compatibility
from flext_oracle_wms.authentication import (
    FlextOracleWmsAuth,
    FlextOracleWmsOAuth2Auth,
    flext_oracle_wms_create_authenticator,
    flext_oracle_wms_create_oauth2_authenticator,
    flext_oracle_wms_get_api_headers,
)
from flext_oracle_wms.client import FlextOracleWmsLegacyClient
from flext_oracle_wms.client_class import (
    FlextOracleWmsAuthenticationError,
    FlextOracleWmsClient,
    FlextOracleWmsClientError,
    FlextOracleWmsConnectionError,
)
from flext_oracle_wms.config import (
    FlextOracleWMSConfig,
    OracleWMSConfiguration,
    OracleWMSConnectionConfiguration,
    OracleWMSEntityConfiguration,
    OracleWMSSchemaConfiguration,
)
from flext_oracle_wms.config_class import FlextOracleWmsConfig
from flext_oracle_wms.config_module import FlextOracleWmsModuleConfig
from flext_oracle_wms.constants import (
    FlextOracleWmsDefaults,
    FlextOracleWmsEntityTypes,
    FlextOracleWmsFilterOperators,
    FlextOracleWmsPageModes,
    FlextOracleWmsWriteModes,
)

# Advanced filtering capabilities
from flext_oracle_wms.filtering import (
    FilterCondition,
    FilterQuery,
    FilterResult,
    FlextOracleWmsAdvancedFilter,
    flext_oracle_wms_create_advanced_filter,
    flext_oracle_wms_filter_by_id_range,
    flext_oracle_wms_filter_by_modification_time,
)

# Helper functions with flext_oracle_wms_ prefix
from flext_oracle_wms.helpers import (
    flext_oracle_wms_build_filter_query,
    flext_oracle_wms_calculate_pagination_info,
    flext_oracle_wms_extract_entity_metadata,
    flext_oracle_wms_format_wms_record,
    flext_oracle_wms_sanitize_entity_name,
    flext_oracle_wms_validate_connection,
)

# Infrastructure capabilities
from flext_oracle_wms.infrastructure import (
    FlextOracleWmsCacheManager,
    FlextOracleWmsEntityDiscovery,
    flext_oracle_wms_create_cache_manager,
    flext_oracle_wms_create_entity_discovery,
)
from flext_oracle_wms.models import (
    FlextOracleWmsDiscoveryResult,
    FlextOracleWmsEntity,
    FlextOracleWmsEntityField,
    FlextOracleWmsError,
    FlextOracleWmsRecordModel,
    FlextOracleWmsResponse,
)

# Dynamic schema processing
from flext_oracle_wms.schema import (
    FlextOracleWmsDynamicSchemaProcessor,
    FlextOracleWmsEntityProcessingResult,
    FlextOracleWmsSchemaDiscoveryResult,
    flext_oracle_wms_create_dynamic_schema_processor,
    flext_oracle_wms_discover_entity_schemas,
    flext_oracle_wms_process_entity_with_schema,
)

# Singer SDK capabilities - MANDATORY flattening/deflattening
# Factory functions for easy instantiation
from flext_oracle_wms.singer import (
    FlatteningResult,
    FlextOracleWmsDeflattener,
    FlextOracleWmsDeflatteningResult,
    FlextOracleWmsFlattener,
    flext_oracle_wms_create_deflattener,
    flext_oracle_wms_create_flattener,
    flext_oracle_wms_deflattened_wms_record,
    flext_oracle_wms_flatten_wms_record,
)

# Type mapping and authentication
from flext_oracle_wms.type_mapping import (
    FlextOracleWmsTypeMapper,
    flext_oracle_wms_create_type_mapper,
    flext_oracle_wms_get_primary_key_schema,
    flext_oracle_wms_get_replication_key_schema,
    flext_oracle_wms_is_timestamp_field,
    flext_oracle_wms_map_oracle_to_singer,
)

# Type definitions and constants
from flext_oracle_wms.typedefs import (
    FlextOracleWmsConnectionInfo,
    FlextOracleWmsEntityInfo,
    WMSFilterCondition,
    WMSFilters,
    WMSFlattenedRecord,
    WMSFlattenedSchema,
    WMSRecord,
    WMSRecordBatch,
    WMSSchema,
)

__all__ = [
    "FilterCondition",
    "FilterQuery",
    "FilterResult",
    "FlatteningResult",
    "FlextOracleWMSConfig",
    # Advanced filtering
    "FlextOracleWmsAdvancedFilter",
    "FlextOracleWmsAuth",
    "FlextOracleWmsAuthenticationError",
    # Infrastructure capabilities
    "FlextOracleWmsCacheManager",
    # NEW CLASSES with FlextOracleWms prefix (proper naming)
    "FlextOracleWmsClient",
    "FlextOracleWmsClientError",
    "FlextOracleWmsConfig",
    "FlextOracleWmsConnectionError",
    "FlextOracleWmsConnectionInfo",
    # Updated constants with FlextOracleWms prefix
    "FlextOracleWmsDefaults",
    # Singer SDK capabilities (MANDATORY) - using correct class names
    "FlextOracleWmsDeflattener",
    "FlextOracleWmsDeflatteningResult",
    # Updated models with FlextOracleWms prefix
    "FlextOracleWmsDiscoveryResult",
    # Dynamic schema processing
    "FlextOracleWmsDynamicSchemaProcessor",
    "FlextOracleWmsEntity",
    "FlextOracleWmsEntityDiscovery",
    "FlextOracleWmsEntityField",
    "FlextOracleWmsEntityInfo",
    "FlextOracleWmsEntityProcessingResult",
    "FlextOracleWmsEntityTypes",
    "FlextOracleWmsError",
    "FlextOracleWmsFilterOperators",
    "FlextOracleWmsFlattener",
    # Core client and configuration
    "FlextOracleWmsLegacyClient",
    "FlextOracleWmsModuleConfig",
    "FlextOracleWmsOAuth2Auth",
    "FlextOracleWmsPageModes",
    "FlextOracleWmsRecordModel",
    "FlextOracleWmsResponse",
    # Schema discovery - using correct class name
    "FlextOracleWmsSchemaDiscoveryResult",
    # Type mapping functions
    "FlextOracleWmsTypeMapper",
    "FlextOracleWmsWriteModes",
    "OracleWMSConfiguration",
    "OracleWMSConnectionConfiguration",
    "OracleWMSEntityConfiguration",
    "OracleWMSSchemaConfiguration",
    "WMSFilterCondition",
    "WMSFilters",
    "WMSFlattenedRecord",
    "WMSFlattenedSchema",
    # Type definitions
    "WMSRecord",
    "WMSRecordBatch",
    "WMSSchema",
    # Helper functions with flext_oracle_wms_ prefix
    "flext_oracle_wms_build_filter_query",
    "flext_oracle_wms_calculate_pagination_info",
    "flext_oracle_wms_create_advanced_filter",
    # Authentication functions
    "flext_oracle_wms_create_authenticator",
    "flext_oracle_wms_create_cache_manager",
    "flext_oracle_wms_create_deflattener",
    "flext_oracle_wms_create_dynamic_schema_processor",
    "flext_oracle_wms_create_entity_discovery",
    "flext_oracle_wms_create_flattener",
    "flext_oracle_wms_create_oauth2_authenticator",
    "flext_oracle_wms_create_type_mapper",
    "flext_oracle_wms_deflattened_wms_record",
    "flext_oracle_wms_discover_entity_schemas",
    "flext_oracle_wms_extract_entity_metadata",
    "flext_oracle_wms_filter_by_id_range",
    "flext_oracle_wms_filter_by_modification_time",
    "flext_oracle_wms_flatten_wms_record",
    "flext_oracle_wms_format_wms_record",
    "flext_oracle_wms_get_api_headers",
    "flext_oracle_wms_get_primary_key_schema",
    "flext_oracle_wms_get_replication_key_schema",
    "flext_oracle_wms_is_timestamp_field",
    "flext_oracle_wms_map_oracle_to_singer",
    "flext_oracle_wms_process_entity_with_schema",
    "flext_oracle_wms_sanitize_entity_name",
    "flext_oracle_wms_validate_connection",
]
