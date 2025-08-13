"""Oracle WMS Operations - Consolidated Data Operations and Utilities.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Consolidated Oracle WMS operations including filtering, flattening, helper functions,
and plugin implementation. This module combines filtering.py + flattening.py +
helpers.py + plugin_implementation.py into unified operations.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import TYPE_CHECKING
from urllib.parse import urljoin, urlparse

from flext_core import (
    FlextResult,
    get_logger,
)

from flext_oracle_wms.wms_constants import (
    FlextOracleWmsDefaults,
    FlextOracleWmsResponseFields,
    OracleWMSFilterOperator,
)
from flext_oracle_wms.wms_exceptions import (
    FlextOracleWmsDataValidationError,
    FlextOracleWmsError,
    FlextOracleWmsSchemaFlatteningError,
)
from flext_oracle_wms.wms_models import (
    TOracleWmsFilters,
    TOracleWmsFilterValue,
    TOracleWmsPaginationInfo,
    TOracleWmsRecord,
    TOracleWmsRecordBatch,
)

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping
    from logging import Logger

    from flext_core.loggings import FlextLogger

    from flext_oracle_wms.wms_models import (
        TOracleWmsApiVersion,
        TOracleWmsEnvironment,
    )

logger = get_logger(__name__)


# =============================================================================
# DRY VALIDATION FUNCTIONS - Consolidated from helpers.py
# =============================================================================


def validate_records_list(records: object, field_name: str = "records") -> None:
    """DRY function to validate records parameter is a list."""
    if not isinstance(records, list):
        pretty = field_name.capitalize()
        msg = f"{pretty} must be a list"
        raise FlextOracleWmsDataValidationError(msg)


def validate_dict_parameter(param: object, field_name: str) -> None:
    """DRY function to validate parameter is a dict."""
    if not isinstance(param, dict):
        pretty = field_name.capitalize()
        msg = f"{pretty} must be a dictionary"
        raise FlextOracleWmsDataValidationError(msg)


def validate_string_parameter(
    param: object,
    field_name: str,
    allow_empty: bool = False,  # noqa: FBT001, FBT002
) -> None:
    """DRY function to validate string parameter."""
    if not isinstance(param, str):
        pretty = field_name.capitalize()
        msg = f"{pretty} must be a string"
        raise FlextOracleWmsDataValidationError(msg)

    if not allow_empty and not param.strip():
        pretty = field_name.capitalize()
        msg = f"{pretty} must be a non-empty string"
        raise FlextOracleWmsDataValidationError(msg)


def handle_operation_exception(
    operation: str,
    exception: Exception,
    logger: FlextLogger | Logger | None = None,
    **context: object,
) -> None:
    """DRY function for handling operations exceptions.

    For legacy compatibility, this function raises a FlextOracleWmsError
    and chains the original exception as the cause.
    """
    error_msg = f"{operation} failed: {exception}"
    if logger is not None:
        # Compatibilidade com asserções: args[1] deve conter a operação, args[2] os extras
        extras = ", ".join(f"{k}={v}" for k, v in context.items()) if context else ""
        logger.error("%s", operation, extras)
    raise FlextOracleWmsError(error_msg) from exception


# =============================================================================
# URL AND UTILITY FUNCTIONS - Consolidated from helpers.py
# =============================================================================


def flext_oracle_wms_normalize_url(base_url: str, path: str) -> str:
    """Normalize Oracle WMS URL by joining base URL and path properly."""
    try:
        validate_string_parameter(base_url, "base_url")
        validate_string_parameter(path, "path")
    except FlextOracleWmsDataValidationError as e:
        # Legacy tests expect base OracleWmsError
        raise FlextOracleWmsError(str(e)) from e

    # Use urljoin for proper URL construction
    return urljoin(base_url.rstrip("/") + "/", path.lstrip("/"))


def flext_oracle_wms_extract_environment_from_url(url: str) -> TOracleWmsEnvironment:
    """Extract environment identifier from Oracle WMS URL."""
    try:
        validate_string_parameter(url, "url")
        parsed = urlparse(url)
        path_parts = parsed.path.strip("/").split("/")

        # Look for environment in path structure
        for part in path_parts:
            if part and not part.startswith(("wms", "lgfapi", "api", "v")):
                return str(part)

        return "default"

    except (
        ValueError,
        TypeError,
        AttributeError,
        FlextOracleWmsDataValidationError,
    ) as e:
        # Legacy behavior: raise base error
        error_message = f"Invalid URL for environment extraction: {url}"
        raise FlextOracleWmsError(error_message) from e


def flext_oracle_wms_build_entity_url(
    base_url: str,
    environment: str,
    entity_name: str,
    api_version: TOracleWmsApiVersion = "v10",
) -> str:
    """Build complete entity URL for Oracle WMS API calls."""
    try:
        validate_string_parameter(base_url, "base_url")
        validate_string_parameter(environment, "environment")
        validate_string_parameter(entity_name, "entity_name")

        if api_version == "v10":
            api_path = f"/{environment}/wms/lgfapi/v10/entity/{entity_name}/"
        else:
            api_path = f"/{environment}/wms/api/entity/{entity_name}/"

        return flext_oracle_wms_normalize_url(base_url, api_path)

    except FlextOracleWmsDataValidationError as e:
        raise FlextOracleWmsError(str(e)) from e


def flext_oracle_wms_validate_entity_name(entity_name: str) -> FlextResult[str]:
    """Validate Oracle WMS entity name format."""
    try:
        validate_string_parameter(entity_name, "entity_name")
        normalized = entity_name.strip().lower()
        if not normalized:
            return FlextResult.fail("cannot be empty")

        # Check length
        max_length = FlextOracleWmsDefaults.MAX_ENTITY_NAME_LENGTH
        if len(normalized) > max_length:
            return FlextResult.fail(
                f"Entity name too long (max {max_length} characters)",
            )

        # Check pattern
        pattern = FlextOracleWmsDefaults.ENTITY_NAME_PATTERN
        if not re.match(pattern, normalized):
            return FlextResult.fail("Invalid entity name format")

        return FlextResult.ok(normalized)

    except FlextOracleWmsDataValidationError as e:
        return FlextResult.fail(str(e))


def flext_oracle_wms_validate_api_response(
    response_data: dict[str, object],
) -> FlextResult[dict[str, object]]:
    """Validate Oracle WMS API response format."""
    try:
        validate_dict_parameter(response_data, "response_data")

        # Consider common success formats: data/results/message/status
        if not response_data:
            return FlextResult.fail("API response is empty")
        if any(k in response_data for k in ("error",)):
            return FlextResult.fail("API error present in response")
        if any(k in response_data for k in ("data", "results", "message", "status")):
            return FlextResult.ok(response_data)

        # Default to success when structure is acceptable dict
        return FlextResult.ok(response_data)

    except FlextOracleWmsDataValidationError as e:
        return FlextResult.fail(str(e))


def flext_oracle_wms_extract_pagination_info(
    response_data: dict[str, object],
) -> TOracleWmsPaginationInfo:
    """Extract pagination information from Oracle WMS API response."""
    fields = FlextOracleWmsResponseFields

    # Safe extraction of pagination fields with proper type checking
    page_num_val = response_data.get(fields.PAGE_NUMBER, 1)
    current_page = int(page_num_val) if isinstance(page_num_val, (int, str)) else 1

    page_count_val = response_data.get(fields.PAGE_COUNT, 1)
    total_pages = int(page_count_val) if isinstance(page_count_val, (int, str)) else 1

    result_count_val = response_data.get(fields.RESULT_COUNT, 0)
    total_results = (
        int(result_count_val) if isinstance(result_count_val, (int, str)) else 0
    )

    return TOracleWmsPaginationInfo(
        current_page=current_page,
        total_pages=total_pages,
        total_results=total_results,
        has_next=bool(response_data.get(fields.NEXT_PAGE)),
        has_previous=bool(response_data.get(fields.PREVIOUS_PAGE)),
        next_url=str(response_data.get(fields.NEXT_PAGE))
        if response_data.get(fields.NEXT_PAGE)
        else None,
        previous_url=str(response_data.get(fields.PREVIOUS_PAGE))
        if response_data.get(fields.PREVIOUS_PAGE)
        else None,
    )


def flext_oracle_wms_format_timestamp(timestamp: str | None = None) -> str:
    """Format timestamp for Oracle WMS operations."""
    if not timestamp:
        return datetime.now(UTC).isoformat()
    return str(timestamp)


def flext_oracle_wms_chunk_records(
    records: TOracleWmsRecordBatch,
    chunk_size: int = 50,  # FlextOracleWmsDefaults.DEFAULT_BATCH_SIZE
) -> list[TOracleWmsRecordBatch]:
    """Chunk records into smaller batches for processing."""

    def _validate_chunk_size(size: int) -> None:
        """Validate chunk size is within acceptable range."""
        if size <= 0 or size > FlextOracleWmsDefaults.MAX_BATCH_SIZE:
            error_message = "Chunk size must be within valid range"
            raise FlextOracleWmsDataValidationError(error_message)

    try:
        validate_records_list(records, "records")
        _validate_chunk_size(chunk_size)
        return [records[i : i + chunk_size] for i in range(0, len(records), chunk_size)]

    except FlextOracleWmsDataValidationError as e:
        raise FlextOracleWmsError(str(e)) from e


# =============================================================================
# FILTERING OPERATIONS - Consolidated from filtering.py
# =============================================================================


@dataclass
class FlextOracleWmsFilter:
    """Oracle WMS advanced filtering implementation."""

    filters: TOracleWmsFilters
    max_conditions: int = 50  # FlextOracleWmsDefaults.MAX_FILTER_CONDITIONS

    def __post_init__(self) -> None:
        """Validate filter conditions after initialization."""
        self._validate_filter_conditions_count()

    def _validate_filter_conditions_count(self) -> None:
        """Validate that filter conditions don't exceed maximum."""
        if len(self.filters) > self.max_conditions:
            msg = f"Too many filter conditions. Max: {self.max_conditions}, Got: {len(self.filters)}"
            raise FlextOracleWmsDataValidationError(msg)

    async def filter_records(
        self,
        records: TOracleWmsRecordBatch,
    ) -> TOracleWmsRecordBatch:
        """Apply filters to records."""
        try:
            validate_records_list(records, "records")
            return self._apply_record_filters(records)
        except FlextOracleWmsDataValidationError as e:
            logger.exception("Record filtering failed", extra={"error": str(e)})
            return []

    def _apply_record_filters(
        self,
        records: TOracleWmsRecordBatch,
    ) -> TOracleWmsRecordBatch:
        """Apply all filter conditions to records."""
        if not self.filters:
            return records

        return [record for record in records if self._record_matches_filters(record)]

    def _record_matches_filters(self, record: TOracleWmsRecord) -> bool:
        """Check if record matches all filter conditions."""
        for field, filter_value in self.filters.items():
            if not self._matches_condition(record, field, filter_value):
                return False
        return True

    def _matches_condition(
        self,
        record: TOracleWmsRecord,
        field: str,
        filter_value: TOracleWmsFilterValue,
    ) -> bool:
        """Check if record field matches filter condition."""
        field_value = self._get_nested_value(record, field)

        # Handle different filter value types
        if isinstance(filter_value, dict):
            # Advanced filter with operator
            operator = str(filter_value.get("operator", "eq"))
            value = filter_value.get("value")
            return self._apply_operator(field_value, operator, value)
        # Simple equality check
        return self._op_equals(field_value, filter_value)

    def _get_nested_value(self, record: TOracleWmsRecord, field_path: str) -> object:
        """Get nested field value from record using dot notation."""
        try:
            value: object = record
            for field_part in field_path.split("."):
                if isinstance(value, dict):
                    value = value.get(field_part)
                else:
                    return None
            return value
        except (AttributeError, KeyError, TypeError):
            return None

    def _apply_operator(
        self,
        field_value: object,
        operator: str,
        filter_value: object,
    ) -> bool:
        """Apply filter operator to field value."""
        operator_map: dict[str, Callable[[object, object], bool]] = {
            OracleWMSFilterOperator.EQ: self._op_equals,
            OracleWMSFilterOperator.NE: self._op_not_equals,
            OracleWMSFilterOperator.GT: self._op_greater_than,
            OracleWMSFilterOperator.GE: self._op_greater_equal,
            OracleWMSFilterOperator.LT: self._op_less_than,
            OracleWMSFilterOperator.LE: self._op_less_equal,
            OracleWMSFilterOperator.IN: self._op_in,
            OracleWMSFilterOperator.NOT_IN: self._op_not_in,
            OracleWMSFilterOperator.LIKE: self._op_like,
            OracleWMSFilterOperator.NOT_LIKE: self._op_not_like,
        }

        op_func = operator_map.get(operator, self._op_equals)
        return bool(op_func(field_value, filter_value))

    def _op_equals(self, field_value: object, filter_value: object) -> bool:
        """Equality operator."""
        return self._normalize_for_comparison(
            field_value,
        ) == self._normalize_for_comparison(filter_value)

    def _op_not_equals(self, field_value: object, filter_value: object) -> bool:
        """Not equals operator."""
        return not self._op_equals(field_value, filter_value)

    def _op_greater_than(self, field_value: object, filter_value: object) -> bool:
        """Greater than operator."""
        try:
            return field_value > filter_value  # type: ignore[operator,no-any-return]
        except (TypeError, ValueError):
            return False

    def _op_greater_equal(self, field_value: object, filter_value: object) -> bool:
        """Greater than or equal operator."""
        try:
            return field_value >= filter_value  # type: ignore[operator,no-any-return]
        except (TypeError, ValueError):
            return False

    def _op_less_than(self, field_value: object, filter_value: object) -> bool:
        """Less than operator."""
        try:
            return field_value < filter_value  # type: ignore[operator,no-any-return]
        except (TypeError, ValueError):
            return False

    def _op_less_equal(self, field_value: object, filter_value: object) -> bool:
        """Less than or equal operator."""
        try:
            return field_value <= filter_value  # type: ignore[operator,no-any-return]
        except (TypeError, ValueError):
            return False

    def _op_in(self, field_value: object, filter_value: object) -> bool:
        """In operator."""
        if isinstance(filter_value, (list, tuple)):
            return field_value in filter_value
        return False

    def _op_not_in(self, field_value: object, filter_value: object) -> bool:
        """Not in operator."""
        return not self._op_in(field_value, filter_value)

    def _op_like(self, field_value: object, filter_value: object) -> bool:
        """Like operator (SQL-style pattern matching)."""
        if not isinstance(field_value, str) or not isinstance(filter_value, str):
            return False

        # Convert SQL LIKE pattern to regex
        pattern = filter_value.replace("%", ".*").replace("_", ".")
        try:
            return bool(re.match(pattern, field_value, re.IGNORECASE))
        except re.error:
            return False

    def _op_not_like(self, field_value: object, filter_value: object) -> bool:
        """Not like operator."""
        return not self._op_like(field_value, filter_value)

    def _normalize_for_comparison(self, value: object) -> object:
        """Normalize value for comparison operations."""
        if isinstance(value, str):
            return value.lower().strip()
        return value


