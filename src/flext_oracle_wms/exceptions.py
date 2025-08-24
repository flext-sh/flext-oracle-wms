"""Oracle WMS Exception Hierarchy - Modern Pydantic v2 Patterns.

This module provides Oracle WMS-specific exceptions using modern patterns from flext-core.
All exceptions follow the FlextErrorMixin pattern with keyword-only arguments and
modern Python 3.13 type aliases for comprehensive error handling in Oracle WMS operations.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping
from enum import Enum

from flext_core import FlextError, FlextErrorMixin


class FlextOracleWmsErrorCodes(Enum):
    """Error codes for Oracle WMS domain operations."""

    WMS_ERROR = "WMS_ERROR"
    WMS_VALIDATION_ERROR = "WMS_VALIDATION_ERROR"
    WMS_CONNECTION_ERROR = "WMS_CONNECTION_ERROR"
    WMS_AUTHENTICATION_ERROR = "WMS_AUTHENTICATION_ERROR"
    WMS_CONFIGURATION_ERROR = "WMS_CONFIGURATION_ERROR"
    WMS_API_ERROR = "WMS_API_ERROR"
    WMS_TIMEOUT_ERROR = "WMS_TIMEOUT_ERROR"
    WMS_PROCESSING_ERROR = "WMS_PROCESSING_ERROR"
    WMS_ENTITY_NOT_FOUND_ERROR = "WMS_ENTITY_NOT_FOUND_ERROR"
    WMS_SCHEMA_ERROR = "WMS_SCHEMA_ERROR"
    WMS_INVENTORY_ERROR = "WMS_INVENTORY_ERROR"
    WMS_SHIPMENT_ERROR = "WMS_SHIPMENT_ERROR"
    WMS_PICKING_ERROR = "WMS_PICKING_ERROR"


# Base Oracle WMS exception hierarchy using FlextErrorMixin pattern
class FlextOracleWmsError(FlextError, FlextErrorMixin):
    """Base Oracle WMS error."""


class FlextOracleWmsValidationError(FlextOracleWmsError):
    """Oracle WMS validation error."""


class FlextOracleWmsConnectionError(FlextOracleWmsError):
    """Oracle WMS connection error."""


class FlextOracleWmsAuthenticationError(FlextOracleWmsError):
    """Oracle WMS authentication error."""


class FlextOracleWmsConfigurationError(FlextOracleWmsError):
    """Oracle WMS configuration error."""


class FlextOracleWmsApiError(FlextOracleWmsError):
    """Oracle WMS API error."""


class FlextOracleWmsTimeoutError(FlextOracleWmsError):
    """Oracle WMS timeout error."""


class FlextOracleWmsProcessingError(FlextOracleWmsError):
    """Oracle WMS processing error."""


class FlextOracleWmsEntityNotFoundError(FlextOracleWmsError):
    """Oracle WMS entity not found error."""


class FlextOracleWmsSchemaError(FlextOracleWmsError):
    """Oracle WMS schema error."""


# Domain-specific exceptions for Oracle WMS business logic
# Using modern FlextErrorMixin pattern with context support


class FlextOracleWmsDataValidationError(FlextOracleWmsValidationError):
    """Oracle WMS data validation errors with field context."""

    def __init__(
        self,
        message: str,
        *,
        field_name: str | None = None,
        field_value: object | None = None,
        validation_rule: str | None = None,
        entity_name: str | None = None,
        code: FlextOracleWmsErrorCodes
        | None = FlextOracleWmsErrorCodes.WMS_VALIDATION_ERROR,
        context: Mapping[str, object] | None = None,
    ) -> None:
        """Initialize Oracle WMS data validation error with field context."""
        context_dict: dict[str, object] = dict(context) if context else {}
        if field_name is not None:
            context_dict["field_name"] = field_name
        if field_value is not None:
            context_dict["field_value"] = field_value
        if validation_rule is not None:
            context_dict["validation_rule"] = validation_rule
        if entity_name is not None:
            context_dict["entity_name"] = entity_name

        super().__init__(
            message,
            code=code,
            context=context_dict,
        )


class FlextOracleWmsApiRequestError(FlextOracleWmsApiError):
    """Oracle WMS API request errors with HTTP context."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        response_body: str | None = None,
        entity_name: str | None = None,
        endpoint: str | None = None,
        method: str | None = None,
        code: FlextOracleWmsErrorCodes | None = FlextOracleWmsErrorCodes.WMS_API_ERROR,
        context: Mapping[str, object] | None = None,
    ) -> None:
        """Initialize Oracle WMS API request error with HTTP context."""
        context_dict: dict[str, object] = dict(context) if context else {}
        if status_code is not None:
            context_dict["status_code"] = status_code
        if response_body is not None:
            context_dict["response_body"] = response_body[:500]  # Truncate for safety
        if entity_name is not None:
            context_dict["entity_name"] = entity_name
        if endpoint is not None:
            context_dict["endpoint"] = endpoint
        if method is not None:
            context_dict["method"] = method

        super().__init__(
            message,
            code=code,
            context=context_dict,
        )


class FlextOracleWmsConfigError(FlextOracleWmsConfigurationError):
    """Oracle WMS configuration errors with config context."""

    def __init__(
        self,
        message: str,
        *,
        config_key: str | None = None,
        config_value: object | None = None,
        config_section: str | None = None,
        valid_range: str | None = None,
        code: FlextOracleWmsErrorCodes
        | None = FlextOracleWmsErrorCodes.WMS_CONFIGURATION_ERROR,
        context: Mapping[str, object] | None = None,
    ) -> None:
        """Initialize Oracle WMS configuration error with config context."""
        context_dict: dict[str, object] = dict(context) if context else {}
        if config_key is not None:
            context_dict["config_key"] = config_key
        if config_value is not None:
            context_dict["config_value"] = config_value
        if config_section is not None:
            context_dict["config_section"] = config_section
        if valid_range is not None:
            context_dict["valid_range"] = valid_range

        super().__init__(
            message,
            code=code,
            context=context_dict,
        )


