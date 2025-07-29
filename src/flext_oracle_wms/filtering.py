"""Oracle WMS Filtering - Essential filtering capabilities using flext-core patterns.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Simplified but powerful filtering for Oracle WMS records.
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any

from flext_core import FlextResult, get_logger

from flext_oracle_wms.constants import (
    FlextOracleWmsDefaults,
    FlextOracleWmsErrorMessages,
    OracleWMSFilterOperator,
)
from flext_oracle_wms.exceptions import (
    FlextOracleWmsDataValidationError,
    FlextOracleWmsError,
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
            msg = f"Max conditions cannot exceed {FlextOracleWmsDefaults.MAX_FILTER_CONDITIONS}"
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
            if not isinstance(records, list):
                msg = "Records must be a list"
                raise FlextOracleWmsDataValidationError(msg)

            if not isinstance(filters, dict):
                msg = "Filters must be a dictionary"
                raise FlextOracleWmsDataValidationError(msg)

            if not filters:
                limited_records = records[:limit] if limit else records
                return FlextResult.ok(limited_records)

            # Validate filter conditions count
            total_conditions = sum(
                len(conditions) if isinstance(conditions, dict) else 1
                for conditions in filters.values()
            )

            if total_conditions > self.max_conditions:
                return FlextResult.fail(
                    f"Too many filter conditions: {total_conditions} > {self.max_conditions}"
                )

            # Apply filters
            filtered_records = []
            for record in records:
                if self._record_matches_filters(record, filters):
                    filtered_records.append(record)

                    # Apply limit
                    if limit and len(filtered_records) >= limit:
                        break

            logger.debug(
                "Filtering completed",
                original_count=len(records),
                filtered_count=len(filtered_records),
                filter_count=total_conditions,
            )

            return FlextResult.ok(filtered_records)

        except FlextOracleWmsDataValidationError:
            raise
        except Exception as e:
            logger.exception("Failed to filter records")
            msg = f"{FlextOracleWmsErrorMessages.PROCESSING_FAILED}: {e}"
            raise FlextOracleWmsError(msg) from e

    async def sort_records(
        self,
        records: TOracleWmsRecordBatch,
        sort_field: str,
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
            if not isinstance(records, list):
                msg = "Records must be a list"
                raise FlextOracleWmsDataValidationError(msg)

            if not isinstance(sort_field, str) or not sort_field.strip():
                msg = "Sort field must be a non-empty string"
                raise FlextOracleWmsDataValidationError(msg)

            def get_sort_value(record: TOracleWmsRecord) -> Any:
                value = self._get_nested_value(record, sort_field)
                # Handle None values
                if value is None:
                    return "" if ascending else "zzz"
                return value

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
            logger.exception("Failed to sort records")
            msg = f"{FlextOracleWmsErrorMessages.PROCESSING_FAILED}: {e}"
            raise FlextOracleWmsError(msg) from e

    def _record_matches_filters(
        self,
        record: TOracleWmsRecord,
        filters: TOracleWmsFilters,
    ) -> bool:
        """Check if record matches all filters (AND logic)."""
        for field, conditions in filters.items():
            if not self._record_matches_field_conditions(record, field, conditions):
                return False
        return True

    def _record_matches_field_conditions(
        self,
        record: TOracleWmsRecord,
        field: str,
        conditions: Any,
    ) -> bool:
        """Check if record matches field conditions."""
        field_value = self._get_nested_value(record, field)

        # Handle simple equality
        if not isinstance(conditions, dict):
            return self._op_equals(field_value, conditions)

        # Handle operator conditions
        for operator, filter_value in conditions.items():
            if operator not in self._operators:
                continue

            operator_func = self._operators[operator]
            if not operator_func(field_value, filter_value):
                return False

        return True

    def _get_nested_value(self, record: TOracleWmsRecord, field_path: str) -> Any:
        """Get value from nested field path using dot notation."""
        if "." not in field_path:
            return record.get(field_path)

        current_value = record
        for field_part in field_path.split("."):
            if isinstance(current_value, dict):
                current_value = current_value.get(field_part)
                if current_value is None:
                    return None
            else:
                return None

        return current_value

    def _normalize_for_comparison(self, value: Any) -> Any:
        """Normalize value for case-insensitive comparison."""
        if not self.case_sensitive and isinstance(value, str):
            return value.lower()
        return value

    # Operator implementations
    def _op_equals(self, field_value: Any, filter_value: Any) -> bool:
        """Equality operator."""
        return self._normalize_for_comparison(
            field_value
        ) == self._normalize_for_comparison(filter_value)

    def _op_not_equals(self, field_value: Any, filter_value: Any) -> bool:
        """Not equals operator."""
        return self._normalize_for_comparison(
            field_value
        ) != self._normalize_for_comparison(filter_value)

    def _op_greater_than(self, field_value: Any, filter_value: Any) -> bool:
        """Greater than operator."""
        try:
            return field_value > filter_value
        except (TypeError, ValueError):
            return False

    def _op_greater_equal(self, field_value: Any, filter_value: Any) -> bool:
        """Greater than or equal operator."""
        try:
            return field_value >= filter_value
        except (TypeError, ValueError):
            return False

    def _op_less_than(self, field_value: Any, filter_value: Any) -> bool:
        """Less than operator."""
        try:
            return field_value < filter_value
        except (TypeError, ValueError):
            return False

    def _op_less_equal(self, field_value: Any, filter_value: Any) -> bool:
        """Less than or equal operator."""
        try:
            return field_value <= filter_value
        except (TypeError, ValueError):
            return False

    def _op_in(self, field_value: Any, filter_value: Any) -> bool:
        """In operator (value in list)."""
        if not isinstance(filter_value, (list, tuple, set)):
            return False

        normalized_field = self._normalize_for_comparison(field_value)
        normalized_list = [self._normalize_for_comparison(v) for v in filter_value]
        return normalized_field in normalized_list

    def _op_not_in(self, field_value: Any, filter_value: Any) -> bool:
        """Not in operator (value not in list)."""
        return not self._op_in(field_value, filter_value)

    def _op_like(self, field_value: Any, filter_value: Any) -> bool:
        """Like operator (pattern matching)."""
        if not isinstance(field_value, str) or not isinstance(filter_value, str):
            return False

        field_str = self._normalize_for_comparison(field_value)
        pattern_str = self._normalize_for_comparison(filter_value)

        # Convert SQL LIKE pattern to regex
        pattern = pattern_str.replace("%", ".*").replace("_", ".")

        flags = 0 if self.case_sensitive else re.IGNORECASE
        return bool(re.search(pattern, field_str, flags))

    def _op_not_like(self, field_value: Any, filter_value: Any) -> bool:
        """Not like operator."""
        return not self._op_like(field_value, filter_value)


# Factory function
def flext_oracle_wms_create_filter(
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
        msg = f"Max conditions cannot exceed {FlextOracleWmsDefaults.MAX_FILTER_CONDITIONS}"
        raise FlextOracleWmsError(msg)

    return FlextOracleWmsFilter(
        case_sensitive=case_sensitive,
        max_conditions=max_conditions,
    )


# Convenience functions
async def flext_oracle_wms_filter_by_field(
    records: TOracleWmsRecordBatch,
    field: str,
    value: Any,
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
        filters = {field: {operator: value}}
        return await filter_engine.filter_records(records, filters)
    except FlextOracleWmsDataValidationError:
        raise
    except Exception as e:
        logger.exception("Failed to filter by field")
        msg = f"{FlextOracleWmsErrorMessages.PROCESSING_FAILED}: {e}"
        raise FlextOracleWmsError(msg) from e


async def flext_oracle_wms_filter_by_id_range(
    records: TOracleWmsRecordBatch,
    id_field: str = "id",
    min_id: Any | None = None,
    max_id: Any | None = None,
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
        filters = {}

        if min_id is not None:
            filters[id_field] = {OracleWMSFilterOperator.GE: min_id}
        if max_id is not None:
            if id_field in filters:
                filters[id_field][OracleWMSFilterOperator.LE] = max_id
            else:
                filters[id_field] = {OracleWMSFilterOperator.LE: max_id}

        return await filter_engine.filter_records(records, filters)
    except FlextOracleWmsDataValidationError:
        raise
    except Exception as e:
        logger.exception("Failed to filter by ID range")
        msg = f"{FlextOracleWmsErrorMessages.PROCESSING_FAILED}: {e}"
        raise FlextOracleWmsError(msg) from e
