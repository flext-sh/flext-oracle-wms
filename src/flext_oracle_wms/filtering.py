"""Oracle WMS Filtering - Essential filtering capabilities using flext-core patterns.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Simplified but powerful filtering for Oracle WMS records.
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from flext_core import FlextResult, get_logger

from flext_oracle_wms.constants import (
    FlextOracleWmsDefaults,
    OracleWMSFilterOperator,
)
from flext_oracle_wms.exceptions import (
    FlextOracleWmsDataValidationError,
    FlextOracleWmsError,
)
from flext_oracle_wms.helpers import (
    handle_operation_exception,
    validate_dict_parameter,
    validate_records_list,
    validate_string_parameter,
)

if TYPE_CHECKING:
    from flext_oracle_wms.types import (
        TOracleWmsFilters,
        TOracleWmsRecord,
        TOracleWmsRecordBatch,
    )

logger = get_logger(__name__)


class FlextOracleWmsFilter:
    """Simplified Oracle WMS filtering engine using flext-core patterns."""

    def __init__(
        self,
        *,
        case_sensitive: bool = False,
        max_conditions: int = FlextOracleWmsDefaults.MAX_FILTER_CONDITIONS,
    ) -> None:
        """Initialize filter with basic configuration.

        Args:
            case_sensitive: Whether string comparisons are case sensitive
            max_conditions: Maximum number of filter conditions allowed

        Raises:
            FlextOracleWmsError: If configuration is invalid

        """
        if max_conditions <= 0:
            msg = "Max conditions must be positive"
            raise FlextOracleWmsError(msg)

        if max_conditions > FlextOracleWmsDefaults.MAX_FILTER_CONDITIONS:
            max_conditions_limit = FlextOracleWmsDefaults.MAX_FILTER_CONDITIONS
            msg = f"Max conditions cannot exceed {max_conditions_limit}"
            raise FlextOracleWmsError(msg)

        self.case_sensitive = case_sensitive
        self.max_conditions = max_conditions

        # Operator implementations
        self._operators = {
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

    def _validate_filter_conditions_count(
        self,
        filters: TOracleWmsFilters,
    ) -> FlextResult[None]:
        """Validate filter conditions count - DRY counting approach."""
        total_conditions = 0
        for conditions in filters.values():
            if isinstance(conditions, list):
                total_conditions += len(conditions)
            else:
                # Single condition (str, int, float, bool)
                total_conditions += 1

        if total_conditions > self.max_conditions:
            error_msg = (
                f"Too many filter conditions: {total_conditions} > "
                f"{self.max_conditions}"
            )
            return FlextResult.fail(error_msg)
        return FlextResult.ok(None)

    def _apply_record_filters(
        self,
        records: TOracleWmsRecordBatch,
        filters: TOracleWmsFilters,
    ) -> list[TOracleWmsRecord]:
        """Apply filters to records."""
        return [
            record
            for record in records
            if self._record_matches_filters(record, filters)
        ]

    def _record_matches_filters(
        self,
        record: TOracleWmsRecord,
        filters: TOracleWmsFilters,
    ) -> bool:
        """Check if record matches all filters - DRY approach with proper types."""
        for field_name, conditions in filters.items():
            field_value = self._get_nested_value(record, field_name)

            if isinstance(conditions, list):
                # List of values - check if field_value is in the list
                if field_value not in conditions:
                    return False
            # Single value - direct comparison
            elif not self._op_equals(field_value, conditions):
                return False
        return True

    def _matches_condition(
        self,
        field_value: object,
        conditions: dict[str, object],
    ) -> bool:
        """Check if field value matches condition operators - DRY approach."""
        for operator_str, filter_value in conditions.items():
            # Convert string to enum using DRY approach
            try:
                operator_enum = OracleWMSFilterOperator(operator_str)
            except ValueError:
                # Unknown operator, skip it
                continue

            if operator_enum not in self._operators:
                continue

            operator_func = self._operators[operator_enum]
            if not operator_func(field_value, filter_value):
                return False
        return True

    async def filter_records(
        self,
        records: TOracleWmsRecordBatch,
        filters: TOracleWmsFilters,
        limit: int | None = None,
    ) -> FlextResult[TOracleWmsRecordBatch]:
        """Filter records using conditions.

        Args:
            records: Records to filter
            filters: Filter conditions
            limit: Maximum number of results

        Returns:
            FlextResult with filtered records

        Raises:
            FlextOracleWmsDataValidationError: If filter data is invalid

        """
        try:
            # Validate input parameters using DRY functions
            validate_records_list(records, "records")
            validate_dict_parameter(filters, "filters")

            # Handle empty filters case
            if not filters:
                limited_records = records[:limit] if limit else records
                return FlextResult.ok(limited_records)

            # Validate filter conditions count using helper method
            validation_result = self._validate_filter_conditions_count(filters)
            if not validation_result.is_success:
                # Cast to proper return type since validation returns FlextResult[None]
                return FlextResult.fail(validation_result.error or "Validation failed")

            # Apply filters using helper method
            filtered_records = self._apply_record_filters(records, filters)

            # Apply limit if specified
            if limit and len(filtered_records) > limit:
                filtered_records = filtered_records[:limit]

            logger.debug(
                "Filtering completed",
                original_count=len(records),
                filtered_count=len(filtered_records),
            )

            return FlextResult.ok(filtered_records)

        except FlextOracleWmsDataValidationError:
            raise
        except Exception as e:
            handle_operation_exception(e, "filter records")
            # Never reached due to handle_operation_exception always raising
            return FlextResult.fail(f"Filter records failed: {e}")

    async def sort_records(
        self,
        records: TOracleWmsRecordBatch,
        sort_field: str,
        *,
        ascending: bool = True,
    ) -> FlextResult[TOracleWmsRecordBatch]:
        """Sort records by field.

        Args:
            records: Records to sort
            sort_field: Field to sort by
            ascending: Sort direction

        Returns:
            FlextResult with sorted records

        Raises:
            FlextOracleWmsDataValidationError: If sort parameters are invalid

        """
        try:
            # Validate input parameters using DRY functions
            validate_records_list(records, "records")
            validate_string_parameter(sort_field, "sort field")

            def get_sort_value(record: TOracleWmsRecord) -> str | int | float:
                value = self._get_nested_value(record, sort_field)
                # Handle None values
                if value is None:
                    return "" if ascending else "zzz"
                # Convert to comparable type
                if isinstance(value, (str, int, float)):
                    return value
                return str(value)

            sorted_records = sorted(
                records,
                key=get_sort_value,
                reverse=not ascending,
            )

            logger.debug(
                "Sorting completed",
                record_count=len(records),
                sort_field=sort_field,
                ascending=ascending,
            )

            return FlextResult.ok(sorted_records)

        except FlextOracleWmsDataValidationError:
            raise
        except Exception as e:
            handle_operation_exception(e, "sort records")
            # Never reached due to handle_operation_exception always raising
            return FlextResult.fail(f"Sort records failed: {e}")

    def _get_nested_value(self, record: TOracleWmsRecord, field_path: str) -> object:
        """Get value from nested field path using dot notation."""
        if "." not in field_path:
            return record.get(field_path)

        current_value: object = record
        for field_part in field_path.split("."):
            if isinstance(current_value, dict):
                current_value = current_value.get(field_part)
                if current_value is None:
                    return None
            else:
                return None

        return current_value

    def _normalize_for_comparison(self, value: object) -> object:
        """Normalize value for case-insensitive comparison."""
        if not self.case_sensitive and isinstance(value, str):
            return value.lower()
        return value

    # Operator implementations
    def _op_equals(self, field_value: object, filter_value: object) -> bool:
        """Equality operator."""
        return self._normalize_for_comparison(
            field_value,
        ) == self._normalize_for_comparison(filter_value)

    def _op_not_equals(self, field_value: object, filter_value: object) -> bool:
        """Not equals operator."""
        return self._normalize_for_comparison(
            field_value,
        ) != self._normalize_for_comparison(filter_value)

    def _op_greater_than(self, field_value: object, filter_value: object) -> bool:
        """Greater than operator with proper type safety."""
        try:
            # Type guard for numeric comparisons
            if isinstance(field_value, (int, float)) and isinstance(
                filter_value, (int, float)
            ):
                return field_value > filter_value
            # Type guard for string comparisons
            if isinstance(field_value, str) and isinstance(filter_value, str):
                return field_value > filter_value
            return False
        except (TypeError, ValueError):
            return False

    def _op_greater_equal(self, field_value: object, filter_value: object) -> bool:
        """Greater than or equal operator with proper type safety."""
        try:
            # Type guard for numeric comparisons
            if isinstance(field_value, (int, float)) and isinstance(
                filter_value, (int, float)
            ):
                return field_value >= filter_value
            # Type guard for string comparisons
            if isinstance(field_value, str) and isinstance(filter_value, str):
                return field_value >= filter_value
            return False
        except (TypeError, ValueError):
            return False

    def _op_less_than(self, field_value: object, filter_value: object) -> bool:
        """Less than operator with proper type safety."""
        try:
            # Type guard for numeric comparisons
            if isinstance(field_value, (int, float)) and isinstance(
                filter_value, (int, float)
            ):
                return field_value < filter_value
            # Type guard for string comparisons
            if isinstance(field_value, str) and isinstance(filter_value, str):
                return field_value < filter_value
            return False
        except (TypeError, ValueError):
            return False

    def _op_less_equal(self, field_value: object, filter_value: object) -> bool:
        """Less than or equal operator with proper type safety."""
        try:
            # Type guard for numeric comparisons
            if isinstance(field_value, (int, float)) and isinstance(
                filter_value, (int, float)
            ):
                return field_value <= filter_value
            # Type guard for string comparisons
            if isinstance(field_value, str) and isinstance(filter_value, str):
                return field_value <= filter_value
            return False
        except (TypeError, ValueError):
            return False

    def _op_in(self, field_value: object, filter_value: object) -> bool:
        """In operator (value in list)."""
        if not isinstance(filter_value, (list, tuple, set)):
            return False

        normalized_field = self._normalize_for_comparison(field_value)
        normalized_list = [self._normalize_for_comparison(v) for v in filter_value]
        return normalized_field in normalized_list

    def _op_not_in(self, field_value: object, filter_value: object) -> bool:
        """Not in operator (value not in list)."""
        return not self._op_in(field_value, filter_value)

    def _op_like(self, field_value: object, filter_value: object) -> bool:
        """Like operator (pattern matching)."""
        if not isinstance(field_value, str) or not isinstance(filter_value, str):
            return False

        field_str = str(self._normalize_for_comparison(field_value))
        pattern_str = str(self._normalize_for_comparison(filter_value))

        # Convert SQL LIKE pattern to regex
        pattern = pattern_str.replace("%", ".*").replace("_", ".")

        flags = 0 if self.case_sensitive else re.IGNORECASE
        return bool(re.search(pattern, field_str, flags))

    def _op_not_like(self, field_value: object, filter_value: object) -> bool:
        """Not like operator."""
        return not self._op_like(field_value, filter_value)


# Factory function
def flext_oracle_wms_create_filter(
    *,
    case_sensitive: bool = False,
    max_conditions: int = FlextOracleWmsDefaults.MAX_FILTER_CONDITIONS,
) -> FlextOracleWmsFilter:
    """Create Oracle WMS filter.

    Args:
        case_sensitive: Whether comparisons are case sensitive
        max_conditions: Maximum number of filter conditions

    Returns:
        Configured filter instance

    Raises:
        FlextOracleWmsError: If configuration is invalid

    """
    if max_conditions <= 0:
        msg = "Max conditions must be positive"
        raise FlextOracleWmsError(msg)

    if max_conditions > FlextOracleWmsDefaults.MAX_FILTER_CONDITIONS:
        max_limit = FlextOracleWmsDefaults.MAX_FILTER_CONDITIONS
        msg = f"Max conditions cannot exceed {max_limit}"
        raise FlextOracleWmsError(msg)

    return FlextOracleWmsFilter(
        case_sensitive=case_sensitive,
        max_conditions=max_conditions,
    )


# Convenience functions
async def flext_oracle_wms_filter_by_field(
    records: TOracleWmsRecordBatch,
    field: str,
    value: object,
    operator: OracleWMSFilterOperator = OracleWMSFilterOperator.EQ,
) -> FlextResult[TOracleWmsRecordBatch]:
    """Filter records by single field condition.

    Args:
        records: Records to filter
        field: Field name
        value: Filter value
        operator: Filter operator

    Returns:
        FlextResult with filtered records

    Raises:
        FlextOracleWmsDataValidationError: If filter data is invalid

    """
    try:
        filter_engine = flext_oracle_wms_create_filter()
        # For simple equality, use direct value with proper type casting
        if operator == OracleWMSFilterOperator.EQ:
            # Ensure value is compatible with TOracleWmsFilterValue
            filter_value: str | int | float | bool | list[str | int | float]
            if isinstance(value, (str, int, float, bool)):
                filter_value = value
            elif isinstance(value, list):
                filter_value = [v for v in value if isinstance(v, (str, int, float))]
            else:
                filter_value = str(value)
            filters: TOracleWmsFilters = {field: filter_value}
        # For non-equality operators, convert to list format
        elif isinstance(value, (str, int, float, bool)):
            filters = {field: [value]}
        else:
            filters = {field: [str(value)]}
        return await filter_engine.filter_records(records, filters)
    except FlextOracleWmsDataValidationError:
        raise
    except Exception as e:
        handle_operation_exception(e, "filter by field")
        # Never reached due to handle_operation_exception always raising
        return FlextResult.fail(f"Filter by field failed: {e}")


async def flext_oracle_wms_filter_by_id_range(
    records: TOracleWmsRecordBatch,
    id_field: str = "id",
    min_id: object | None = None,
    max_id: object | None = None,
) -> FlextResult[TOracleWmsRecordBatch]:
    """Filter records by ID range.

    Args:
        records: Records to filter
        id_field: ID field name
        min_id: Minimum ID value
        max_id: Maximum ID value

    Returns:
        FlextResult with filtered records

    Raises:
        FlextOracleWmsDataValidationError: If filter data is invalid

    """
    try:
        filter_engine = flext_oracle_wms_create_filter()
        filters: TOracleWmsFilters = {}

        if min_id is not None and max_id is not None:
            # Range filter - use list of values with proper typing
            if isinstance(min_id, (str, int, float)) and isinstance(
                max_id,
                (str, int, float),
            ):
                filters[id_field] = [min_id, max_id]
            else:
                filters[id_field] = [str(min_id), str(max_id)]
        elif min_id is not None:
            # Single value filter
            filter_value = (
                min_id if isinstance(min_id, (str, int, float, bool)) else str(min_id)
            )
            filters[id_field] = filter_value
        elif max_id is not None:
            # Single value filter
            filter_value = (
                max_id if isinstance(max_id, (str, int, float, bool)) else str(max_id)
            )
            filters[id_field] = filter_value

        return await filter_engine.filter_records(records, filters)
    except FlextOracleWmsDataValidationError:
        raise
    except Exception as e:
        handle_operation_exception(e, "filter by ID range")
        # Never reached due to handle_operation_exception always raising
        return FlextResult.fail(f"Filter by ID range failed: {e}")
