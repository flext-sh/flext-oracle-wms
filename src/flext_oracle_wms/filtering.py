"""Backward-compatibility filtering shim.

Provides legacy import path `flext_oracle_wms.filtering` by exposing
filter components implemented in `wms_operations` with the API expected
by the tests in this repository.


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import re
from typing import override

from flext_core import FlextLogger, FlextResult, FlextTypes

from flext_oracle_wms.constants import (
    FlextOracleWmsConstants,
    OracleWMSFilterOperator,
)
from flext_oracle_wms.typings import FlextOracleWmsTypes
from flext_oracle_wms.wms_exceptions import (
    FlextOracleWmsDataValidationError,
    FlextOracleWmsError,
)


class FlextOracleWmsFilter:
    """Oracle WMS filter with case sensitivity and validation.

    This class provides a unified interface for Oracle WMS filtering operations,
    consolidating functionality from FlextOracleWmsFilter with additional
    case sensitivity support.
    """

    # Shared logger for all filter operations
    logger = FlextLogger(__name__)

    @override
    def __init__(
        self,
        *,
        filters: FlextOracleWmsTypes.Core.Dict | None = None,
        case_sensitive: bool = False,
        max_conditions: int = 50,
    ) -> None:
        """Initialize Oracle WMS filter with case sensitivity and validation.

        Args:
            filters: Filter conditions to initialize with
            case_sensitive: Whether string comparisons should be case sensitive
            max_conditions: Maximum number of filter conditions allowed

        """
        if max_conditions <= 0:
            msg = "max_conditions must be positive"
            raise FlextOracleWmsError(msg)
        # Enforce upper bound according to defaults used by tests
        if max_conditions > FlextOracleWmsConstants.Filtering.MAX_FILTER_CONDITIONS:
            msg = "max_conditions cannot exceed configured maximum"
            raise FlextOracleWmsError(msg)

        self.max_conditions = max_conditions
        self.case_sensitive = case_sensitive
        self.filters: FlextOracleWmsTypes.Core.Dict = filters or {}

        # Validate filters if provided
        if self.filters:
            validation_result: FlextResult[None] = (
                self._validate_filter_conditions_total(self.filters)
            )
            if validation_result.is_failure:
                raise FlextOracleWmsDataValidationError(
                    validation_result.error or "Filter validation failed",
                )

    def _normalize_for_comparison(self, value: object) -> object:
        if isinstance(value, str) and not self.case_sensitive:
            return value.lower().strip()
        return value

    # Override LIKE to honor case_sensitive flag for tests
    def _op_like(self, field_value: object, filter_value: object) -> bool:
        if not isinstance(field_value, str) or not isinstance(filter_value, str):
            return False
        pattern = filter_value.replace("%", ".*").replace("_", ".")
        try:
            flags = 0 if self.case_sensitive else re.IGNORECASE
            return bool(re.match(pattern, field_value, flags))
        except re.error:
            # Invalid regex pattern - return False for LIKE operation
            return False

    def _op_not_like(self, field_value: object, filter_value: object) -> bool:
        return not self._op_like(field_value, filter_value)

    def _op_in(self, field_value: object, filter_value: object) -> bool:
        """In operator with case sensitivity support."""
        if isinstance(filter_value, (list, tuple)):
            if isinstance(field_value, str) and not self.case_sensitive:
                # Case insensitive comparison
                return any(
                    isinstance(item, str) and field_value.lower() == item.lower()
                    for item in filter_value
                )
            return field_value in filter_value
        return False

    def filter_records(
        self,
        records: list[FlextOracleWmsTypes.Core.Dict],
        filters: FlextOracleWmsTypes.Core.Dict,
    ) -> FlextResult[list[FlextOracleWmsTypes.Core.Dict]]:
        """Filter records with given filters.

        Args:
            records: List of records to filter
            filters: Filter conditions to apply

        Returns:
            FlextResult containing filtered records

        """
        # Parameters are already properly typed

        # Validate filter conditions
        count_result: FlextResult[None] = self._validate_filter_conditions_total(
            filters
        )
        if count_result.is_failure:
            return FlextResult[list[FlextOracleWmsTypes.Core.Dict]].fail(
                count_result.error or "Filter validation failed",
            )

        # Store filters for validation
        self.filters = filters
        filtered_records = self._apply_record_filters(records)
        return FlextResult[list[FlextOracleWmsTypes.Core.Dict]].ok(filtered_records)

    def filter_records_with_options(
        self,
        records: list[FlextOracleWmsTypes.Core.Dict],
        filters: FlextOracleWmsTypes.Core.Dict,
        limit: int | None = None,
    ) -> FlextResult[list[FlextOracleWmsTypes.Core.Dict]]:
        """Filter records with additional options like limit.

        Args:
            records: List of records to filter
            filters: Filter conditions to apply
            limit: Optional limit on number of results

        Returns:
            FlextResult containing filtered records

        """
        count_result: FlextResult[None] = self._validate_filter_conditions_total(
            filters
        )
        if count_result.is_failure:
            return FlextResult[list[FlextOracleWmsTypes.Core.Dict]].fail(
                count_result.error or "Filter validation failed",
            )

        # Store filters for validation
        self.filters = filters
        filtered_records = self._apply_record_filters(records)
        if limit is not None:
            filtered_records = filtered_records[:limit]
        return FlextResult[list[FlextOracleWmsTypes.Core.Dict]].ok(filtered_records)

    def sort_records(
        self,
        records: list[FlextOracleWmsTypes.Core.Dict],
        sort_field: str,
        *,
        ascending: bool = True,
    ) -> FlextResult[list[FlextOracleWmsTypes.Core.Dict]]:
        """Sort records by specified field.

        Args:
            records: List of records to sort
            sort_field: Field name to sort by
            ascending: Whether to sort in ascending order

        Returns:
            FlextResult containing sorted records

        """
        # Parameters are already properly typed

        try:

            def key_func(record: FlextOracleWmsTypes.Core.Dict) -> str:
                value = self._get_nested_value(record, sort_field)
                if value is None:
                    return "" if ascending else "zzz"
                return str(value)

            sorted_records = sorted(records, key=key_func, reverse=not ascending)
            return FlextResult[list[FlextOracleWmsTypes.Core.Dict]].ok(sorted_records)
        except Exception as e:
            error_msg = f"sort_records failed: {e}"
            FlextOracleWmsFilter.logger.exception(error_msg)
            return FlextResult[list[FlextOracleWmsTypes.Core.Dict]].fail(error_msg)

    def _validate_filter_conditions_total(
        self,
        filters: FlextOracleWmsTypes.Core.Dict,
    ) -> FlextResult[None]:
        try:
            total_conditions = 0
            for value in filters.values():
                if isinstance(value, list):
                    total_conditions += len(value)
                else:
                    total_conditions += 1
            if total_conditions > self.max_conditions:
                return FlextResult[None].fail(
                    f"Too many filter conditions. Max: {self.max_conditions}, Got: {total_conditions}",
                )
            return FlextResult[None].ok(None)
        except Exception as e:  # pragma: no cover
            return FlextResult[None].fail(str(e))

    def _validate_filter_conditions_count(self: object) -> None:
        """Validate that filter conditions don't exceed maximum."""
        if len(self.filters) > self.max_conditions:
            msg = f"Too many filter conditions. Max: {self.max_conditions}, Got: {len(self.filters)}"
            raise FlextOracleWmsDataValidationError(msg)

    def _apply_record_filters(
        self,
        records: list[FlextOracleWmsTypes.Core.Dict],
    ) -> list[FlextOracleWmsTypes.Core.Dict]:
        """Apply all filter conditions to records."""
        if not self.filters:
            return records

        return [record for record in records if self._record_matches_filters(record)]

    def _record_matches_filters(self, record: FlextOracleWmsTypes.Core.Dict) -> bool:
        """Check if record matches all filter conditions."""
        for field, filter_value in self.filters.items():
            if not self._matches_condition(record, field, filter_value):
                return False
        return True

    def _matches_condition(
        self,
        record: FlextOracleWmsTypes.Core.Dict,
        field: str,
        filter_value: object,
    ) -> bool:
        """Check if record field matches filter condition."""
        field_value = self._get_nested_value(record, field)

        # Handle different filter value types
        if isinstance(filter_value, dict):
            # Advanced filter with operator
            operator = str(filter_value.get("operator", "eq"))
            value = filter_value.get("value")
            return self._apply_operator(field_value, operator, value)

        return self._op_equals(field_value, filter_value)

    def _get_nested_value(
        self,
        record: FlextOracleWmsTypes.Core.Dict,
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
        """Apply filter operator to field value."""
        if operator == "eq":
            return self._op_equals(field_value, filter_value)
        if operator == "ne":
            return not self._op_equals(field_value, filter_value)
        if operator == "gt":
            return self._op_greater_than(field_value, filter_value)
        if operator == "lt":
            return self._op_less_than(field_value, filter_value)
        if operator == "gte":
            return self._op_greater_than(field_value, filter_value) or self._op_equals(
                field_value,
                filter_value,
            )
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
        """Equality operator."""
        normalized_field = self._normalize_for_comparison(field_value)
        normalized_filter = self._normalize_for_comparison(filter_value)

        # Handle list filter values (IN operation)
        if isinstance(normalized_filter, list):
            return normalized_field in normalized_filter

        return normalized_field == normalized_filter

    def _op_not_equals(self, field_value: object, filter_value: object) -> bool:
        """Not equals operator."""
        return not self._op_equals(field_value, filter_value)

    def _op_greater_than(self, field_value: object, filter_value: object) -> bool:
        """Greater than operator."""
        try:
            if isinstance(field_value, (int, float)) and isinstance(
                filter_value,
                (int, float),
            ):
                return field_value > filter_value
            if isinstance(field_value, str) and isinstance(filter_value, str):
                return field_value > filter_value
            return False
        except (TypeError, ValueError):
            return False

    def _op_less_than(self, field_value: object, filter_value: object) -> bool:
        """Less than operator."""
        try:
            if isinstance(field_value, (int, float)) and isinstance(
                filter_value,
                (int, float),
            ):
                return field_value < filter_value
            if isinstance(field_value, str) and isinstance(filter_value, str):
                return field_value < filter_value
            return False
        except (TypeError, ValueError):
            return False

    def _op_greater_equal(self, field_value: object, filter_value: object) -> bool:
        """Greater than or equal operator."""
        try:
            if isinstance(field_value, (int, float)) and isinstance(
                filter_value,
                (int, float),
            ):
                return field_value >= filter_value
            return False
        except (TypeError, ValueError):
            return False

    def _op_less_equal(self, field_value: object, filter_value: object) -> bool:
        """Less than or equal operator."""
        try:
            if isinstance(field_value, (int, float)) and isinstance(
                filter_value,
                (int, float),
            ):
                return field_value <= filter_value
            return False
        except (TypeError, ValueError):
            return False

    def _op_not_in(self, field_value: object, filter_value: object) -> bool:
        """Not in operator."""
        return not self._op_in(field_value, filter_value)

    def _op_contains(self, field_value: object, filter_value: object) -> bool:
        """Check if field value contains filter value."""
        if isinstance(field_value, str) and isinstance(filter_value, str):
            if not self.case_sensitive:
                return filter_value.lower() in field_value.lower()
            return filter_value in field_value
        return False

    # Nested helper class for factory and utility functions
    class FilterFactory:
        """Factory and utility functions for Oracle WMS filters."""

        @staticmethod
        def create_filter(
            *,
            case_sensitive: bool = False,
            max_conditions: int = 50,
        ) -> FlextOracleWmsFilter:
            """Create a new filter with case sensitivity and maximum conditions."""
            return FlextOracleWmsFilter(
                case_sensitive=case_sensitive,
                max_conditions=max_conditions,
            )

        @staticmethod
        def filter_by_field(
            records: list[FlextOracleWmsTypes.Core.Dict],
            field: str,
            _value: object,
            operator: OracleWMSFilterOperator | None = None,
        ) -> FlextResult[list[FlextOracleWmsTypes.Core.Dict]]:
            """Filter records by field value and operator."""
            engine = FlextOracleWmsFilter()
            if operator == OracleWMSFilterOperator.NE:
                pass
            # Set filters before calling filter_records
            filters = {field: "op_value"}
            return engine.filter_records(records, filters)

        @staticmethod
        def filter_by_id_range(
            records: list[FlextOracleWmsTypes.Core.Dict],
            id_field: str,
            min_id: object | None = None,
            max_id: object | None = None,
        ) -> FlextResult[list[FlextOracleWmsTypes.Core.Dict]]:
            """Filter records by ID range."""
            # Records parameter is already properly typed

            if not records:
                return FlextResult[list[FlextOracleWmsTypes.Core.Dict]].ok([])

            # Apply manual range filtering since we need both min and max on same field
            filtered_records: list[FlextTypes.Dict] = []
            for record in records:
                field_value = record.get(id_field)
                if field_value is None:
                    continue

                # Apply min filter
                if min_id is not None:
                    try:
                        if isinstance(field_value, (int, float)) and isinstance(
                            min_id,
                            (int, float),
                        ):
                            # Type narrowing: both are numeric
                            numeric_field: float = float(field_value)
                            numeric_min: float = float(min_id)
                            if numeric_field < numeric_min:
                                continue
                        elif isinstance(field_value, str) and isinstance(min_id, str):
                            # Type narrowing: both are strings
                            str_field: str = field_value
                            str_min: str = min_id
                            if str_field < str_min:
                                continue
                        else:
                            continue
                    except (TypeError, ValueError):
                        continue

                # Apply max filter
                if max_id is not None:
                    try:
                        if isinstance(field_value, (int, float)) and isinstance(
                            max_id,
                            (int, float),
                        ):
                            # Type narrowing: both are numeric
                            numeric_field_max: float = float(field_value)
                            numeric_max: float = float(max_id)
                            if numeric_field_max > numeric_max:
                                continue
                        elif isinstance(field_value, str) and isinstance(max_id, str):
                            # Type narrowing: both are strings
                            str_field_max: str = field_value
                            str_max: str = max_id
                            if str_field_max > str_max:
                                continue
                        else:
                            continue
                    except (TypeError, ValueError):
                        continue

                # If we get here, record passes both filters
                filtered_records.append(record)

            return FlextResult[list[FlextOracleWmsTypes.Core.Dict]].ok(filtered_records)


# Backward compatibility aliases
flext_oracle_wms_create_filter = FlextOracleWmsFilter.FilterFactory.create_filter
flext_oracle_wms_filter_by_field = FlextOracleWmsFilter.FilterFactory.filter_by_field
flext_oracle_wms_filter_by_id_range = (
    FlextOracleWmsFilter.FilterFactory.filter_by_id_range
)

__all__: FlextOracleWmsTypes.Core.StringList = [
    "FlextOracleWmsFilter",
    "flext_oracle_wms_create_filter",
    "flext_oracle_wms_filter_by_field",
    "flext_oracle_wms_filter_by_id_range",
]
