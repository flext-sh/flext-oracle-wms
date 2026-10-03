"""Behavioral tests for Oracle WMS utilities public contract.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import pytest
from flext_tests import tm

from flext_oracle_wms.errors import FlextOracleWmsErrors
from tests import c, e, m, t, u


@pytest.mark.unit
class TestsFlextOracleWmsHelpers:
    """Behavioral contract of FlextOracleWmsUtilities (public utilities facade)."""

    @staticmethod
    @pytest.fixture
    def records() -> list[t.OracleWms.Tests.Record]:
        """Three ordered records exercised by the filtering contract.

        Returns:
            The resulting ``list[t.OracleWms.Tests.Record]``.
        """
        return [
            {"id": 1, "name": "Alpha"},
            {"id": 2, "name": "beta"},
            {"id": 5, "name": "Gamma"},
        ]

    # ---- facade contract -------------------------------------------------

    @staticmethod
    def test_utilities_facade_inherits_flext_core_utilities() -> None:
        """The facade composes flext-core utilities via MRO."""
        assert issubclass(u, u)

    @staticmethod
    def test_filter_engine_reachable_through_public_namespace() -> None:
        """Filtering engine is exposed on both the facade and OracleWms namespace."""
        assert u.Filter is u.OracleWms.Filter

    # ---- conversion helpers ---------------------------------------------

    @staticmethod
    @pytest.mark.parametrize(
        ("value", "default", "expected"),
        [(123, "", "123"), (None, "fallback", "fallback"), ("kept", "", "kept")],
    )
    def test_to_str_returns_string_or_default(
        value: str | int | None,
        default: str,
        expected: str,
    ) -> None:
        """to_str stringifies present values and substitutes the default for None."""
        tm.that(u.to_str(value, default=default), eq=expected)

    # ---- filter_by_field -------------------------------------------------

    @staticmethod
    def test_filter_by_field_keeps_only_matching_records(
        records: list[t.OracleWms.Tests.Record],
    ) -> None:
        """Equality filtering yields exactly the records whose field matches."""
        result = u.Filter.filter_by_field(records, "name", "beta")

        tm.ok(result)
        tm.that([row["id"] for row in result.unwrap()], eq=[2])

    @staticmethod
    def test_filter_by_field_with_operator_applies_comparison(
        records: list[t.OracleWms.Tests.Record],
    ) -> None:
        """A GTE operator keeps records at or above the threshold."""
        result = u.Filter.filter_by_field(
            records,
            "id",
            2,
            operator=c.OracleWms.WmsFilterOperator.GTE,
        )

        tm.ok(result)
        tm.that([row["id"] for row in result.unwrap()], eq=[2, 5])

    # ---- filter_by_id_range ---------------------------------------------

    @staticmethod
    @pytest.mark.parametrize(
        ("min_id", "max_id", "expected"),
        [(2, None, [2, 5]), (None, 2, [1, 2]), (2, 2, [2]), (None, None, [1, 2, 5])],
    )
    def test_filter_by_id_range_is_inclusive(
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

        tm.ok(result)
        tm.that([row["id"] for row in result.unwrap()], eq=expected)

    @staticmethod
    def test_filter_by_id_range_on_empty_input_returns_empty() -> None:
        """Filtering an empty collection succeeds with an empty result."""
        result = u.Filter.filter_by_id_range([], "id", min_id=1)

        tm.ok(result)
        tm.that(result.unwrap(), eq=[])

    # ---- create_filter / instance state ---------------------------------

    @staticmethod
    def test_create_filter_exposes_requested_configuration() -> None:
        """The engine reports the configuration it was created with."""
        engine = u.Filter.create_filter(case_sensitive=True, max_conditions=10)

        tm.that(engine, is_=u.Filter)
        tm.that(engine.case_sensitive, eq=True)
        tm.that(engine.max_conditions, eq=10)

    @staticmethod
    @pytest.mark.parametrize(
        "max_conditions",
        [0, -1, c.OracleWms.Filtering.MAX_FILTER_CONDITIONS + 1],
    )
    def test_create_filter_rejects_out_of_range_limits(
        max_conditions: int,
    ) -> None:
        """Out-of-range condition limits fail loudly via the exception family."""
        with pytest.raises(e.BaseError):
            u.Filter.create_filter(max_conditions=max_conditions)

    @staticmethod
    def test_constructor_rejects_filters_exceeding_condition_limit() -> None:
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

    @staticmethod
    def test_case_insensitive_engine_matches_regardless_of_case(
        records: list[t.OracleWms.Tests.Record],
    ) -> None:
        """Default (case-insensitive) matching ignores letter case."""
        engine = u.Filter.create_filter()

        result = engine.filter_records(records, {"name": "ALPHA"})

        tm.ok(result)
        tm.that([row["id"] for row in result.unwrap()], eq=[1])

    @staticmethod
    def test_case_sensitive_engine_requires_exact_case(
        records: list[t.OracleWms.Tests.Record],
    ) -> None:
        """A case-sensitive engine rejects a case mismatch."""
        engine = u.Filter.create_filter(case_sensitive=True)

        result = engine.filter_records(records, {"name": "ALPHA"})

        tm.ok(result)
        tm.that(result.unwrap(), eq=[])

    # ---- filter_records limit and validation ----------------------------

    @staticmethod
    def test_filter_records_respects_limit(
        records: list[t.OracleWms.Tests.Record],
    ) -> None:
        """The optional limit truncates the matched records."""
        engine = u.Filter.create_filter()

        result = engine.filter_records(records, {}, limit=2)

        tm.ok(result)
        tm.that(len(result.unwrap()), eq=2)

    @staticmethod
    def test_filter_records_reports_condition_overflow_as_failure(
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

        tm.fail(result)
        tm.that((result.error or ""), has="Too many conditions")

    # ---- sort_records ----------------------------------------------------

    @staticmethod
    @pytest.mark.parametrize(
        ("ascending", "expected"),
        [(True, [1, 5, 2]), (False, [2, 5, 1])],
    )
    def test_sort_records_orders_by_field(
        records: list[t.OracleWms.Tests.Record],
        *,
        ascending: bool,
        expected: list[int],
    ) -> None:
        """Sorting orders records by the requested field in the given direction."""
        engine = u.Filter.create_filter()

        result = engine.sort_records(records, "name", ascending=ascending)

        tm.ok(result)
        tm.that([row["id"] for row in result.unwrap()], eq=expected)
