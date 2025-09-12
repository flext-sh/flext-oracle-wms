"""Enterprise Oracle WMS Cloud integration library for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextTypes

# WMS Dynamic Schema Processing
from flext_oracle_wms.dynamic import (
    flext_oracle_wms_create_dynamic_schema_processor,
)

# WMS Filtering - Filter operations
from flext_oracle_wms.filtering import (
    FlextOracleWmsFilter,
    flext_oracle_wms_create_filter,
    flext_oracle_wms_filter_by_field,
    flext_oracle_wms_filter_by_id_range,
)

# WMS Flattening
from flext_oracle_wms.flattening import (
    FlextOracleWmsDataFlattener,
    flext_oracle_wms_create_data_flattener,
)

# WMS Constants - Core constants and enums
# WMS API - API catalog and mock server
from flext_oracle_wms.wms_api import (
    FLEXT_ORACLE_WMS_APIS,
    OracleWmsMockServer,
    get_mock_server,
)

# WMS Client - Client and authentication
from flext_oracle_wms.wms_client import (
    FlextOracleWmsAuthConfig,
    FlextOracleWmsAuthenticator,
    FlextOracleWmsAuthPlugin,
    FlextOracleWmsClient,
    FlextOracleWmsClientMock,
    create_oracle_wms_client,
    # REMOVED: Helper functions eliminated in favor of direct class usage
)

# WMS Configuration - Single source of truth
from flext_oracle_wms.wms_config import (
    FlextOracleWmsClientConfig,
    FlextOracleWmsConfig,
    FlextOracleWmsModuleConfig,
)
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

# WMS Discovery - Entity discovery and schema processing
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
    # REMOVED: Helper functions eliminated in favor of direct class usage
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
    TOracleWmsFilters,
    TOracleWmsFilterValue,
    TOracleWmsPaginationInfo,
    TOracleWmsRecord,
    TOracleWmsRecordBatch,
    TOracleWmsSchema,
    TOracleWmsTimeout,
)

# WMS Operations - Data operations and utilities
from flext_oracle_wms.wms_operations import (
    FlextOracleWmsDataPlugin,
    FlextOracleWmsFilterConfig,
    FlextOracleWmsFlattener,
    FlextOracleWmsPlugin,
    FlextOracleWmsPluginContext,
    FlextOracleWmsPluginRegistry,
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
    validate_dict_parameter,
    validate_records_list,
    validate_string_parameter,
)

# Version information
__version__ = "0.9.0"
__version_info__ = tuple(int(x) for x in __version__.split(".") if x.isdigit())
__author__ = "FLEXT Contributors"
__description__ = (
    "Oracle WMS integration library using flext-core and flext-api patterns"
)


__all__: FlextTypes.Core.StringList = [
    "DISCOVERY_FAILURE",
    "DISCOVERY_SUCCESS",
    "FLEXT_ORACLE_WMS_APIS",
    "DiscoveryContext",
    "EndpointDiscoveryStrategy",
    "EntityResponseParser",
    "FlextOracleWmsApiCategory",
    "FlextOracleWmsApiEndpoint",
    "FlextOracleWmsApiError",
    "FlextOracleWmsApiPaths",
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
    "FlextOracleWmsClientConfig",
    "FlextOracleWmsClientMock",
    "FlextOracleWmsConfig",
    "FlextOracleWmsConfigurationError",
    "FlextOracleWmsConnectionError",
    "FlextOracleWmsConstants",
    "FlextOracleWmsDataFlattener",
    "FlextOracleWmsDataPlugin",
    "FlextOracleWmsDataValidationError",
    "FlextOracleWmsDefaults",
    "FlextOracleWmsDiscoveryResult",
    "FlextOracleWmsDynamicSchemaProcessor",
    "FlextOracleWmsEntity",
    "FlextOracleWmsEntityDiscovery",
    "FlextOracleWmsEntityNotFoundError",
    "FlextOracleWmsError",
    "FlextOracleWmsErrorMessages",
    "FlextOracleWmsFilter",
    "FlextOracleWmsFilterConfig",
    "FlextOracleWmsFlattener",
    "FlextOracleWmsInventoryError",
    "FlextOracleWmsModuleConfig",
    "FlextOracleWmsPickingError",
    "FlextOracleWmsPlugin",
    "FlextOracleWmsPluginContext",
    "FlextOracleWmsPluginRegistry",
    "FlextOracleWmsProcessingError",
    "FlextOracleWmsResponseFields",
    "FlextOracleWmsSchemaError",
    "FlextOracleWmsSchemaFlatteningError",
    "FlextOracleWmsSemanticConstants",
    "FlextOracleWmsShipmentError",
    "FlextOracleWmsTimeoutError",
    "FlextOracleWmsUnifiedConfig",
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
    "WMSAPIVersion",
    "WMSRetryAttempts",
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
    "flext_oracle_wms_create_dynamic_schema_processor",
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
    "load_config",
    "validate_dict_parameter",
    "validate_records_list",
    "validate_string_parameter",
]

# -----------------------------------------------------------------------------
# Test helper: provide builtin `_run(cmd_list, cwd)` used by example tests
# Some tests call `_run` at module scope; expose it via builtins so name lookup
# succeeds even if not defined locally in the test function.
# -----------------------------------------------------------------------------
try:  # pragma: no cover - helper glue for tests only
    import asyncio as _asyncio
    import builtins as _builtins

    async def _run(
        cmd_list: FlextTypes.Core.StringList, cwd: str | None = None
    ) -> tuple[int, str, str]:
        """Run function.

        Args:
            cmd_list (FlextTypes.Core.StringList): Description.
            cwd (str | None): Description.

        Returns:
            tuple[int, str, str]: Description.

        """
        proc = await _asyncio.create_subprocess_exec(
            *cmd_list,
            cwd=cwd,
            stdout=_asyncio.subprocess.PIPE,
            stderr=_asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        return proc.returncode or 0, stdout.decode(), stderr.decode()

    setattr(_builtins, "_run", _run)
except Exception:  # pragma: no cover - defensive
    # Test helper setup failed, tests will need to provide _run themselves
    # This is non-critical as it only affects test utilities
    from flext_core import FlextLogger

    FlextLogger(__name__).debug(
        "Test helper _run setup failed, tests may need manual setup"
    )
