"""Oracle WMS Filtering utilities.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from flext_api import u
from flext_core import e, r

from flext_oracle_wms._utilities import (
    FlextOracleWmsUtilitiesFilteringOperators as Operators,
)
from flext_oracle_wms.constants import c
from flext_oracle_wms.errors import FlextOracleWmsErrors
from flext_oracle_wms.models import m
from flext_oracle_wms.protocols import p
from flext_oracle_wms.typings import t


class FlextOracleWmsUtilitiesFiltering:
    """Filtering utilities for Oracle WMS -- u.OracleWms.Filtering.*."""

    class Filter:
        """Filter engine: construction, matching and sorting over records."""

        logger = u.fetch_logger(__name__)

        def __init__(
            self,
            *,
            filters: Mapping[str, t.OracleWms.FilterEntry] | None = None,
            case_sensitive: bool = False,
            max_conditions: int = c.OracleWms.Filtering.MAX_FILTER_CONDITIONS,
        ) -> None:
            """Initialize the engine with strict condition limits.

            Raises:
                BaseError: If ``max_conditions`` is invalid.
                ValidationError: If the initial filters exceed the limit.

            """
            if not 0 < max_conditions <= c.OracleWms.Filtering.MAX_FILTER_CONDITIONS:
                invalid_limit = "Invalid max_conditions"
                raise e.BaseError(invalid_limit)
            self.max_conditions: int = max_conditions
            self.case_sensitive: bool = case_sensitive
            self.filters: Mapping[str, t.OracleWms.FilterEntry] = filters or {}
            if self.filters and self._total(self.filters) > max_conditions:
                invalid_filters = "Filter validation failed"
                raise FlextOracleWmsErrors.ValidationError(invalid_filters)

        @classmethod
        def create_filter(
            cls,
            *,
            case_sensitive: bool = False,
            max_conditions: int = c.OracleWms.Filtering.MAX_FILTER_CONDITIONS,
        ) -> FlextOracleWmsUtilitiesFiltering.Filter:
            """Create an engine with explicit configuration.

            Returns:
                The configured filter engine.

            """
            return cls(case_sensitive=case_sensitive, max_conditions=max_conditions)

        @classmethod
        def filter_by_field(
            cls,
            records: Sequence[t.OracleWms.FilterRecord],
            field: str,
            value: t.OracleWms.FilterScalar,
            operator: c.OracleWms.WmsFilterOperator | None = None,
        ) -> p.Result[Sequence[t.OracleWms.FilterRecord]]:
            """Filter records by one field using optional operator semantics.

            Returns:
                The filtered records.

            """
            model = m.OracleWms.FlextOracleWmsOperatorFilter
            entry: t.OracleWms.FilterEntry = (
                value if operator is None else model(operator=operator, value=value)
            )
            return cls().filter_records(records, {field: entry})

        @classmethod
        def filter_by_id_range(
            cls,
            records: Sequence[t.OracleWms.FilterRecord],
            id_field: str,
            min_id: t.OracleWms.FilterScalar | None = None,
            max_id: t.OracleWms.FilterScalar | None = None,
        ) -> p.Result[Sequence[t.OracleWms.FilterRecord]]:
            """Filter records by an inclusive identifier range.

            Returns:
                The filtered records.

            """
            selected: Sequence[t.OracleWms.FilterRecord] = [
                record
                for record in records
                if (value := record.get(id_field)) is not None
                and (min_id is None or Operators.compare(value, min_id, ">="))
                and (max_id is None or Operators.compare(value, max_id, "<="))
            ]
            return r[Sequence[t.OracleWms.FilterRecord]].ok(selected)

        def filter_records(
            self,
            records: Sequence[t.OracleWms.FilterRecord],
            filters: Mapping[str, t.OracleWms.FilterEntry],
            limit: int | None = None,
        ) -> p.Result[Sequence[t.OracleWms.FilterRecord]]:
            """Filter records against field conditions and an optional limit.

            Returns:
                The filtered records.

            """
            total = self._total(filters)
            if total > self.max_conditions:
                return r[Sequence[t.OracleWms.FilterRecord]].fail(
                    f"Too many conditions. Max: {self.max_conditions}, Got: {total}",
                )
            self.filters = filters
            matched: Sequence[t.OracleWms.FilterRecord] = [
                record for record in records if self._matches(record, filters)
            ][:limit]
            return r[Sequence[t.OracleWms.FilterRecord]].ok(matched)

        def sort_records(
            self,
            records: Sequence[t.OracleWms.FilterRecord],
            sort_field: str,
            *,
            ascending: bool = True,
        ) -> p.Result[Sequence[t.OracleWms.FilterRecord]]:
            """Sort records by a dot-path field.

            Returns:
                The sorted records.

            """
            try:
                missing = "" if ascending else "zzz"

                def sort_key(record: t.OracleWms.FilterRecord) -> str:
                    value = Operators.path(record, sort_field)
                    return str(missing if value is None else value)

                return r[Sequence[t.OracleWms.FilterRecord]].ok(
                    sorted(records, key=sort_key, reverse=not ascending),
                )
            except Exception as exc:
                self.logger.exception("Sort failed")
                return r[Sequence[t.OracleWms.FilterRecord]].fail_op("Sort", exc)

        @staticmethod
        def _total(filters: Mapping[str, t.OracleWms.FilterEntry]) -> int:
            return sum(Operators.size(entry) for entry in filters.values())

        def _matches(
            self,
            record: t.OracleWms.FilterRecord,
            filters: Mapping[str, t.OracleWms.FilterEntry],
        ) -> bool:
            return all(
                self._matches_entry(record, field, entry)
                for field, entry in filters.items()
            )

        def _matches_entry(
            self,
            record: t.OracleWms.FilterRecord,
            field: str,
            entry: t.OracleWms.FilterEntry,
        ) -> bool:
            value = Operators.path(record, field)
            if isinstance(entry, m.OracleWms.FlextOracleWmsOperatorFilter):
                return Operators.matches(
                    value,
                    entry.operator,
                    entry.value,
                    case_sensitive=self.case_sensitive,
                )
            if isinstance(entry, list):
                return value is not None and value in entry
            return Operators.normalize(
                value, case_sensitive=self.case_sensitive
            ) == Operators.normalize(entry, case_sensitive=self.case_sensitive)


__all__: list[str] = ["FlextOracleWmsUtilitiesFiltering"]