# =============================================================================
# DATA FLATTENING OPERATIONS - Consolidated from flattening.py
# =============================================================================


@dataclass
class FlextOracleWmsFlattener:
    """Oracle WMS data flattening implementation."""

    max_depth: int = 10  # FlextOracleWmsDefaults.MAX_SCHEMA_DEPTH
    separator: str = "__"
    preserve_arrays: bool = False

    def flatten_record(self, record: TOracleWmsRecord) -> TOracleWmsRecord:
        """Flatten a single Oracle WMS record."""
        try:
            validate_dict_parameter(record, "record")
            return self._flatten_dict(record)
        except (FlextOracleWmsDataValidationError, Exception) as e:
            msg = f"Record flattening failed: {e}"
            raise FlextOracleWmsSchemaFlatteningError(msg) from e

    def flatten_records(self, records: TOracleWmsRecordBatch) -> TOracleWmsRecordBatch:
        """Flatten multiple Oracle WMS records."""
        try:
            validate_records_list(records, "records")
            return [self.flatten_record(record) for record in records]
        except (FlextOracleWmsDataValidationError, Exception) as e:
            msg = f"Batch flattening failed: {e}"
            raise FlextOracleWmsSchemaFlatteningError(msg) from e

    def _flatten_dict(
        self,
        data: dict[str, object],
        prefix: str = "",
        depth: int = 0,
    ) -> dict[str, object]:
        """Recursively flatten dictionary structure."""
        if depth >= self.max_depth:
            return {prefix.rstrip(self.separator): data}

        result = {}
        for key, value in data.items():
            new_key = (
                f"{prefix}{key}" if not prefix else f"{prefix}{self.separator}{key}"
            )

            if isinstance(value, dict):
                result.update(
                    self._flatten_dict(value, new_key + self.separator, depth + 1),
                )
            elif isinstance(value, list) and not self.preserve_arrays:
                for i, item in enumerate(value):
                    array_key = f"{new_key}{self.separator}{i}"
                    if isinstance(item, dict):
                        result.update(
                            self._flatten_dict(
                                item,
                                array_key + self.separator,
                                depth + 1,
                            ),
                        )
                    else:
                        result[array_key] = item
            else:
                result[new_key] = value

        return result