class FlextOracleWmsInventoryError(FlextOracleWmsProcessingError):
    """Oracle WMS inventory errors with WMS context."""

    def __init__(
        self,
        message: str,
        *,
        inventory_id: str | None = None,
        location_id: str | None = None,
        item_id: str | None = None,
        quantity: int | None = None,
        operation: str | None = None,
        code: FlextOracleWmsErrorCodes
        | None = FlextOracleWmsErrorCodes.WMS_INVENTORY_ERROR,
        context: Mapping[str, object] | None = None,
    ) -> None:
        """Initialize Oracle WMS inventory error with WMS context."""
        context_dict: dict[str, object] = dict(context) if context else {}
        if inventory_id is not None:
            context_dict["inventory_id"] = inventory_id
        if location_id is not None:
            context_dict["location_id"] = location_id
        if item_id is not None:
            context_dict["item_id"] = item_id
        if quantity is not None:
            context_dict["quantity"] = quantity
        if operation is not None:
            context_dict["operation"] = operation

        super().__init__(
            message,
            code=code,
            context=context_dict,
        )


class FlextOracleWmsShipmentError(FlextOracleWmsProcessingError):
    """Oracle WMS shipment errors with WMS context."""

    def __init__(
        self,
        message: str,
        *,
        shipment_id: str | None = None,
        order_id: str | None = None,
        carrier_id: str | None = None,
        tracking_number: str | None = None,
        status: str | None = None,
        code: FlextOracleWmsErrorCodes
        | None = FlextOracleWmsErrorCodes.WMS_SHIPMENT_ERROR,
        context: Mapping[str, object] | None = None,
    ) -> None:
        """Initialize Oracle WMS shipment error with WMS context."""
        context_dict: dict[str, object] = dict(context) if context else {}
        if shipment_id is not None:
            context_dict["shipment_id"] = shipment_id
        if order_id is not None:
            context_dict["order_id"] = order_id
        if carrier_id is not None:
            context_dict["carrier_id"] = carrier_id
        if tracking_number is not None:
            context_dict["tracking_number"] = tracking_number
        if status is not None:
            context_dict["status"] = status

        super().__init__(
            message,
            code=code,
            context=context_dict,
        )


class FlextOracleWmsPickingError(FlextOracleWmsProcessingError):
    """Oracle WMS picking errors with WMS context."""

    def __init__(
        self,
        message: str,
        *,
        pick_id: str | None = None,
        wave_id: str | None = None,
        task_id: str | None = None,
        location: str | None = None,
        quantity_picked: int | None = None,
        code: FlextOracleWmsErrorCodes
        | None = FlextOracleWmsErrorCodes.WMS_PICKING_ERROR,
        context: Mapping[str, object] | None = None,
    ) -> None:
        """Initialize Oracle WMS picking error with WMS context."""
        context_dict: dict[str, object] = dict(context) if context else {}
        if pick_id is not None:
            context_dict["pick_id"] = pick_id
        if wave_id is not None:
            context_dict["wave_id"] = wave_id
        if task_id is not None:
            context_dict["task_id"] = task_id
        if location is not None:
            context_dict["location"] = location
        if quantity_picked is not None:
            context_dict["quantity_picked"] = quantity_picked

        super().__init__(
            message,
            code=code,
            context=context_dict,
        )


class FlextOracleWmsSchemaFlatteningError(FlextOracleWmsSchemaError):
    """Oracle WMS schema flattening errors with schema context."""

    def __init__(
        self,
        message: str,
        *,
        schema_name: str | None = None,
        field_name: str | None = None,
        nested_path: str | None = None,
        flattening_rule: str | None = None,
        code: FlextOracleWmsErrorCodes
        | None = FlextOracleWmsErrorCodes.WMS_SCHEMA_ERROR,
        context: Mapping[str, object] | None = None,
    ) -> None:
        """Initialize Oracle WMS schema flattening error with schema context."""
        context_dict: dict[str, object] = dict(context) if context else {}
        if schema_name is not None:
            context_dict["schema_name"] = schema_name
        if field_name is not None:
            context_dict["field_name"] = field_name
        if nested_path is not None:
            context_dict["nested_path"] = nested_path
        if flattening_rule is not None:
            context_dict["flattening_rule"] = flattening_rule

        super().__init__(
            message,
            code=code,
            context=context_dict,
        )


__all__: list[str] = [
    "FlextOracleWmsApiError",
    "FlextOracleWmsApiRequestError",
    "FlextOracleWmsAuthenticationError",
    "FlextOracleWmsConfigError",
    "FlextOracleWmsConfigurationError",
    "FlextOracleWmsConnectionError",
    "FlextOracleWmsDataValidationError",
    "FlextOracleWmsEntityNotFoundError",
    "FlextOracleWmsError",
    "FlextOracleWmsErrorCodes",
    "FlextOracleWmsInventoryError",
    "FlextOracleWmsPickingError",
    "FlextOracleWmsProcessingError",
    "FlextOracleWmsSchemaError",
    "FlextOracleWmsSchemaFlatteningError",
    "FlextOracleWmsShipmentError",
    "FlextOracleWmsTimeoutError",
    "FlextOracleWmsValidationError",
]
