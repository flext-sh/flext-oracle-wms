"""Legacy compatibility layer for flext-oracle-wms modernization.

This module provides backward compatibility for legacy exception classes and APIs
that were refactored during the flext-core modernization. All legacy names are
maintained as facades to the new FlextErrorMixin-based exceptions.

This layer will be deprecated in a future version. Please migrate to the new
FlextOracleWms* exception classes for modern error handling patterns.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import warnings

from flext_oracle_wms.authentication import FlextOracleWmsAuthenticator
from flext_oracle_wms.client import FlextOracleWmsClient
from flext_oracle_wms.config import FlextOracleWmsClientConfig
from flext_oracle_wms.exceptions import FlextOracleWmsProcessingError


def _deprecation_warning(old_name: str, new_name: str) -> None:
    """Issue deprecation warning for legacy API usage."""
    warnings.warn(
        f"{old_name} is deprecated. Use {new_name} instead. "
        f"Legacy compatibility will be removed in a future version.",
        DeprecationWarning,
        stacklevel=3,
    )


# Legacy exception aliases following facade pattern from wms_exceptions.py
def flext_oracle_wms_filter_error(
    *args: object, **_kwargs: object
) -> FlextOracleWmsProcessingError:  # noqa: N802
    """Legacy: Use FlextOracleWmsProcessingError instead."""
    _deprecation_warning("FlextOracleWmsFilterError", "FlextOracleWmsProcessingError")
    # Convert positional args to message and pass kwargs as context
    message = str(args[0]) if args else "Filter error"
    return FlextOracleWmsProcessingError(message)


def flext_oracle_wms_rate_limit_error(
    *args: object, **_kwargs: object
) -> FlextOracleWmsProcessingError:  # noqa: N802
    """Legacy: Use FlextOracleWmsProcessingError instead."""
    _deprecation_warning(
        "FlextOracleWmsRateLimitError", "FlextOracleWmsProcessingError"
    )
    # Convert positional args to message and pass kwargs as context
    message = str(args[0]) if args else "Rate limit error"
    return FlextOracleWmsProcessingError(message)


# Legacy class aliases for compatibility
FlextOracleWmsFilterError = flext_oracle_wms_filter_error
FlextOracleWmsRateLimitError = flext_oracle_wms_rate_limit_error


# Legacy API function aliases
def create_wms_client(*args: object, **kwargs: object) -> object:  # noqa: N802
    """Legacy: Use FlextOracleWmsClient directly instead."""
    _deprecation_warning("create_wms_client", "FlextOracleWmsClient")
    return FlextOracleWmsClient(*args, **kwargs)


def create_wms_config(*args: object, **kwargs: object) -> object:  # noqa: N802
    """Legacy: Use FlextOracleWmsClientConfig directly instead."""
    _deprecation_warning("create_wms_config", "FlextOracleWmsClientConfig")
    return FlextOracleWmsClientConfig(*args, **kwargs)


def setup_wms_authentication(*args: object, **kwargs: object) -> object:  # noqa: N802
    """Legacy: Use FlextOracleWmsAuthenticator directly instead."""
    _deprecation_warning("setup_wms_authentication", "FlextOracleWmsAuthenticator")
    if FlextOracleWmsAuthenticator is None:
        msg = "FlextOracleWmsAuthenticator not available"
        raise ImportError(msg) from None
    return FlextOracleWmsAuthenticator(*args, **kwargs)


# Legacy constants and configuration from Oracle WMS patterns
WMS_DEFAULT_TIMEOUT = 30.0
WMS_DEFAULT_RETRY_COUNT = 3
WMS_DEFAULT_BATCH_SIZE = 100
WMS_DEFAULT_CACHE_TTL = 300  # 5 minutes


# Legacy parameter factories for compatibility - simplified
def wms_validation_error_params(**kwargs: object) -> dict[str, object]:  # noqa: N802
    """Legacy: Create parameters for WMS validation error - use FlextOracleWmsDataValidationError context instead."""
    _deprecation_warning(
        "WmsValidationErrorParams",
        "FlextOracleWmsDataValidationError context parameter",
    )
    return {
        "field_name": kwargs.get("field_name"),
        "field_value": kwargs.get("field_value"),
        "validation_rule": kwargs.get("validation_rule"),
        "entity_name": kwargs.get("entity_name"),
    }


def wms_configuration_error_params(**kwargs: object) -> dict[str, object]:  # noqa: N802
    """Legacy: Create parameters for WMS configuration error - use FlextOracleWmsConfigError context instead."""
    _deprecation_warning(
        "WmsConfigurationErrorParams", "FlextOracleWmsConfigError context parameter"
    )
    return {
        "config_key": kwargs.get("config_key"),
        "config_value": kwargs.get("config_value"),
        "config_section": kwargs.get("config_section"),
        "valid_range": kwargs.get("valid_range"),
    }


def wms_api_error_params(**kwargs: object) -> dict[str, object]:  # noqa: N802
    """Legacy: Create parameters for WMS API error - use FlextOracleWmsApiRequestError context instead."""
    _deprecation_warning(
        "WmsApiErrorParams", "FlextOracleWmsApiRequestError context parameter"
    )
    return {
        "status_code": kwargs.get("status_code"),
        "response_body": kwargs.get("response_body"),
        "entity_name": kwargs.get("entity_name"),
        "endpoint": kwargs.get("endpoint"),
        "method": kwargs.get("method"),
    }


# Legacy class aliases for parameter factories
WmsValidationErrorParams = wms_validation_error_params
WmsConfigurationErrorParams = wms_configuration_error_params
WmsApiErrorParams = wms_api_error_params


__all__: list[str] = [
    "WMS_DEFAULT_BATCH_SIZE",
    "WMS_DEFAULT_CACHE_TTL",
    "WMS_DEFAULT_RETRY_COUNT",
    "WMS_DEFAULT_TIMEOUT",
    "FlextOracleWmsFilterError",
    "FlextOracleWmsRateLimitError",
    "WmsApiErrorParams",
    "WmsConfigurationErrorParams",
    "WmsValidationErrorParams",
    "create_wms_client",
    "create_wms_config",
    "setup_wms_authentication",
]
