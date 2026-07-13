"""Behavioral tests for Oracle WMS utilities public contract.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import pytest

from flext_core import u as core_u
from flext_oracle_wms import c, e, m
from flext_oracle_wms.errors import FlextOracleWmsErrors
from tests import t, u

__all__: list[str] = ["TestsFlextOracleWmsHelpers"]


@pytest.mark.unit
class TestsFlextOracleWmsHelpers:
    """Behavioral contract of FlextOracleWmsUtilities (public utilities facade)."""

    @pytest.fixture
    def records(self) -> list[t.OracleWms.Tests.Record]:
        """Three ordered records exercised by the filtering contract."""
        return [
            {"id": 1, "name": "Alpha"},
            {"id": 2, "name": "beta"},
            {"id": 5, "name": "Gamma"},
        ]

    # ---- facade contract -------------------------------------------------

    def test_utilities_facade_inherits_flext_core_utilities(self) -> None:
        """The facade composes flext-core utilities via MRO."""
        assert issubclass(u, core_u)

    def test_filter_engine_reachable_through_public_namespace(self) -> None:
        """Filtering engine is exposed on both the facade and OracleWms namespace."""
        assert u.Filter is u.OracleWms.Filter

    # ---- conversion helpers ---------------------------------------------

    @pytest.mark.parametrize(
        ("value", "default", "expected"),
        [
            (123, "", "123"),
            (None, "fallback", "fallback"),
            ("kept", "", "kept"),
        ],
    )
    def test_to_str_returns_string_or_default(
        self,
        value: str | int | None,
        default: str,
        expected: str,
    ) -> None:
        """to_str stringifies present values and substitutes the default for None."""
        assert u.to_str(value, default=default) == expected

    # ---- filter_by_field -------------------------------------------------

    def test_filter_by_field_keeps_only_matching_records(
        self,
        records: list[t.OracleWms.Tests.Record],
    ) -> None:
        """Equality filtering yields exactly the records whose field matches."""
        result = u.Filter.filter_by_field(records, "name", "beta")

        assert result.success
        assert [row["id"] for row in result.unwrap()] == [2]

    def test_filter_by_field_with_operator_applies_comparison(
        self,
        records: list[t.OracleWms.Tests.Record],
    ) -> None:
        """A GTE operator keeps records at or above the threshold."""
        result = u.Filter.filter_by_field(
            records,
            "id",
            2,
            operator=c.OracleWms.WmsFilterOperator.GTE,
        )

        assert result.success
        assert [row["id"] for row in result.unwrap()] == [2, 5]

    # ---- filter_by_id_range ---------------------------------------------

    @pytest.mark.parametrize(
        ("min_id", "max_id", "expected"),
        [
            (2, None, [2, 5]),
            (None, 2, [1, 2]),
            (2, 2, [2]),
            (None, None, [1, 2, 5]),
        ],
    )
    def test_filter_by_id_range_is_inclusive(
        self,
        records: list[t.OracleWms.Tests.Record],
        min_id: int | None,
        max_id: int | None,
        expected: list[int],
    ) -> None:
        """Identifier range filtering is inclusive on both bounds."""
        result = u.Filter.filter_by_id_range(
            records,
            "id",
            min_id=min_id,
            max_id=max_id,
        )

        assert result.success
        assert [row["id"] for row in result.unwrap()] == expected

    def test_filter_by_id_range_on_empty_input_returns_empty(self) -> None:
        """Filtering an empty collection succeeds with an empty result."""
        result = u.Filter.filter_by_id_range([], "id", min_id=1)

        assert result.success
        assert result.unwrap() == []

    # ---- create_filter / instance state ---------------------------------

    def test_create_filter_exposes_requested_configuration(self) -> None:
        """The engine reports the configuration it was created with."""
        engine = u.Filter.create_filter(case_sensitive=True, max_conditions=10)

        assert isinstance(engine, u.Filter)
        assert engine.case_sensitive is True
        assert engine.max_conditions == 10

    @pytest.mark.parametrize(
        "max_conditions", [0, -1, c.OracleWms.Filtering.MAX_FILTER_CONDITIONS + 1]
    )
    def test_create_filter_rejects_out_of_range_limits(
        self,
        max_conditions: int,
    ) -> None:
        """Out-of-range condition limits fail loudly via the exception family."""
        with pytest.raises(e.BaseError):
            u.Filter.create_filter(max_conditions=max_conditions)

    def test_constructor_rejects_filters_exceeding_condition_limit(self) -> None:
        """Building an engine with too many conditions raises a validation error."""
        with pytest.raises(FlextOracleWmsErrors.ValidationError):
            u.Filter(
                filters={
                    "id": m.OracleWms.FlextOracleWmsOperatorFilter(
                        operator=c.OracleWms.WmsFilterOperator.IN,
                        value=[1, 2, 3],
                    ),
                },
                max_conditions=1,
            )

    # ---- case sensitivity ------------------------------------------------

    def test_case_insensitive_engine_matches_regardless_of_case(
        self,
        records: list[t.OracleWms.Tests.Record],
    ) -> None:
        """Default (case-insensitive) matching ignores letter case."""
        engine = u.Filter.create_filter()

        result = engine.filter_records(records, {"name": "ALPHA"})

        assert result.success
        assert [row["id"] for row in result.unwrap()] == [1]

    def test_case_sensitive_engine_requires_exact_case(
        self,
        records: list[t.OracleWms.Tests.Record],
    ) -> None:
        """A case-sensitive engine rejects a case mismatch."""
        engine = u.Filter.create_filter(case_sensitive=True)

        result = engine.filter_records(records, {"name": "ALPHA"})

        assert result.success
        assert result.unwrap() == []

    # ---- filter_records limit and validation ----------------------------

    def test_filter_records_respects_limit(
        self,
        records: list[t.OracleWms.Tests.Record],
    ) -> None:
        """The optional limit truncates the matched records."""
        engine = u.Filter.create_filter()

        result = engine.filter_records(records, {}, limit=2)

        assert result.success
        assert len(result.unwrap()) == 2

    def test_filter_records_reports_condition_overflow_as_failure(
        self,
        records: list[t.OracleWms.Tests.Record],
    ) -> None:
        """Exceeding max_conditions returns a failure result, not a raise."""
        engine = u.Filter.create_filter(max_conditions=1)

        result = engine.filter_records(
            records,
            {
                "id": m.OracleWms.FlextOracleWmsOperatorFilter(
                    operator=c.OracleWms.WmsFilterOperator.IN,
                    value=[1, 2, 5],
                ),
            },
        )

        assert result.failure
        assert "Too many conditions" in (result.error or "")

    # ---- sort_records ----------------------------------------------------

    @pytest.mark.parametrize(
        ("ascending", "expected"),
        [
            (True, [1, 5, 2]),
            (False, [2, 5, 1]),
        ],
    )
    def test_sort_records_orders_by_field(
        self,
        records: list[t.OracleWms.Tests.Record],
        *,
        ascending: bool,
        expected: list[int],
    ) -> None:
        """Sorting orders records by the requested field in the given direction."""
        engine = u.Filter.create_filter()

        result = engine.sort_records(records, "name", ascending=ascending)

        assert result.success
        assert [row["id"] for row in result.unwrap()] == expected
