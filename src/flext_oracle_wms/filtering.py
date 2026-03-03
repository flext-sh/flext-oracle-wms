"""FLEXT Generic Filtering - Functional patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping
from enum import StrEnum

from flext_core import FlextExceptions, FlextLogger, FlextResult
from pydantic import BaseModel, ConfigDict

from flext_oracle_wms.constants import FlextOracleWmsConstants

type FilterScalar = t.JsonPrimitive | None
type FilterList = list[FilterScalar]
type FilterRecordValue = FilterScalar | FilterList | Mapping[str, FilterRecordValue]
type FilterRecord = Mapping[str, FilterRecordValue]
type FilterEntry = FilterScalar | FilterList | OperatorFilter


class FlextOracleWmsDataValidationError(FlextExceptions.BaseError):
    """Data validation error for Oracle WMS filtering."""


class FilterOperator(StrEnum):
    """Supported filter operators."""

    EQ = "eq"
    NE = "ne"
    IN = "in"
    CONTAINS = "contains"
    GT = "gt"
    LT = "lt"
    GTE = "gte"
    LTE = "lte"


class OperatorFilter(BaseModel):
    """Filter declaration with explicit operator/value pair."""

    model_config = ConfigDict(extra="forbid", strict=True)

    operator: FilterOperator
    value: FilterScalar | FilterList


class FlextOracleWmsFilter:
    """Generic filter with functional composition and strict validation."""

    logger = FlextLogger(__name__)

    def __init__(
        self,
        *,
        filters: Mapping[str, FilterEntry] | None = None,
        case_sensitive: bool = False,
        max_conditions: int = 50,
    ) -> None:
        """Initialize filter engine with strict condition limits."""
        if (
            max_conditions <= 0
            or max_conditions > FlextOracleWmsConstants.Filtering.MAX_FILTER_CONDITIONS
        ):
            error_message = "Invalid max_conditions"
            raise FlextExceptions.BaseError(error_message)

        self.max_conditions: int = max_conditions
        self.case_sensitive: bool = case_sensitive
        self.filters: Mapping[str, FilterEntry] = filters or {}
        if (
            self.filters
            and self._validate_filter_conditions_total(self.filters).is_failure
        ):
            error_message = "Filter validation failed"
            raise FlextOracleWmsDataValidationError(error_message)

    def _validate_filter_conditions_total(
        self,
        filters: Mapping[str, FilterEntry],
    ) -> FlextResult[bool]:
        total = sum(self._condition_size(value) for value in filters.values())
        if total > self.max_conditions:
            return FlextResult.fail(
                f"Too many filter conditions: {total} > {self.max_conditions}",
            )
        return FlextResult.ok(True)

    @staticmethod
    def _condition_size(value: FilterEntry) -> int:
        match value:
            case list() as items:
                return len(items)
            case OperatorFilter() as condition:
                match condition.value:
                    case list() as values:
                        return len(values)
                    case _:
                        return 1
            case _:
                return 1

    def _get_nested_value(
        self,
        record: FilterRecord,
        field: str,
    ) -> FilterRecordValue | None:
        keys = field.split(".")
        current: FilterRecordValue | Mapping[str, FilterRecordValue] = record
        for key in keys:
            match current:
                case dict() as mapping:
                    next_value = mapping.get(key)
                    if next_value is None:
                        return None
                    current = next_value
                case _:
                    return None
        return current

    def _normalize(
        self,
        value: FilterRecordValue | FilterScalar,
    ) -> FilterRecordValue | str:
        match value:
            case None:
                return ""
            case str() as text if not self.case_sensitive:
                return text.lower()
            case _:
                return value

    def filter_records(
        self,
        records: list[FilterRecord],
        filters: Mapping[str, FilterEntry],
        limit: int | None = None,
    ) -> FlextResult[list[FilterRecord]]:
        """Filter records against field conditions and optional limit."""
        if (result := self._validate_filters(filters)).is_failure:
            return FlextResult.fail(result.error or "Validation failed")

        self.filters = filters
        filtered = [
            record for record in records if self._matches_all_filters(record, filters)
        ]
        if limit is not None:
            filtered = filtered[:limit]
        return FlextResult.ok(filtered)

    def sort_records(
        self,
        records: list[FilterRecord],
        sort_field: str,
        *,
        ascending: bool = True,
    ) -> FlextResult[list[FilterRecord]]:
        """Sort records by a dot-path field."""
        try:

            def key_func(record: FilterRecord) -> str:
                value = self._get_nested_value(record, sort_field)
                return str(value if value is not None else ("" if ascending else "zzz"))

            return FlextResult.ok(sorted(records, key=key_func, reverse=not ascending))
        except Exception as exc:
            self.logger.exception("Sort failed")
            return FlextResult.fail(f"Sort failed: {exc}")

    def _validate_filters(
        self,
        filters: Mapping[str, FilterEntry],
    ) -> FlextResult[bool]:
        total = sum(self._condition_size(value) for value in filters.values())
        if total > self.max_conditions:
            return FlextResult.fail(
                f"Too many conditions. Max: {self.max_conditions}, Got: {total}",
            )
        return FlextResult.ok(True)

    def _matches_all_filters(
        self,
        record: FilterRecord,
        filters: Mapping[str, FilterEntry],
    ) -> bool:
        return all(
            self._matches_condition(record, field, filter_value)
            for field, filter_value in filters.items()
        )

    def _matches_condition(
        self,
        record: FilterRecord,
        field: str,
        filter_value: FilterEntry,
    ) -> bool:
        field_value = self._get_nested_value(record, field)
        match filter_value:
            case OperatorFilter() as condition:
                return self._apply_operator(
                    field_value,
                    condition.operator,
                    condition.value,
                )
            case list() as candidates:
                return field_value in candidates if field_value is not None else False
            case _:
                return self._normalize(field_value) == self._normalize(filter_value)

    def _apply_operator(
        self,
        field_value: FilterRecordValue | None,
        operator: FilterOperator | str,
        filter_value: FilterScalar | FilterList,
    ) -> bool:
        if field_value is None and filter_value is not None:
            return False
        if field_value is not None and filter_value is None:
            return False
        if field_value is None and filter_value is None:
            return operator in {
                FilterOperator.EQ,
                FilterOperator.GTE,
                FilterOperator.LTE,
                "eq",
                "gte",
                "lte",
            }

        match operator:
            case FilterOperator.EQ | "eq":
                return self._normalize(field_value) == self._normalize(filter_value)
            case FilterOperator.NE | "ne":
                return self._normalize(field_value) != self._normalize(filter_value)
            case FilterOperator.IN | "in":
                match filter_value:
                    case list() as options:
                        return str(field_value) in [str(item) for item in options]
                    case _:
                        return False
            case FilterOperator.CONTAINS | "contains":
                return str(filter_value) in str(field_value)
            case FilterOperator.GT | "gt":
                return self._compare(field_value, filter_value, ">")
            case FilterOperator.LT | "lt":
                return self._compare(field_value, filter_value, "<")
            case FilterOperator.GTE | "gte":
                return self._compare(field_value, filter_value, ">=")
            case FilterOperator.LTE | "lte":
                return self._compare(field_value, filter_value, "<=")
            case _:
                return False

    @staticmethod
    def _compare(
        left: FilterRecordValue | None,
        right: FilterScalar | FilterList,
        op: str,
    ) -> bool:
        try:
            left_num = float(str(left))
            right_num = float(str(right))
            if op == ">":
                return left_num > right_num
            if op == "<":
                return left_num < right_num
            if op == ">=":
                return left_num >= right_num
            return left_num <= right_num
        except ValueError:
            left_str = str(left)
            right_str = str(right)
            if op == ">":
                return left_str > right_str
            if op == "<":
                return left_str < right_str
            if op == ">=":
                return left_str >= right_str
            return left_str <= right_str

    @classmethod
    def create_filter(
        cls,
        *,
        case_sensitive: bool = False,
        max_conditions: int = 50,
    ) -> FlextOracleWmsFilter:
        """Create a filter engine with explicit configuration."""
        return cls(case_sensitive=case_sensitive, max_conditions=max_conditions)

    @classmethod
    def filter_by_field(
        cls,
        records: list[FilterRecord],
        field: str,
        value: FilterScalar,
        operator: FilterOperator | None = None,
    ) -> FlextResult[list[FilterRecord]]:
        """Filter records by one field using optional operator semantics."""
        engine = cls()
        if operator is None:
            filters = {field: value}
        else:
            filters = {field: OperatorFilter(operator=operator, value=value)}
        return engine.filter_records(records, filters)

    @classmethod
    def filter_by_id_range(
        cls,
        records: list[FilterRecord],
        id_field: str,
        min_id: FilterScalar | None = None,
        max_id: FilterScalar | None = None,
    ) -> FlextResult[list[FilterRecord]]:
        """Filter records by inclusive identifier range."""
        if not records:
            return FlextResult.ok([])

        filtered: list[FilterRecord] = []
        for record in records:
            field_value = record.get(id_field)
            if field_value is None:
                continue

            if min_id is not None and not cls._check_min(field_value, min_id):
                continue
            if max_id is not None and not cls._check_max(field_value, max_id):
                continue
            filtered.append(record)

        return FlextResult.ok(filtered)

    @staticmethod
    def _check_min(field_value: FilterRecordValue, min_val: FilterScalar) -> bool:
        return FlextOracleWmsFilter._compare(field_value, min_val, ">=")

    @staticmethod
    def _check_max(field_value: FilterRecordValue, max_val: FilterScalar) -> bool:
        return FlextOracleWmsFilter._compare(field_value, max_val, "<=")


__all__ = ["FilterOperator", "FlextOracleWmsFilter", "OperatorFilter"]
