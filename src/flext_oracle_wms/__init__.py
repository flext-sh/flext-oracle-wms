"""Enterprise Oracle WMS Cloud integration library for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_oracle_wms.__version__ import __version__, __version_info__
from flext_oracle_wms.config import FlextOracleWmsConfig
from flext_oracle_wms.constants import (
    FlextOracleWmsConstants,
    OracleWMSAuthMethod,
)
from flext_oracle_wms.wms_client import FlextOracleWmsClient
from flext_oracle_wms.wms_exceptions import (
    FlextOracleWmsApiError,
    FlextOracleWmsEntityNotFoundError,
    FlextOracleWmsExceptions,
    FlextOracleWmsInventoryError,
    FlextOracleWmsPickingError,
    FlextOracleWmsSchemaError,
    FlextOracleWmsSchemaFlatteningError,
    FlextOracleWmsShipmentError,
)
from flext_oracle_wms.wms_models import (
    FlextOracleWmsApiVersion,
    TOracleWmsApiResponse,
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


# Import mock server function
def get_mock_server(environment: str = "mock_test") -> object:
    """Get Oracle WMS mock server instance."""
    from flext_oracle_wms.wms_api import FlextOracleWmsApi

    return FlextOracleWmsApi.get_mock_server(environment)


# Configuration aliases for backward compatibility
FlextOracleWmsClientConfig = FlextOracleWmsConfig
FlextOracleWmsModuleConfig = FlextOracleWmsConfig


__all__ = [
    "FlextOracleWmsApiError",
    # Types and models
    "FlextOracleWmsApiVersion",
    # Core classes
    "FlextOracleWmsClient",
    # Backward compatibility aliases
    "FlextOracleWmsClientConfig",
    "FlextOracleWmsConfig",
    # Constants and enums
    "FlextOracleWmsConstants",
    "FlextOracleWmsEntityNotFoundError",
    # Exception hierarchy
    "FlextOracleWmsExceptions",
    "FlextOracleWmsInventoryError",
    "FlextOracleWmsModuleConfig",
    "FlextOracleWmsPickingError",
    "FlextOracleWmsSchemaError",
    "FlextOracleWmsSchemaFlatteningError",
    "FlextOracleWmsShipmentError",
    "OracleWMSAuthMethod",
    "TOracleWmsApiResponse",
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
    # Version info
    "__version__",
    "__version_info__",
    # Utilities
    "get_mock_server",
]
