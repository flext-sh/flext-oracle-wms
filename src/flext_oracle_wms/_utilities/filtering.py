"""Oracle WMS Filtering utilities.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    MutableSequence,
    Sequence,
)

from flext_api import u

from flext_oracle_wms import c, e, m, p, r, t
from flext_oracle_wms.errors import FlextOracleWmsErrors


class FlextOracleWmsUtilitiesFiltering:
    """Filtering utilities for Oracle WMS -- u.OracleWms.Filtering.*."""

    class Filter:
        """Generic filter with functional composition and strict validation."""

        logger = u.fetch_logger(__name__)

        def __init__(
            self,
            *,
            filters: t.MappingKV[str, t.OracleWms.FilterEntry] | None = None,
            case_sensitive: bool = False,
            max_conditions: int = 50,
        ) -> None:
            """Initialize filter engine with strict condition limits."""
            if (
                max_conditions <= 0
                or max_conditions > c.OracleWms.Filtering.MAX_FILTER_CONDITIONS
            ):
                error_message = "Invalid max_conditions"
                raise e.BaseError(error_message)
            self.max_conditions: int = max_conditions
            self.case_sensitive: bool = case_sensitive
            self.filters: t.MappingKV[str, t.OracleWms.FilterEntry] = filters or {}
            if (
                self.filters
                and self._validate_filter_conditions_total(self.filters).failure
            ):
                error_message = "Filter validation failed"
                raise FlextOracleWmsErrors.ValidationError(error_message)

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
            records: t.SequenceOf[t.OracleWms.FilterRecord],
            field: str,
            value: t.OracleWms.FilterScalar,
            operator: c.OracleWms.WmsFilterOperator | None = None,
        ) -> p.Result[Sequence[t.OracleWms.FilterRecord]]:
            """Filter records by one field using optional operator semantics."""
            engine = cls()
            filters: t.MappingKV[str, t.OracleWms.FilterEntry]
            if operator is None:
                filters = {field: value}
            else:
                filters = {
                    field: m.OracleWms.FlextOracleWmsOperatorFilter(
                        operator=operator,
                        value=value,
                    ),
                }
            return engine.filter_records(records, filters)

        @classmethod
        def filter_by_id_range(
            cls,
            records: t.SequenceOf[t.OracleWms.FilterRecord],
            id_field: str,
            min_id: t.OracleWms.FilterScalar | None = None,
            max_id: t.OracleWms.FilterScalar | None = None,
        ) -> p.Result[Sequence[t.OracleWms.FilterRecord]]:
            """Filter records by inclusive identifier range."""
            if not records:
                return r[Sequence[t.OracleWms.FilterRecord]].ok([])
            filtered: MutableSequence[t.OracleWms.FilterRecord] = []
            for record in records:
                field_value = record.get(id_field)
                if field_value is None:
                    continue
                if min_id is not None and (not cls._check_min(field_value, min_id)):
                    continue
                if max_id is not None and (not cls._check_max(field_value, max_id)):
                    continue
                filtered.append(record)
            return r[Sequence[t.OracleWms.FilterRecord]].ok(filtered)

        @classmethod
        def _check_max(
            cls,
            field_value: t.OracleWms.FilterRecordValue,
            max_val: t.OracleWms.FilterScalar,
        ) -> bool:
            return cls._compare(field_value, max_val, "<=")

        @classmethod
        def _check_min(
            cls,
            field_value: t.OracleWms.FilterRecordValue,
            min_val: t.OracleWms.FilterScalar,
        ) -> bool:
            return cls._compare(field_value, min_val, ">=")

        @classmethod
        def _compare(
            cls,
            left: t.OracleWms.FilterRecordValue | None,
            right: t.OracleWms.FilterScalar | t.OracleWms.FilterList,
            op: str,
        ) -> bool:
            try:
                left_num = t.float_adapter().validate_python(left)
                right_num = t.float_adapter().validate_python(right)
                result = cls._compare_float(
                    left_num,
                    right_num,
                    op,
                )
            except c.ValidationError:
                result = cls._compare_string(
                    str(left),
                    str(right),
                    op,
                )
            final: bool = result
            return final

        @staticmethod
        def _compare_float(left_num: float, right_num: float, op: str) -> bool:
            """Compare numeric filter values."""
            match op:
                case ">":
                    return left_num > right_num
                case "<":
                    return left_num < right_num
                case ">=":
                    return left_num >= right_num
                case _:
                    return left_num <= right_num

        @staticmethod
        def _compare_string(left_str: str, right_str: str, op: str) -> bool:
            """Compare string filter values."""
            match op:
                case ">":
                    return left_str > right_str
                case "<":
                    return left_str < right_str
                case ">=":
                    return left_str >= right_str
                case _:
                    return left_str <= right_str

        @staticmethod
        def _condition_size(value: t.OracleWms.FilterEntry) -> int:
            match value:
                case list() as items:
                    return len(items)
                case m.OracleWms.FlextOracleWmsOperatorFilter() as condition:
                    match condition.value:
                        case list() as values:
                            return len(values)
                        case _:
                            return 1
                case _:
                    return 1

        def filter_records(
            self,
            records: t.SequenceOf[t.OracleWms.FilterRecord],
            filters: t.MappingKV[str, t.OracleWms.FilterEntry],
            limit: int | None = None,
        ) -> p.Result[Sequence[t.OracleWms.FilterRecord]]:
            """Filter records against field conditions and optional limit."""
            if (result := self._validate_filters(filters)).failure:
                return r[Sequence[t.OracleWms.FilterRecord]].fail(
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
            return r[Sequence[t.OracleWms.FilterRecord]].ok(filtered)

        def sort_records(
            self,
            records: t.SequenceOf[t.OracleWms.FilterRecord],
            sort_field: str,
            *,
            ascending: bool = True,
        ) -> p.Result[Sequence[t.OracleWms.FilterRecord]]:
            """Sort records by a dot-path field."""
            try:

                def key_func(record: t.OracleWms.FilterRecord) -> str:
                    value = self._get_nested_value(record, sort_field)
                    return str(
                        value if value is not None else "" if ascending else "zzz",
                    )

                return r[Sequence[t.OracleWms.FilterRecord]].ok(
                    sorted(records, key=key_func, reverse=not ascending),
                )
            except Exception as exc:
                self.logger.exception("Sort failed")
                return r[Sequence[t.OracleWms.FilterRecord]].fail_op("Sort", exc)

        def _apply_operator(
            self,
            field_value: t.OracleWms.FilterRecordValue | None,
            operator: c.OracleWms.WmsFilterOperator | str,
            filter_value: (t.OracleWms.FilterScalar | t.OracleWms.FilterList),
        ) -> bool:
            if (field_value is None and filter_value is not None) or (
                field_value is not None and filter_value is None
            ):
                result = False
            elif field_value is None and filter_value is None:
                result = operator in {
                    c.OracleWms.WmsFilterOperator.EQ,
                    c.OracleWms.WmsFilterOperator.GTE,
                    c.OracleWms.WmsFilterOperator.LTE,
                    "eq",
                    "gte",
                    "lte",
                }
            else:
                match operator:
                    case c.OracleWms.WmsFilterOperator.EQ | "eq":
                        result = self._normalize(field_value) == self._normalize(
                            filter_value,
                        )
                    case c.OracleWms.WmsFilterOperator.NE | "ne":
                        result = self._normalize(field_value) != self._normalize(
                            filter_value,
                        )
                    case c.OracleWms.WmsFilterOperator.IN | "in":
                        match filter_value:
                            case list() as options:
                                result = str(field_value) in [
                                    str(item) for item in options
                                ]
                            case _:
                                result = False
                    case c.OracleWms.WmsFilterOperator.CONTAINS | "contains":
                        result = (
                            isinstance(field_value, str)
                            and str(filter_value) in field_value
                        )
                    case c.OracleWms.WmsFilterOperator.GT | "gt":
                        result = type(field_value) is type(
                            filter_value,
                        ) and self._compare(field_value, filter_value, ">")
                    case c.OracleWms.WmsFilterOperator.LT | "lt":
                        result = type(field_value) is type(
                            filter_value,
                        ) and self._compare(field_value, filter_value, "<")
                    case c.OracleWms.WmsFilterOperator.GTE | "gte":
                        result = type(field_value) is type(
                            filter_value,
                        ) and self._compare(field_value, filter_value, ">=")
                    case c.OracleWms.WmsFilterOperator.LTE | "lte":
                        result = type(field_value) is type(
                            filter_value,
                        ) and self._compare(field_value, filter_value, "<=")
                    case _:
                        result = False
            return result

        def _get_nested_value(
            self,
            record: t.OracleWms.FilterRecord,
            field: str,
        ) -> t.OracleWms.NestedFilterValue | None:
            keys = field.split(".")
            # Try nested dict traversal first
            current: (
                t.OracleWms.NestedFilterValue
                | t.MappingKV[
                    str,
                    t.OracleWms.FilterScalar
                    | t.OracleWms.FilterList
                    | t.MappingKV[
                        str,
                        t.OracleWms.FilterScalar | t.OracleWms.FilterList,
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
            record: t.OracleWms.FilterRecord,
            filters: t.MappingKV[str, t.OracleWms.FilterEntry],
        ) -> bool:
            return all(
                (
                    self._matches_condition(record, field, filter_value)
                    for field, filter_value in filters.items()
                ),
            )

        def _matches_condition(
            self,
            record: t.OracleWms.FilterRecord,
            field: str,
            filter_value: t.OracleWms.FilterEntry,
        ) -> bool:
            field_value = self._get_nested_value(record, field)
            match filter_value:
                case m.OracleWms.FlextOracleWmsOperatorFilter() as condition:
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
            value: (t.OracleWms.FilterRecordValue | t.OracleWms.FilterScalar),
        ) -> t.OracleWms.FilterRecordValue | str:
            match value:
                case None:
                    return ""
                case str() as text if not self.case_sensitive:
                    return text.lower()
                case _:
                    return value

        def _validate_filter_conditions_total(
            self,
            filters: t.MappingKV[str, t.OracleWms.FilterEntry],
        ) -> p.Result[bool]:
            total = sum(self._condition_size(value) for value in filters.values())
            if total > self.max_conditions:
                return r[bool].fail(
                    f"Too many filter conditions: {total} > {self.max_conditions}",
                )
            return r[bool].ok(True)

        def _validate_filters(
            self,
            filters: t.MappingKV[str, t.OracleWms.FilterEntry],
        ) -> p.Result[bool]:
            total = sum(self._condition_size(value) for value in filters.values())
            if total > self.max_conditions:
                return r[bool].fail(
                    f"Too many conditions. Max: {self.max_conditions}, Got: {total}",
                )
            return r[bool].ok(True)


__all__: list[str] = [
    "FlextOracleWmsUtilitiesFiltering",
]