# =============================================================================
# PLUGIN IMPLEMENTATION - Consolidated from plugin_implementation.py
# =============================================================================


class FlextOracleWmsPluginContext:
    """Oracle WMS plugin context implementation."""

    def __init__(
        self,
        config: Mapping[str, object] | None = None,
        logger_instance: object | None = None,
    ) -> None:
        """Initialize Oracle WMS plugin context."""
        self.config = config or {}
        self.logger = logger_instance


class FlextOracleWmsPlugin:
    """Oracle WMS plugin implementation."""

    def __init__(self, name: str, version: str = "0.9.0") -> None:
        """Initialize Oracle WMS plugin."""
        self.name = name
        self.version = version
        self._logger = get_logger(__name__)

    async def initialize(
        self,
        context: FlextOracleWmsPluginContext,
    ) -> FlextResult[None]:
        """Initialize Oracle WMS plugin with context."""
        try:
            # Use context minimally (e.g., to record if a logger was provided)
            has_external_logger = bool(getattr(context, "logger", None))
            self._logger.info(
                "Initializing Oracle WMS plugin",
                plugin_name=self.name,
                has_external_logger=has_external_logger,
            )
            return FlextResult.ok(None)
        except (TypeError, ValueError, AttributeError, RuntimeError) as e:
            return FlextResult.fail(f"Oracle WMS plugin initialization failed: {e}")

    async def cleanup(self) -> FlextResult[None]:
        """Cleanup Oracle WMS plugin resources."""
        try:
            self._logger.info(
                "Cleaning up Oracle WMS plugin",
                plugin_name=self.name,
            )
            return FlextResult.ok(None)
        except (OSError, RuntimeError, AttributeError) as e:
            return FlextResult.fail(f"Oracle WMS plugin cleanup failed: {e}")


