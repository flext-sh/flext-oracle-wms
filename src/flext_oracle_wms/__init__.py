"""Enterprise Oracle WMS Cloud integration library for FLEXT ecosystem."""

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
    # REMOVED: Helper functions eliminated in favor of direct class usage
)

# WMS Discovery - Entity discovery and schema processing
from flext_oracle_wms.wms_discovery import (
    FlextOracleWmsCacheConfig,
    FlextOracleWmsCacheManager,
    FlextOracleWmsDynamicSchemaProcessor,
    FlextOracleWmsEntityDiscovery,
    # REMOVED: Helper functions eliminated in favor of direct class usage
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
    # REMOVED: flext_oracle_wms_create_filter (use FlextOracleWmsFilter directly)
    flext_oracle_wms_extract_environment_from_url,
    flext_oracle_wms_extract_pagination_info,
    # REMOVED: flext_oracle_wms_filter_by_field (use FlextOracleWmsFilter directly)
    # REMOVED: flext_oracle_wms_filter_by_id_range (use FlextOracleWmsFilter directly)
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
    # REMOVED: Factory functions eliminated in favor of direct class usage
    # Helper Functions
    "flext_oracle_wms_build_entity_url",
    "flext_oracle_wms_chunk_records",
    "flext_oracle_wms_extract_environment_from_url",
    "flext_oracle_wms_extract_pagination_info",
    # REMOVED: Factory functions eliminated in favor of direct class usage
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

# -----------------------------------------------------------------------------
# Test helper: provide builtin `_run(cmd_list, cwd)` used by example tests
# Some tests call `_run` at module scope; expose it via builtins so name lookup
# succeeds even if not defined locally in the test function.
# -----------------------------------------------------------------------------
try:  # pragma: no cover - helper glue for tests only
    import asyncio as _asyncio
    import builtins as _builtins

    async def _run(cmd_list: list[str], cwd: str | None = None) -> tuple[int, str, str]:
        """Run function.

        Args:
            cmd_list (list[str]): Description.
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
