"""Oracle WMS filter operator semantics.

All operator predicates, ordering and path resolution live here so the
filtering engine only composes them.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping
from operator import ge, gt, le, lt

from flext_api import u

from flext_oracle_wms.constants import c
from flext_oracle_wms.models import m
from flext_oracle_wms.typings import t


class FlextOracleWmsUtilitiesFilteringOperators:
    """Pure predicates and lookups used by the WMS filter engine."""

    @staticmethod
    def size(entry: t.OracleWms.FilterEntry) -> int:
        """Count the conditions one filter entry declares.

        Returns:
            The number of conditions.

        """
        values = (
            entry.value
            if isinstance(entry, m.OracleWms.FlextOracleWmsOperatorFilter)
            else entry
        )
        return len(values) if isinstance(values, list) else 1

    @classmethod
    def compare(
        cls,
        left: t.OracleWms.FilterRecordValue | None,
        right: t.OracleWms.FilterValues,
        symbol: str,
    ) -> bool:
        """Compare two values with one ordering symbol.

        Returns:
            Whether the relation holds.

        """
        if isinstance(left, str) and isinstance(right, str):
            return cls.ordered(left, right, symbol)
        adapter = u.float_adapter()
        left_num = u.validate_value(adapter, cls._scalar(left), strict=True).unwrap()
        right_num = u.validate_value(adapter, cls._scalar(right), strict=True).unwrap()
        return cls.ordered(left_num, right_num, symbol)

    @staticmethod
    def ordered(left: float | str, right: float | str, symbol: str) -> bool:
        """Apply one ordering symbol.

        Returns:
            Whether the relation holds.

        """
        match symbol:
            case ">":
                return gt(left, right)
            case "<":
                return lt(left, right)
            case ">=":
                return ge(left, right)
            case _:
                return le(left, right)

    @staticmethod
    def resolve(
        value: c.OracleWms.WmsFilterOperator | str,
    ) -> c.OracleWms.WmsFilterOperator | None:
        """Resolve a declared operator, leaving an unknown value unmatched.

        Returns:
            The declared operator or ``None``.

        """
        try:
            return c.OracleWms.WmsFilterOperator(value)
        except ValueError:
            return None

    @staticmethod
    def normalize(
        value: t.OracleWms.FilterRecordValue | t.OracleWms.FilterScalar,
        *,
        case_sensitive: bool,
    ) -> t.OracleWms.FilterRecordValue | str:
        """Normalize a value for equality, folding case unless requested.

        Returns:
            The normalized value.

        """
        if value is None:
            return ""
        if isinstance(value, str) and not case_sensitive:
            return value.lower()
        return value

    @classmethod
    def matches(
        cls,
        left: t.OracleWms.FilterRecordValue | None,
        operator: c.OracleWms.WmsFilterOperator | str,
        right: t.OracleWms.FilterValues,
        *,
        case_sensitive: bool,
    ) -> bool:
        """Match one operator, including null semantics.

        Returns:
            Whether the value matches.

        """
        resolved = cls.resolve(operator)
        if resolved is None or (left is None) != (right is None):
            return False
        if left is None:
            return resolved in c.OracleWms.NULL_MATCHING_OPERATORS
        match resolved:
            case c.OracleWms.WmsFilterOperator.EQ:
                result = cls.normalize(left, case_sensitive=case_sensitive) == (
                    cls.normalize(right, case_sensitive=case_sensitive)
                )
            case c.OracleWms.WmsFilterOperator.NE:
                result = cls.normalize(left, case_sensitive=case_sensitive) != (
                    cls.normalize(right, case_sensitive=case_sensitive)
                )
            case c.OracleWms.WmsFilterOperator.IN:
                result = isinstance(right, list) and str(left) in [
                    str(item) for item in right
                ]
            case c.OracleWms.WmsFilterOperator.CONTAINS:
                result = isinstance(left, str) and str(right) in left
            case _:
                result = (
                    type(left) is type(right)
                    and resolved in c.OracleWms.ORDERING_SYMBOLS
                    and cls.compare(
                        left,
                        right,
                        c.OracleWms.ORDERING_SYMBOLS[resolved],
                    )
                )
        return result

    @staticmethod
    def path(
        record: t.OracleWms.FilterRecord,
        field: str,
    ) -> t.OracleWms.NestedFilterValue | None:
        """Resolve a dot path, falling back to its flattened key.

        Returns:
            The resolved value or ``None``.

        """
        keys = field.split(".")
        current: t.OracleWms.NestedFilterValue | None = record
        for key in keys:
            if not isinstance(current, Mapping):
                break
            current = current.get(key)
            if current is None:
                break
        else:
            return None if isinstance(current, Mapping) else current
        flat = record.get("_".join(keys)) if len(keys) > 1 else None
        return flat if not isinstance(flat, Mapping) else None

    @staticmethod
    def _scalar(
        value: t.OracleWms.FilterRecordValue | None,
    ) -> t.Scalar | None:
        return value if isinstance(value, c.SCALAR_TYPES) else None


__all__: list[str] = ["FlextOracleWmsUtilitiesFilteringOperators"]
