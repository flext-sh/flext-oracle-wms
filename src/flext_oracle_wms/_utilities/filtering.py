"""Oracle WMS Filtering utilities.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, MutableSequence, Sequence

from pydantic import ValidationError

from flext_core import e, p, r, u
from flext_oracle_wms.constants import c
from flext_oracle_wms.errors import (
    FlextOracleWmsDataValidationError as _FlextOracleWmsDataValidationError,
)
from flext_oracle_wms.models import FlextOracleWmsModels
from flext_oracle_wms.typings import t

FlextOracleWmsOperatorFilter = (
    FlextOracleWmsModels.OracleWms.FlextOracleWmsOperatorFilter
)

# Canonical alias -- single source of truth lives in c.OracleWms.WmsFilterOperator
# c.OracleWms.WmsFilterOperator = c.OracleWms.WmsFilterOperator

# Type alias for filter entries (can be scalar, list, or operator filter)
type FilterEntry = (
    t.OracleWms.Core.FilterScalar
    | t.OracleWms.Core.FilterList
    | FlextOracleWmsOperatorFilter
)


class FlextOracleWmsUtilitiesFiltering:
    """Filtering utilities for Oracle WMS -- u.OracleWms.Filtering.*."""

    DataValidationError = _FlextOracleWmsDataValidationError
    OperatorFilter = FlextOracleWmsOperatorFilter

    class Filter:
        """Generic filter with functional composition and strict validation."""

        logger = u.fetch_logger(__name__)

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
                or max_conditions > c.Filtering.MAX_FILTER_CONDITIONS
            ):
                error_message = "Invalid max_conditions"
                raise e.BaseError(error_message)
            self.max_conditions: int = max_conditions
            self.case_sensitive: bool = case_sensitive
            self.filters: Mapping[str, FilterEntry] = filters or {}
            if (
                self.filters
                and self._validate_filter_conditions_total(self.filters).failure
            ):
                error_message = "Filter validation failed"
                raise _FlextOracleWmsDataValidationError(error_message)

        @classmethod
        def create_filter(
            cls,
            *,
            case_sensitive: bool = False,
            max_conditions: int = 50,
        ) -> FlextOracleWmsUtilitiesFiltering.Filter:
            """Create a filter engine with explicit configuration."""
            return cls(case_sensitive=case_sensitive, max_conditions=max_conditions)

        @classmethod
        def filter_by_field(
            cls,
            records: Sequence[t.OracleWms.Core.FilterRecord],
            field: str,
            value: t.OracleWms.Core.FilterScalar,
            operator: c.OracleWms.WmsFilterOperator | None = None,
        ) -> p.Result[Sequence[t.OracleWms.Core.FilterRecord]]:
            """Filter records by one field using optional operator semantics."""
            engine = cls()
            filters: Mapping[str, FilterEntry]
            if operator is None:
                filters = {field: value}
            else:
                filters = {
                    field: FlextOracleWmsOperatorFilter(operator=operator, value=value),
                }
            return engine.filter_records(records, filters)

        @classmethod
        def filter_by_id_range(
            cls,
            records: Sequence[t.OracleWms.Core.FilterRecord],
            id_field: str,
            min_id: t.OracleWms.Core.FilterScalar | None = None,
            max_id: t.OracleWms.Core.FilterScalar | None = None,
        ) -> p.Result[Sequence[t.OracleWms.Core.FilterRecord]]:
            """Filter records by inclusive identifier range."""
            if not records:
                return r[Sequence[t.OracleWms.Core.FilterRecord]].ok([])
            filtered: MutableSequence[t.OracleWms.Core.FilterRecord] = []
            for record in records:
                field_value = record.get(id_field)
                if field_value is None:
                    continue
                if min_id is not None and (not cls._check_min(field_value, min_id)):
                    continue
                if max_id is not None and (not cls._check_max(field_value, max_id)):
                    continue
                filtered.append(record)
            return r[Sequence[t.OracleWms.Core.FilterRecord]].ok(filtered)

        @classmethod
        def _check_max(
            cls,
            field_value: t.OracleWms.Core.FilterRecordValue,
            max_val: t.OracleWms.Core.FilterScalar,
        ) -> bool:
            return cls._compare(field_value, max_val, "<=")

        @classmethod
        def _check_min(
            cls,
            field_value: t.OracleWms.Core.FilterRecordValue,
            min_val: t.OracleWms.Core.FilterScalar,
        ) -> bool:
            return cls._compare(field_value, min_val, ">=")

        @staticmethod
        def _compare(
            left: t.OracleWms.Core.FilterRecordValue | None,
            right: t.OracleWms.Core.FilterScalar | t.OracleWms.Core.FilterList,
            op: str,
        ) -> bool:
            try:
                left_num = t.OracleWms.FLOAT_ADAPTER.validate_python(left)
                right_num = t.OracleWms.FLOAT_ADAPTER.validate_python(right)
                if op == ">":
                    return left_num > right_num
                if op == "<":
                    return left_num < right_num
                if op == ">=":
                    return left_num >= right_num
                return left_num <= right_num
            except ValidationError:
                left_str = str(left)
                right_str = str(right)
                if op == ">":
                    return left_str > right_str
                if op == "<":
                    return left_str < right_str
                if op == ">=":
                    return left_str >= right_str
                return left_str <= right_str

        @staticmethod
        def _condition_size(value: FilterEntry) -> int:
            match value:
                case list() as items:
                    return len(items)
                case FlextOracleWmsOperatorFilter() as condition:
                    match condition.value:
                        case list() as values:
                            return len(values)
                        case _:
                            return 1
                case _:
                    return 1

        def filter_records(
            self,
            records: Sequence[t.OracleWms.Core.FilterRecord],
            filters: Mapping[str, FilterEntry],
            limit: int | None = None,
        ) -> p.Result[Sequence[t.OracleWms.Core.FilterRecord]]:
            """Filter records against field conditions and optional limit."""
            if (result := self._validate_filters(filters)).failure:
                return r[Sequence[t.OracleWms.Core.FilterRecord]].fail(
                    result.error or "Validation failed",
                )
            self.filters = filters
            filtered = [
                record
                for record in records
                if self._matches_all_filters(record, filters)
            ]
            if limit is not None:
                filtered = filtered[:limit]
            return r[Sequence[t.OracleWms.Core.FilterRecord]].ok(filtered)

        def sort_records(
            self,
            records: Sequence[t.OracleWms.Core.FilterRecord],
            sort_field: str,
            *,
            ascending: bool = True,
        ) -> p.Result[Sequence[t.OracleWms.Core.FilterRecord]]:
            """Sort records by a dot-path field."""
            try:

                def key_func(record: t.OracleWms.Core.FilterRecord) -> str:
                    value = self._get_nested_value(record, sort_field)
                    return str(
                        value if value is not None else "" if ascending else "zzz"
                    )

                return r[Sequence[t.OracleWms.Core.FilterRecord]].ok(
                    sorted(records, key=key_func, reverse=not ascending),
                )
            except Exception as exc:
                self.logger.exception("Sort failed")
                return r[Sequence[t.OracleWms.Core.FilterRecord]].fail(
                    f"Sort failed: {exc}"
                )

        def _apply_operator(
            self,
            field_value: t.OracleWms.Core.FilterRecordValue | None,
            operator: c.OracleWms.WmsFilterOperator | str,
            filter_value: (t.OracleWms.Core.FilterScalar | t.OracleWms.Core.FilterList),
        ) -> bool:
            if field_value is None and filter_value is not None:
                return False
            if field_value is not None and filter_value is None:
                return False
            if field_value is None and filter_value is None:
                return operator in {
                    c.OracleWms.WmsFilterOperator.EQ,
                    c.OracleWms.WmsFilterOperator.GTE,
                    c.OracleWms.WmsFilterOperator.LTE,
                    "eq",
                    "gte",
                    "lte",
                }
            match operator:
                case c.OracleWms.WmsFilterOperator.EQ | "eq":
                    return self._normalize(field_value) == self._normalize(filter_value)
                case c.OracleWms.WmsFilterOperator.NE | "ne":
                    return self._normalize(field_value) != self._normalize(filter_value)
                case c.OracleWms.WmsFilterOperator.IN | "in":
                    match filter_value:
                        case list() as options:
                            return str(field_value) in [str(item) for item in options]
                        case _:
                            return False
                case c.OracleWms.WmsFilterOperator.CONTAINS | "contains":
                    if not isinstance(field_value, str):
                        return False
                    return str(filter_value) in field_value
                case c.OracleWms.WmsFilterOperator.GT | "gt":
                    if type(field_value) is not type(filter_value):
                        return False
                    return self._compare(field_value, filter_value, ">")
                case c.OracleWms.WmsFilterOperator.LT | "lt":
                    if type(field_value) is not type(filter_value):
                        return False
                    return self._compare(field_value, filter_value, "<")
                case c.OracleWms.WmsFilterOperator.GTE | "gte":
                    if type(field_value) is not type(filter_value):
                        return False
                    return self._compare(field_value, filter_value, ">=")
                case c.OracleWms.WmsFilterOperator.LTE | "lte":
                    if type(field_value) is not type(filter_value):
                        return False
                    return self._compare(field_value, filter_value, "<=")
                case _:
                    return False

        def _get_nested_value(
            self,
            record: t.OracleWms.Core.FilterRecord,
            field: str,
        ) -> t.OracleWms.Core.NestedFilterValue | None:
            keys = field.split(".")
            # Try nested dict traversal first
            current: (
                t.OracleWms.Core.NestedFilterValue
                | Mapping[
                    str,
                    t.OracleWms.Core.FilterScalar
                    | t.OracleWms.Core.FilterList
                    | Mapping[
                        str,
                        t.OracleWms.Core.FilterScalar | t.OracleWms.Core.FilterList,
                    ],
                ]
            ) = record
            for key in keys:
                match current:
                    case dict() as mapping:
                        next_value = mapping.get(key)
                        if next_value is None:
                            break
                        current = next_value
                    case _:
                        break
            else:
                if not isinstance(current, dict):
                    return current
                return None
            # Fallback: try underscore-joined flat key
            if len(keys) > 1:
                flat_key = "_".join(keys)
                flat_value = record.get(flat_key)
                if flat_value is not None:
                    return flat_value if not isinstance(flat_value, dict) else None
            return None

        def _matches_all_filters(
            self,
            record: t.OracleWms.Core.FilterRecord,
            filters: Mapping[str, FilterEntry],
        ) -> bool:
            return all(
                (
                    self._matches_condition(record, field, filter_value)
                    for field, filter_value in filters.items()
                ),
            )

        def _matches_condition(
            self,
            record: t.OracleWms.Core.FilterRecord,
            field: str,
            filter_value: FilterEntry,
        ) -> bool:
            field_value = self._get_nested_value(record, field)
            match filter_value:
                case FlextOracleWmsOperatorFilter() as condition:
                    return self._apply_operator(
                        field_value,
                        condition.operator,
                        condition.value,
                    )
                case list() as candidates:
                    return (
                        field_value in candidates if field_value is not None else False
                    )
                case _:
                    return self._normalize(field_value) == self._normalize(filter_value)

        def _normalize(
            self,
            value: (t.OracleWms.Core.FilterRecordValue | t.OracleWms.Core.FilterScalar),
        ) -> t.OracleWms.Core.FilterRecordValue | str:
            match value:
                case None:
                    return ""
                case str() as text if not self.case_sensitive:
                    return text.lower()
                case _:
                    return value

        def _validate_filter_conditions_total(
            self,
            filters: Mapping[str, FilterEntry],
        ) -> p.Result[bool]:
            total = sum(self._condition_size(value) for value in filters.values())
            if total > self.max_conditions:
                return r[bool].fail(
                    f"Too many filter conditions: {total} > {self.max_conditions}",
                )
            return r[bool].ok(True)

        def _validate_filters(
            self, filters: Mapping[str, FilterEntry]
        ) -> p.Result[bool]:
            total = sum(self._condition_size(value) for value in filters.values())
            if total > self.max_conditions:
                return r[bool].fail(
                    f"Too many conditions. Max: {self.max_conditions}, Got: {total}",
                )
            return r[bool].ok(True)


__all__: list[str] = [
    "FlextOracleWmsOperatorFilter",
    "FlextOracleWmsUtilitiesFiltering",
]
