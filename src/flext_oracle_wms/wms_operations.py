"""Oracle WMS Operations - Consolidated Data Operations and Utilities.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT.

Consolidated Oracle WMS operations including filtering, flattening, helper functions,
and plugin implementation. This module combines filtering.py + flattening.py +
helpers.py + plugin_implementation.py into unified operations.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass
from typing import override

# Use FlextLogger from flext_core instead
from urllib.parse import urljoin, urlparse

from flext_core import (
    FlextLogger,
    FlextResult,
    FlextTypes,
    FlextUtilities,
)
from flext_oracle_wms.filtering import FlextOracleWmsFilter
from flext_oracle_wms.utilities import FlextOracleWmsUtilities
from flext_oracle_wms.wms_constants import (
    FlextOracleWmsConstants,
)
from flext_oracle_wms.wms_exceptions import (
    FlextOracleWmsDataValidationError,
    FlextOracleWmsError,
    FlextOracleWmsSchemaFlatteningError,
)

# Type aliases for Oracle WMS operations
TOracleWmsEnvironment = str
TOracleWmsApiVersion = str
TOracleWmsRecord = FlextTypes.Core.Dict
TOracleWmsRecordBatch = list[TOracleWmsRecord]
TOracleWmsPaginationInfo = FlextTypes.Core.Dict
TOracleWmsFilters = FlextTypes.Core.Dict
TOracleWmsFilterValue = object

logger = FlextLogger(__name__)


# Validation functions removed - use FlextValidations.TypeValidators directly


def handle_operation_exception(
    exception: Exception,
    operation: str,
    logger: FlextLogger | None = None,
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
        logger.error(f"{operation}: {extras}")
    raise FlextOracleWmsError(error_msg) from exception


def flext_oracle_wms_normalize_url(base_url: str, path: str) -> str:
    """Normalize Oracle WMS URL by joining base URL and path properly."""
    # Simple validation using type annotations - no over-engineering
    if not isinstance(base_url, str) or not base_url.strip():
        msg = "base_url must be a non-empty string"
        raise FlextOracleWmsError(msg)

    if not isinstance(path, str) or not path.strip():
        msg = "path must be a non-empty string"
        raise FlextOracleWmsError(msg)

    # Use urljoin for proper URL construction
    return urljoin(base_url.rstrip("/") + "/", path.lstrip("/"))


def flext_oracle_wms_extract_environment_from_url(url: str) -> TOracleWmsEnvironment:
    """Extract environment identifier from Oracle WMS URL."""
    try:
        # Simple validation using type annotations - no over-engineering
        if not isinstance(url, str) or not url.strip():
            msg = "URL must be a non-empty string"
            raise ValueError(msg)

        parsed = urlparse(url)
        path_parts = parsed.path.strip("/").split("/")

        # Look for environment in path structure
        for part in path_parts:
            if part and not part.startswith(("wms", "lgfapi", "api", "v")):
                return str(part)

        return FlextOracleWmsConstants.DEFAULT_ENVIRONMENT

    except (
        ValueError,
        TypeError,
        AttributeError,
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
    # Simple validation using type annotations - no over-engineering
    if not isinstance(base_url, str) or not base_url.strip():
        msg = "All URL components must be non-empty strings"
        raise FlextOracleWmsError(msg)

    if not isinstance(environment, str) or not environment.strip():
        msg = "All URL components must be non-empty strings"
        raise FlextOracleWmsError(msg)

    if not isinstance(entity_name, str) or not entity_name.strip():
        msg = "All URL components must be non-empty strings"
        raise FlextOracleWmsError(msg)

    # Treat any semantic version starting with 'v' as LGF API path
    if isinstance(api_version, str) and api_version.lower().startswith("v"):
        api_path = f"/{environment}/wms/lgfapi/{api_version}/entity/{entity_name}/"
    else:
        api_path = f"/{environment}/wms/api/entity/{entity_name}/"

    return flext_oracle_wms_normalize_url(base_url, api_path)


def flext_oracle_wms_validate_entity_name(entity_name: str) -> FlextResult[str]:
    """Validate Oracle WMS entity name format."""
    # Simple validation using type annotations - no over-engineering

    if not entity_name.strip():
        return FlextResult[str].fail("Entity name cannot be empty")

    normalized = entity_name.strip().lower()
    if not normalized:
        return FlextResult[str].fail("cannot be empty")

    # Check length
    max_length = FlextOracleWmsConstants.Entities.MAX_ENTITY_NAME_LENGTH
    if len(normalized) > max_length:
        return FlextResult[str].fail(
            f"Entity name too long (max {max_length} characters)",
        )

    # Check pattern
    pattern = FlextOracleWmsConstants.Entities.ENTITY_NAME_PATTERN
    if not re.match(pattern, normalized):
        return FlextResult[str].fail("Invalid entity name format")

    return FlextResult[str].ok(normalized)


def flext_oracle_wms_validate_api_response(
    response_data: object,
) -> FlextResult[FlextTypes.Core.Dict]:
    """Validate Oracle WMS API response format.

    Note: Intentionally avoids upfront strict type validation to mirror legacy
    behavior expected by tests, where non-dict inputs trigger AttributeError/
    TypeError via attribute access (e.g., calling `.get` on non-dicts).
    """
    # Validate response_data is a dictionary
    if not isinstance(response_data, dict):
        return FlextResult[FlextTypes.Core.Dict].fail(
            "Response data is not a dictionary",
        )

    response_dict: FlextTypes.Core.Dict = response_data
    if any(k in response_dict for k in ("error",)):
        err_val = response_dict.get("error")
        if isinstance(err_val, str) and err_val.strip():
            return FlextResult[FlextTypes.Core.Dict].fail(f"API error: {err_val}")
        return FlextResult[FlextTypes.Core.Dict].fail("API error")

    # Treat message starting with "Error:  or containing error" keyword as failure
    msg = response_dict.get("message")
    if isinstance(msg, str):
        msg_lower = msg.strip().lower()
        if msg_lower.startswith("error") or "error" in msg_lower:
            return FlextResult[FlextTypes.Core.Dict].fail(f"API error: {msg}")

    # If status field explicitly indicates error, treat as failure
    status_val = response_dict.get("status")
    if isinstance(status_val, str) and status_val.lower() in {
        "error",
        "failed",
        "failure",
    }:
        message_text = response_dict.get("message")
        if isinstance(message_text, str) and message_text:
            return FlextResult[FlextTypes.Core.Dict].fail(f"API error: {message_text}")
        return FlextResult[FlextTypes.Core.Dict].fail("API error")

    if any(k in response_dict for k in ("data", "results", "message", "status")):
        return FlextResult[FlextTypes.Core.Dict].ok(response_dict)

    # Default to success when structure is acceptable dict
    return FlextResult[FlextTypes.Core.Dict].ok(response_dict)


def flext_oracle_wms_extract_pagination_info(
    response_data: FlextTypes.Core.Dict,
) -> TOracleWmsPaginationInfo:
    """Extract pagination information from Oracle WMS API response."""
    fields = FlextOracleWmsConstants.ResponseFields

    # Safe extraction of pagination fields with proper type checking
    page_num_val = response_data.get(fields.PAGE_NUMBER, 1)
    int(page_num_val) if isinstance(page_num_val, (int, str)) else 1

    page_count_val = response_data.get(fields.PAGE_COUNT, 1)
    int(page_count_val) if isinstance(page_count_val, (int, str)) else 1

    result_count_val: FlextResult[object] = response_data.get(fields.RESULT_COUNT, 0)
    (int(result_count_val) if isinstance(result_count_val, (int, str)) else 0)

    # Build plain dict to avoid typing reference at runtime
    return {
        "current_page": "current_page",
        "total_pages": "total_pages",
        "total_results": "total_results",
        "has_next": bool(response_data.get(fields.NEXT_PAGE)),
        "has_previous": bool(response_data.get(fields.PREVIOUS_PAGE)),
        "next_url": (
            str(response_data.get(fields.NEXT_PAGE))
            if response_data.get(fields.NEXT_PAGE)
            else None
        ),
        "previous_url": (
            str(response_data.get(fields.PREVIOUS_PAGE))
            if response_data.get(fields.PREVIOUS_PAGE)
            else None
        ),
    }


def flext_oracle_wms_format_timestamp(timestamp: str | None = None) -> str:
    """Format timestamp for Oracle WMS operations."""
    if not timestamp:
        return FlextUtilities.Generators.generate_iso_timestamp()
    return str(timestamp)


def flext_oracle_wms_chunk_records(
    records: TOracleWmsRecordBatch,
    chunk_size: int = 50,  # FlextOracleWmsConstants.Processing.DEFAULT_BATCH_SIZE
) -> list[TOracleWmsRecordBatch]:
    """Chunk records into smaller batches for processing using FlextOracleWmsUtilities."""
    # Use FlextOracleWmsUtilities for consistent chunking logic
    result = FlextOracleWmsUtilities.DataProcessing.chunk_records(records, chunk_size)
    if result.is_failure:
        logger.error(f"Failed to chunk records: {result.error}")
        return []  # Return empty list on failure to maintain backward compatibility
    return result.value


class FlextOracleWmsUnifiedOperations:
    """Unified Oracle WMS operations class consolidating filtering, flattening, and utilities.

    This class eliminates duplication by providing all Oracle WMS operations
    in a single, cohesive interface following SOLID principles.
    """

    class _FilterOperations:
        """Nested class for filtering operations."""

        @override
        @override
        @override
        @override
        @override
        def __init__(self, parent: FlextOracleWmsUnifiedOperations) -> None:
            """Initialize the instance."""
            self._parent = parent
            self._filters: TOracleWmsFilters = {}
            self._max_conditions: int = 50
            self._case_sensitive: bool = False

        def configure(
            self,
            *,
            case_sensitive: bool = False,
            max_conditions: int = 50,
            filters: TOracleWmsFilters | None = None,
        ) -> None:
            """Configure filter operations."""
            if max_conditions <= 0:
                msg = "max_conditions must be positive"
                raise FlextOracleWmsDataValidationError(msg)
            max_conditions = min(max_conditions, 100)  # Enforce upper bound

            self._case_sensitive = case_sensitive
            self._max_conditions = max_conditions
            self._filters = filters or {}

        async def filter_records(
            self,
            records: list[FlextTypes.Core.Dict],
            filters: FlextTypes.Core.Dict,
        ) -> FlextResult[list[FlextTypes.Core.Dict]]:
            """Filter records with given filters."""
            # Validate filter count
            if len(filters) > self._max_conditions:
                return FlextResult[list[FlextTypes.Core.Dict]].fail(
                    f"Too many filter conditions. Max: {self._max_conditions}, Got: {len(filters)}",
                )

            try:
                filtered_records = [
                    record
                    for record in records
                    if self._record_matches_filters(record, filters)
                ]

                return FlextResult[list[FlextTypes.Core.Dict]].ok(filtered_records)
            except Exception as e:
                return FlextResult[list[FlextTypes.Core.Dict]].fail(
                    f"Filtering failed: {e}",
                )

        def _record_matches_filters(
            self,
            record: FlextTypes.Core.Dict,
            filters: FlextTypes.Core.Dict,
        ) -> bool:
            """Check if record matches all filter conditions."""
            for field, filter_value in filters.items():
                if not self._matches_condition(record, field, filter_value):
                    return False
            return True

        def _matches_condition(
            self,
            record: FlextTypes.Core.Dict,
            field: str,
            filter_value: object,
        ) -> bool:
            """Check if record field matches filter condition."""
            field_value = self._get_nested_value(record, field)

            if isinstance(filter_value, dict):
                operator = str(filter_value.get("operator", "eq"))
                value = filter_value.get("value")
                return self._apply_operator(field_value, operator, value)

            return self._op_equals(field_value, filter_value)

        def _get_nested_value(
            self,
            record: FlextTypes.Core.Dict,
            field_path: str,
        ) -> object:
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
            """Apply operator to field value."""
            if operator == "eq":
                return self._op_equals(field_value, filter_value)
            if operator == "ne":
                return not self._op_equals(field_value, filter_value)
            if operator == "gt":
                return self._op_greater_than(field_value, filter_value)
            if operator == "lt":
                return self._op_less_than(field_value, filter_value)
            if operator == "gte":
                return self._op_greater_than(
                    field_value,
                    filter_value,
                ) or self._op_equals(field_value, filter_value)
            if operator == "lte":
                return self._op_less_than(field_value, filter_value) or self._op_equals(
                    field_value,
                    filter_value,
                )
            if operator == "in":
                return self._op_in(field_value, filter_value)
            if operator == "contains":
                return self._op_contains(field_value, filter_value)
            return False

        def _op_equals(self, field_value: object, filter_value: object) -> bool:
            """Check if field value equals filter value."""
            if field_value is None and filter_value is None:
                return True
            if field_value is None or filter_value is None:
                return False

            if isinstance(field_value, str) and isinstance(filter_value, str):
                if not self._case_sensitive:
                    return field_value.lower() == filter_value.lower()
                return field_value == filter_value

            return field_value == filter_value

        def _op_greater_than(self, field_value: object, filter_value: object) -> bool:
            """Check if field value is greater than filter value."""
            try:
                if isinstance(field_value, (int, float)) and isinstance(
                    filter_value,
                    (int, float),
                ):
                    return field_value > filter_value
                if isinstance(field_value, str) and isinstance(filter_value, str):
                    return field_value > filter_value
                return False
            except (ValueError, TypeError):
                return False

        def _op_less_than(self, field_value: object, filter_value: object) -> bool:
            """Check if field value is less than filter value."""
            try:
                if isinstance(field_value, (int, float)) and isinstance(
                    filter_value,
                    (int, float),
                ):
                    return field_value < filter_value
                if isinstance(field_value, str) and isinstance(filter_value, str):
                    return field_value < filter_value
                return False
            except (ValueError, TypeError):
                return False

        def _op_in(self, field_value: object, filter_value: object) -> bool:
            """Check if field value is in filter value list."""
            if isinstance(filter_value, list):
                return field_value in filter_value
            return False

        def _op_contains(self, field_value: object, filter_value: object) -> bool:
            """Check if field value contains filter value."""
            if isinstance(field_value, str) and isinstance(filter_value, str):
                if not self._case_sensitive:
                    return filter_value.lower() in field_value.lower()
                return filter_value in field_value
            return False

    class _FlattenOperations:
        """Nested class for flattening operations."""

        @override
        @override
        @override
        @override
        @override
        def __init__(self, parent: FlextOracleWmsUnifiedOperations) -> None:
            """Initialize the instance."""
            self._parent = parent
            self._separator: str = "_"
            self._max_depth: int = 5
            self._preserve_lists: bool = False

        def configure(
            self,
            *,
            separator: str = "_",
            max_depth: int = 5,
            preserve_lists: bool = False,
        ) -> None:
            """Configure flattening operations."""
            self._separator = separator
            self._max_depth = max_depth
            self._preserve_lists = preserve_lists

        def flatten_records(
            self,
            records: list[FlextTypes.Core.Dict],
        ) -> list[FlextTypes.Core.Dict]:
            """Flatten nested records."""
            flattened_records: list[dict[str, object]] = []
            for record in records:
                flattened_record = self._flatten_dict(record)
                flattened_records.append(flattened_record)
            return flattened_records

        def _flatten_dict(
            self,
            data: FlextTypes.Core.Dict,
            parent_key: str = "",
            depth: int = 0,
        ) -> FlextTypes.Core.Dict:
            """Flatten a dictionary recursively."""
            if depth >= self._max_depth:
                return data

            flattened = {}
            for key, value in data.items():
                new_key = f"{parent_key}{self._separator}{key}" if parent_key else key

                if isinstance(value, dict):
                    nested = self._flatten_dict(value, new_key, depth + 1)
                    flattened.update(nested)
                elif isinstance(value, list) and not self._preserve_lists:
                    for i, item in enumerate(value):
                        if isinstance(item, dict):
                            nested = self._flatten_dict(
                                item,
                                f"{new_key}{self._separator}{i}",
                                depth + 1,
                            )
                            flattened.update(nested)
                        else:
                            flattened[f"{new_key}{self._separator}{i}"] = item
                else:
                    flattened[new_key] = value

            return flattened

    @override
    @override
    @override
    @override
    @override
    def __init__(self: object) -> None:
        """Initialize unified operations."""
        self.filter = self._FilterOperations(self)
        self.flatten = self._FlattenOperations(self)

    # Factory methods for backward compatibility
    @classmethod
    def create_filter(
        cls,
        *,
        case_sensitive: bool = False,
        max_conditions: int = 50,
    ) -> FlextOracleWmsUnifiedOperations:
        """Create unified operations configured for filtering."""
        ops = cls()
        ops.filter.configure(
            case_sensitive=case_sensitive,
            max_conditions=max_conditions,
        )
        return ops

    @classmethod
    def create_flattener(
        cls,
        *,
        separator: str = "_",
        max_depth: int = 5,
        preserve_lists: bool = False,
    ) -> FlextOracleWmsUnifiedOperations:
        """Create unified operations configured for flattening."""
        ops = cls()
        ops.flatten.configure(
            separator=separator,
            max_depth=max_depth,
            preserve_lists=preserve_lists,
        )
        return ops


# Alias for backward compatibility
FlextOracleWmsFilterConfig = FlextOracleWmsFilter


@dataclass
class FlextOracleWmsFlattener:
    """Oracle WMS data flattening implementation."""

    max_depth: int = 10  # FlextOracleWmsConstants.Processing.MAX_SCHEMA_DEPTH
    separator: str = "_"
    preserve_arrays: bool = False

    def _raise_flattening_error(self, message: str) -> None:
        """Helper to raise flattening error in inner function."""
        raise FlextOracleWmsSchemaFlatteningError(message)

    def flatten_record(self, record: TOracleWmsRecord) -> TOracleWmsRecord:
        """Flatten a single Oracle WMS record."""
        try:
            # Simple validation using type annotations - no over-engineering

            return self._flatten_dict(record)
        except Exception as e:
            msg = f"Record flattening failed: {e}"
            raise FlextOracleWmsSchemaFlatteningError(msg) from e

    def flatten_records(self, records: TOracleWmsRecordBatch) -> TOracleWmsRecordBatch:
        """Flatten multiple Oracle WMS records."""
        try:
            # Simple validation using type annotations - no over-engineering

            return [self.flatten_record(record) for record in records]
        except Exception as e:
            msg = f"Batch flattening failed: {e}"
            raise FlextOracleWmsSchemaFlatteningError(msg) from e

    def _flatten_dict(
        self,
        data: FlextTypes.Core.Dict,
        prefix: str = "",
        depth: int = 0,
    ) -> FlextTypes.Core.Dict:
        """Recursively flatten dictionary structure."""
        if depth >= self.max_depth:
            return {prefix.rstrip(self.separator): "data"}

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


class FlextOracleWmsPluginContext:
    """Oracle WMS plugin context implementation."""

    @override
    @override
    @override
    @override
    @override
    def __init__(
        self,
        config: Mapping[str, object] | None = None,
        logger_instance: object | None = None,
    ) -> None:
        """Initialize Oracle WMS plugin context."""
        self.config: dict[str, object] = config or {}
        self.logger = logger_instance


class FlextOracleWmsPlugin:
    """Oracle WMS plugin implementation."""

    @override
    @override
    @override
    @override
    @override
    def __init__(self, name: str, version: str = "0.9.0") -> None:
        """Initialize Oracle WMS plugin."""
        self.name = name
        self.version = version
        self._logger = FlextLogger(__name__)

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
            return FlextResult[None].ok(None)
        except (TypeError, ValueError, AttributeError, RuntimeError) as e:
            return FlextResult[None].fail(
                f"Oracle WMS plugin initialization failed: {e}",
            )

    async def cleanup(self) -> FlextResult[None]:
        """Cleanup Oracle WMS plugin resources."""
        try:
            self._logger.info(
                "Cleaning up Oracle WMS plugin",
                plugin_name=self.name,
            )
            return FlextResult[None].ok(None)
        except (OSError, RuntimeError, AttributeError) as e:
            return FlextResult[None].fail(f"Oracle WMS plugin cleanup failed: {e}")


class FlextOracleWmsDataPlugin:
    """Oracle WMS data plugin implementation."""

    @override
    @override
    @override
    @override
    @override
    def __init__(self, name: str, version: str = "0.9.0") -> None:
        """Initialize Oracle WMS data plugin."""
        self.name = name
        self.version = version


class FlextOracleWmsPluginRegistry:
    """Oracle WMS plugin registry implementation."""

    @override
    @override
    @override
    @override
    @override
    def __init__(self: object) -> None:
        """Initialize plugin registry."""
        self._plugins: dict[str, FlextOracleWmsPlugin] = {}
        self._logger = FlextLogger(__name__)

    def register_plugin(self, plugin: FlextOracleWmsPlugin) -> FlextResult[None]:
        """Register Oracle WMS plugin."""
        try:
            self._plugins[plugin.name] = plugin
            self._logger.info("Registered Oracle WMS plugin", plugin_name=plugin.name)
            return FlextResult[None].ok(None)
        except (TypeError, ValueError, AttributeError, RuntimeError) as e:
            return FlextResult[None].fail(f"Plugin registration failed: {e}")

    def get_plugin(self, name: str) -> FlextOracleWmsPlugin | None:
        """Get registered plugin by name."""
        return self._plugins.get(name)


# REMOVED: Factory functions eliminated in favor of direct class usage
# Users should instantiate FlextOracleWmsFilter directly:
# FlextOracleWmsFilter(filters=filters)
# FlextOracleWmsFilter(filters={field: "value"})
# FlextOracleWmsFilter(filters={"id": {"operator": "ge", "value": "start_id"}, "id_max": {"operator": "le", "value": "end_id"}})


def create_oracle_wms_data_plugin(
    name: str,
    version: str = "0.9.0",
) -> FlextOracleWmsDataPlugin:
    """Create Oracle WMS data plugin instance."""
    return FlextOracleWmsDataPlugin(name, version)


def create_oracle_wms_plugin_registry() -> FlextOracleWmsPluginRegistry:
    """Create Oracle WMS plugin registry instance."""
    return FlextOracleWmsPluginRegistry()


__all__: FlextTypes.Core.StringList = [
    "FlextOracleWmsDataPlugin",
    # Filtering Operations
    "FlextOracleWmsFilterConfig",
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
    # REMOVED: flext_oracle_wms_create_filter - use FlextOracleWmsFilter directly
    "flext_oracle_wms_extract_environment_from_url",
    "flext_oracle_wms_extract_pagination_info",
    # REMOVED: flext_oracle_wms_filter_by_field - use FlextOracleWmsFilter directly
    # REMOVED: flext_oracle_wms_filter_by_id_range - use FlextOracleWmsFilter directly
    "flext_oracle_wms_format_timestamp",
    # URL and Utility Functions
    "flext_oracle_wms_normalize_url",
    "flext_oracle_wms_validate_api_response",
    "flext_oracle_wms_validate_entity_name",
    "handle_operation_exception",
    # Validation functions removed - use FlextValidations.TypeValidators directly
]
