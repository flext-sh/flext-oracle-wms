"""FLEXT Generic Filtering - Functional patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import cast

from flext_core import FlextExceptions, FlextLogger, FlextResult, FlextTypes as t

from flext_oracle_wms.constants import FlextOracleWmsConstants


# Exception class with real inheritance
class FlextOracleWmsDataValidationError(FlextExceptions.BaseError):
    """FlextOracleWmsDataValidationError - real inheritance from BaseError."""


class FlextOracleWmsFilter:
    """Generic filter with functional composition and FLEXT delegation."""

    logger = FlextLogger(__name__)

    def __init__(
        self,
        *,
        filters: dict[str, t.GeneralValueType] | None = None,
        case_sensitive: bool = False,
        max_conditions: int = 50,
    ) -> None:
        """Initialize with functional defaults."""
        if (
            max_conditions <= 0
            or max_conditions > FlextOracleWmsConstants.Filtering.MAX_FILTER_CONDITIONS
        ):
            msg = "Invalid max_conditions"
            raise FlextExceptions.BaseError(msg)

        self.max_conditions = max_conditions
        self.case_sensitive = case_sensitive
        self.filters = filters or {}

        # Initialize operator dispatch table
        self._init_operators()

        if (
            self.filters
            and self._validate_filter_conditions_total(self.filters).is_failure
        ):
            msg = "Filter validation failed"
            raise FlextOracleWmsDataValidationError(msg)

    def _init_operators(self) -> None:
        """Initialize operator dispatch table."""
        # This method can be extended for custom operators

    def _validate_filter_conditions_total(
        self,
        filters: dict[str, t.GeneralValueType],
    ) -> FlextResult[bool]:
        """Validate total filter conditions."""
        total = sum(len(v) if isinstance(v, list) else 1 for v in filters.values())
        if total > self.max_conditions:
            return FlextResult.fail(
                f"Too many filter conditions: {total} > {self.max_conditions}",
            )
        return FlextResult.ok(True)

    def _get_nested_value(
        self, record: dict[str, t.GeneralValueType], field: str
    ) -> t.GeneralValueType:
        """Get nested value from record using dot notation."""
        keys = field.split(".")
        value: object = record
        try:
            for key in keys:
                if isinstance(value, dict):
                    value = value.get(key)
                else:
                    return cast("t.GeneralValueType", None)
            return cast("t.GeneralValueType", value)
        except (KeyError, TypeError):
            return cast("t.GeneralValueType", None)

    def _normalize(self, value: object) -> object:
        """Normalize value for comparison."""
        if value is None:
            return ""
        if not self.case_sensitive and isinstance(value, str):
            return value.lower()
        return value

    def filter_records(
        self,
        records: list[dict[str, t.GeneralValueType]],
        filters: dict[str, t.GeneralValueType],
        limit: int | None = None,
    ) -> FlextResult[list[dict[str, t.GeneralValueType]]]:
        """Filter records with functional composition."""
        if (result := self._validate_filters(filters)).is_failure:
            return FlextResult.fail(result.error or "Validation failed")

        self.filters = filters
        filtered = [r for r in records if self._matches_all_filters(r, filters)]
        if limit:
            filtered = filtered[:limit]
        return FlextResult.ok(filtered)

    def sort_records(
        self,
        records: list[dict[str, t.GeneralValueType]],
        sort_field: str,
        *,
        ascending: bool = True,
    ) -> FlextResult[list[dict[str, t.GeneralValueType]]]:
        """Sort records with functional key extraction."""
        try:

            def key_func(r: dict[str, t.GeneralValueType]) -> str:
                return str(
                    self._get_nested_value(r, sort_field)
                    or ("" if ascending else "zzz"),
                )

            return FlextResult.ok(sorted(records, key=key_func, reverse=not ascending))
        except Exception as e:
            self.logger.exception("Sort failed")
            return FlextResult.fail(f"Sort failed: {e}")

    def _validate_filters(
        self, filters: dict[str, t.GeneralValueType]
    ) -> FlextResult[bool]:
        """Validate filter conditions."""
        total = sum(len(v) if isinstance(v, list) else 1 for v in filters.values())
        if total > self.max_conditions:
            return FlextResult.fail(
                f"Too many conditions. Max: {self.max_conditions}, Got: {total}",
            )
        return FlextResult.ok(True)

    def _matches_all_filters(
        self,
        record: dict[str, t.GeneralValueType],
        filters: dict[str, t.GeneralValueType],
    ) -> bool:
        """Check if record matches all filters with functional composition."""
        return all(
            self._matches_condition(record, field, filter_value)
            for field, filter_value in filters.items()
        )

    def _matches_condition(
        self,
        record: dict[str, t.GeneralValueType],
        field: str,
        filter_value: t.GeneralValueType,
    ) -> bool:
        """Match condition with pattern matching."""
        field_value = self._get_nested_value(record, field)

        match filter_value:
            case dict() if "operator" in filter_value:
                # Advanced filter with operator
                operator = str(filter_value.get("operator", "eq"))
                value = filter_value.get("value")
                return self._apply_operator(field_value, operator, value)
            case list():
                # List matching
                return field_value in filter_value if field_value is not None else False
            case _:
                # Simple equality
                return self._normalize(field_value) == self._normalize(filter_value)

    def _apply_operator(
        self,
        field_value: object,
        operator: str,
        filter_value: object,
    ) -> bool:
        """Apply operator with functional dispatch."""
        operators = {
            "eq": lambda fv, f: self._normalize(fv) == self._normalize(f),
            "ne": lambda fv, f: self._normalize(fv) != self._normalize(f),
            "gt": lambda fv, f: (
                (
                    isinstance(fv, (int, float))
                    and isinstance(f, (int, float))
                    and fv > f
                )
                or (isinstance(fv, str) and isinstance(f, str) and fv > f)
            ),
            "lt": lambda fv, f: (
                (
                    isinstance(fv, (int, float))
                    and isinstance(f, (int, float))
                    and fv < f
                )
                or (isinstance(fv, str) and isinstance(f, str) and fv < f)
            ),
            "gte": lambda fv, f: (
                self._apply_operator(fv, "gt", f) or self._apply_operator(fv, "eq", f)
            ),
            "lte": lambda fv, f: (
                self._apply_operator(fv, "lt", f) or self._apply_operator(fv, "eq", f)
            ),
            "in": lambda fv, f: isinstance(f, (list, tuple)) and fv in f,
            "contains": lambda fv, f: (
                isinstance(fv, str) and isinstance(f, str) and f in fv
            ),
        }
        return operators.get(operator, lambda *_: False)(field_value, filter_value)

    @classmethod
    def create_filter(
        cls,
        *,
        case_sensitive: bool = False,
        max_conditions: int = 50,
    ) -> FlextOracleWmsFilter:
        """Create a new filter instance."""
        return cls(case_sensitive=case_sensitive, max_conditions=max_conditions)

    @classmethod
    def filter_by_field(
        cls,
        records: list[dict[str, t.GeneralValueType]],
        field: str,
        value: t.GeneralValueType,
        operator: str | None = None,
    ) -> FlextResult[list[dict[str, t.GeneralValueType]]]:
        """Filter records by field value."""
        engine = cls()
        filters: dict[str, t.GeneralValueType] = {field: value}
        if operator:
            filters[field] = cast(
                "t.GeneralValueType",
                {"operator": operator or "eq", "value": value},
            )
        # filters is already dict[str, t.GeneralValueType] compatible - no cast needed
        return engine.filter_records(records, filters)

    @classmethod
    def filter_by_id_range(
        cls,
        records: list[dict[str, t.GeneralValueType]],
        id_field: str,
        min_id: t.GeneralValueType | None = None,
        max_id: t.GeneralValueType | None = None,
    ) -> FlextResult[list[dict[str, t.GeneralValueType]]]:
        """Filter records by ID range."""
        if not records:
            return FlextResult.ok([])

        filtered = []
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
    def _check_min(field_value: object, min_val: object) -> bool:
        """Check minimum value constraint."""
        try:
            if isinstance(field_value, (int, float)) and isinstance(
                min_val,
                (int, float),
            ):
                return float(field_value) >= float(min_val)
            if isinstance(field_value, str) and isinstance(min_val, str):
                return field_value >= min_val
        except (TypeError, ValueError):
            pass
        return True

    @staticmethod
    def _check_max(field_value: object, max_val: object) -> bool:
        """Check maximum value constraint."""
        try:
            if isinstance(field_value, (int, float)) and isinstance(
                max_val,
                (int, float),
            ):
                return float(field_value) <= float(max_val)
            if isinstance(field_value, str) and isinstance(max_val, str):
                return field_value <= max_val
        except (TypeError, ValueError):
            pass
        return True


# Backward compatibility aliases
flext_oracle_wms_create_filter = FlextOracleWmsFilter.create_filter
flext_oracle_wms_filter_by_field = FlextOracleWmsFilter.filter_by_field
flext_oracle_wms_filter_by_id_range = FlextOracleWmsFilter.filter_by_id_range

__all__ = [
    "FlextOracleWmsFilter",
    "flext_oracle_wms_create_filter",
    "flext_oracle_wms_filter_by_field",
    "flext_oracle_wms_filter_by_id_range",
]