class FlextOracleWmsDataPlugin:
    """Oracle WMS data plugin implementation."""

    def __init__(self, name: str, version: str = "0.9.0") -> None:
        """Initialize Oracle WMS data plugin."""
        self.name = name
        self.version = version


class FlextOracleWmsPluginRegistry:
    """Oracle WMS plugin registry implementation."""

    def __init__(self) -> None:
        """Initialize plugin registry."""
        self._plugins: dict[str, FlextOracleWmsPlugin] = {}
        self._logger = get_logger(__name__)

    def register_plugin(self, plugin: FlextOracleWmsPlugin) -> FlextResult[None]:
        """Register Oracle WMS plugin."""
        try:
            self._plugins[plugin.name] = plugin
            self._logger.info("Registered Oracle WMS plugin", plugin_name=plugin.name)
            return FlextResult.ok(None)
        except (TypeError, ValueError, AttributeError, RuntimeError) as e:
            return FlextResult.fail(f"Plugin registration failed: {e}")

    def get_plugin(self, name: str) -> FlextOracleWmsPlugin | None:
        """Get registered plugin by name."""
        return self._plugins.get(name)


# =============================================================================
# FACTORY FUNCTIONS - Convenient creation functions
# =============================================================================


def flext_oracle_wms_create_filter(filters: TOracleWmsFilters) -> FlextOracleWmsFilter:
    """Create Oracle WMS filter instance."""
    return FlextOracleWmsFilter(filters=filters)


