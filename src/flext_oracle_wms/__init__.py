"""Enterprise Oracle WMS Cloud integration library for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Final

from flext_oracle_wms.api import FlextOracleWms
from flext_oracle_wms.config import (
    FlextOracleWmsClientConfig,
    FlextOracleWmsConfig,
)
from flext_oracle_wms.filtering import (
    FlextOracleWmsFilter,
)
from flext_oracle_wms.flattening import (
    FlextOracleWmsDataFlattener,
)
from flext_oracle_wms.protocols import FlextOracleWmsProtocols
from flext_oracle_wms.typings import FlextOracleWmsTypes
from flext_oracle_wms.utilities import FlextOracleWmsUtilities
from flext_oracle_wms.version import VERSION, FlextOracleWmsVersion
from flext_oracle_wms.wms_api import (
    FLEXT_ORACLE_WMS_APIS,
    FlextOracleWmsApiCategory,
    FlextOracleWmsApiEndpoint,
    OracleWmsMockServer,
    get_mock_server,
)
from flext_oracle_wms.wms_client import (
    FlextOracleWmsClient,
)
from flext_oracle_wms.wms_constants import (
    FlextOracleWmsApiVersion,
    FlextOracleWmsConstants,
    FlextOracleWmsDefaults,
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
    FlextOracleWmsUnifiedOperations,
)

PROJECT_VERSION: Final[FlextOracleWmsVersion] = VERSION

__version__: str = VERSION.version
__version_info__: tuple[int | str, ...] = VERSION.version_info

__all__ = [
    "DISCOVERY_FAILURE",
    "DISCOVERY_SUCCESS",
    "FLEXT_ORACLE_WMS_APIS",
    "PROJECT_VERSION",
    "VERSION",
    "DiscoveryContext",
    "EndpointDiscoveryStrategy",
    "EntityResponseParser",
    "FlextOracleWms",
    "FlextOracleWmsApiCategory",
    "FlextOracleWmsApiEndpoint",
    "FlextOracleWmsApiError",
    "FlextOracleWmsApiVersion",
    "FlextOracleWmsAuthenticationError",
    "FlextOracleWmsCacheConfig",
    "FlextOracleWmsCacheEntry",
    "FlextOracleWmsCacheManager",
    "FlextOracleWmsCacheStats",
    "FlextOracleWmsClient",
    "FlextOracleWmsClientConfig",
    "FlextOracleWmsConfig",
    "FlextOracleWmsConfigurationError",
    "FlextOracleWmsConnectionError",
    "FlextOracleWmsConstants",
    "FlextOracleWmsDataFlattener",
    "FlextOracleWmsDataValidationError",
    "FlextOracleWmsDefaults",
    "FlextOracleWmsDynamicSchemaProcessor",
    "FlextOracleWmsEntityDiscovery",
    "FlextOracleWmsEntityNotFoundError",
    "FlextOracleWmsError",
    "FlextOracleWmsFilter",
    "FlextOracleWmsInventoryError",
    "FlextOracleWmsPickingError",
    "FlextOracleWmsProcessingError",
    "FlextOracleWmsProtocols",
    "FlextOracleWmsSchemaError",
    "FlextOracleWmsSchemaFlatteningError",
    "FlextOracleWmsShipmentError",
    "FlextOracleWmsTimeoutError",
    "FlextOracleWmsTypes",
    "FlextOracleWmsUnifiedOperations",
    "FlextOracleWmsUtilities",
    "FlextOracleWmsValidationError",
    "FlextOracleWmsVersion",
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
    "__version__",
    "__version_info__",
    "get_mock_server",
]
