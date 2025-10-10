"""Enterprise Oracle WMS Cloud integration library for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextResult

from flext_oracle_wms.__version__ import __version__, __version_info__
from flext_oracle_wms.api import FlextOracleWms
from flext_oracle_wms.config import (
    FlextOracleWmsClientConfig,
    FlextOracleWmsConfig,
)
from flext_oracle_wms.constants import (
    FlextOracleWmsApiVersion,
    FlextOracleWmsConstants,
    OracleWMSAuthMethod,
)
from flext_oracle_wms.protocols import FlextOracleWmsProtocols
from flext_oracle_wms.typings import FlextOracleWmsTypes
from flext_oracle_wms.wms_api import (
    FLEXT_ORACLE_WMS_APIS,
    FlextOracleWmsApiCategory,
    FlextOracleWmsApiEndpoint,
    OracleWmsMockServer,
)
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
    get_mock_server,
)

# Create aliases for commonly used exceptions
FlextOracleWmsError = FlextOracleWmsExceptions.BaseError
FlextOracleWmsAuthenticationError = FlextOracleWmsExceptions.AuthenticationError
FlextOracleWmsConnectionError = FlextOracleWmsExceptions.WmsConnectionError
FlextOracleWmsConfigurationError = FlextOracleWmsExceptions.ConfigurationError
FlextOracleWmsDataValidationError = FlextOracleWmsExceptions.DataValidationError
FlextOracleWmsProcessingError = FlextOracleWmsExceptions.ProcessingError
FlextOracleWmsTimeoutError = FlextOracleWmsExceptions.WmsTimeoutError
FlextOracleWmsValidationError = FlextOracleWmsExceptions.ValidationError


# Placeholder classes for missing auth components (to be implemented)
class FlextOracleWmsAuthConfig:
    """Placeholder for Oracle WMS authentication configuration."""

    def __init__(
        self, auth_type: str = "basic", username: str = "", password: str = ""
    ) -> None:
        """Initialize authentication configuration."""
        self.auth_type = auth_type
        self.username = username
        self.password = password

    def validate_business_rules(self) -> FlextResult[bool]:
        """Validate authentication configuration business rules."""
        from flext_core import FlextResult

        return FlextResult.ok(True)


class FlextOracleWmsAuthenticator:
    """Placeholder for Oracle WMS authenticator."""

    def __init__(self, config: FlextOracleWmsAuthConfig) -> None:
        """Initialize authenticator with configuration."""
        self.config = config

    def get_auth_headers(self) -> FlextResult[dict[str, str]]:
        """Get authentication headers."""
        from flext_core import FlextResult

        return FlextResult.ok({"Authorization": "Basic placeholder"})


# Import models at module level

# wms_operations module temporarily removed
# from flext_oracle_wms.wms_operations import (
#     FlextOracleWmsUnifiedOperations,
# )


__all__ = [
    "FLEXT_ORACLE_WMS_APIS",
    "FlextOracleWms",
    "FlextOracleWmsApiCategory",
    "FlextOracleWmsApiEndpoint",
    "FlextOracleWmsApiError",
    "FlextOracleWmsApiVersion",
    "FlextOracleWmsAuthConfig",
    "FlextOracleWmsAuthenticationError",
    "FlextOracleWmsAuthenticator",
    "FlextOracleWmsClient",
    "FlextOracleWmsClientConfig",
    "FlextOracleWmsConfig",
    "FlextOracleWmsConfigurationError",
    "FlextOracleWmsConnectionError",
    "FlextOracleWmsConstants",
    "FlextOracleWmsDataValidationError",
    "FlextOracleWmsEntityNotFoundError",
    "FlextOracleWmsError",
    "FlextOracleWmsExceptions",
    "FlextOracleWmsInventoryError",
    "FlextOracleWmsPickingError",
    "FlextOracleWmsProcessingError",
    "FlextOracleWmsProtocols",
    "FlextOracleWmsSchemaError",
    "FlextOracleWmsSchemaFlatteningError",
    "FlextOracleWmsShipmentError",
    "FlextOracleWmsTimeoutError",
    "FlextOracleWmsTypes",
    "FlextOracleWmsValidationError",
    "OracleWMSAuthMethod",
    "OracleWmsMockServer",
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
    "__version__",
    "__version_info__",
    "get_mock_server",
]