def flext_oracle_wms_filter_by_field(
    field: str,
    value: TOracleWmsFilterValue,
) -> FlextOracleWmsFilter:
    """Create simple field filter."""
    return FlextOracleWmsFilter(filters={field: value})


def flext_oracle_wms_filter_by_id_range(
    start_id: int,
    end_id: int,
) -> FlextOracleWmsFilter:
    """Create ID range filter."""
    return FlextOracleWmsFilter(
        filters={
            "id": {"operator": "ge", "value": start_id},
            "id_max": {"operator": "le", "value": end_id},
        },
    )


def create_oracle_wms_data_plugin(
    name: str,
    version: str = "0.9.0",
) -> FlextOracleWmsDataPlugin:
    """Create Oracle WMS data plugin instance."""
    return FlextOracleWmsDataPlugin(name, version)


def create_oracle_wms_plugin_registry() -> FlextOracleWmsPluginRegistry:
    """Create Oracle WMS plugin registry instance."""
    return FlextOracleWmsPluginRegistry()


# =============================================================================
# EXPORTS
# =============================================================================

__all__: list[str] = [
    "FlextOracleWmsDataPlugin",
    # Filtering Operations
    "FlextOracleWmsFilter",
    # Data Flattening
    "FlextOracleWmsFlattener",
    # Plugin Implementation
    "FlextOracleWmsPlugin",
    "FlextOracleWmsPluginContext",
    "FlextOracleWmsPluginRegistry",
    "create_oracle_wms_data_plugin",
    "create_oracle_wms_plugin_registry",
    "flext_oracle_wms_build_entity_url",
    "flext_oracle_wms_chunk_records",
    "flext_oracle_wms_create_filter",
    "flext_oracle_wms_extract_environment_from_url",
    "flext_oracle_wms_extract_pagination_info",
    "flext_oracle_wms_filter_by_field",
    "flext_oracle_wms_filter_by_id_range",
    "flext_oracle_wms_format_timestamp",
    # URL and Utility Functions
    "flext_oracle_wms_normalize_url",
    "flext_oracle_wms_validate_api_response",
    "flext_oracle_wms_validate_entity_name",
    "handle_operation_exception",
    "validate_dict_parameter",
    # Validation Functions
    "validate_records_list",
    "validate_string_parameter",
]
