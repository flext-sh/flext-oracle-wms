"""Behavioral tests for the Oracle WMS filtering utility.

Exercises the PUBLIC contract of ``FlextOracleWmsUtilitiesFiltering.Filter``
through its observable surface only:

- construction / configuration validation (raised FlextExceptions family)
- ``filter_records`` -> ``r[Sequence]`` (scalar, list, operator, nested, limits)
- ``sort_records`` -> ``r[Sequence]`` (ordering, None handling, missing field)
- ``filter_by_field`` / ``filter_by_id_range`` classmethod helpers

No private attribute/method is touched: operator semantics, normalization,
nested-path resolution and range checks are all asserted via the public
filtering results they produce.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from flext_tests import e

from flext_oracle_wms import FlextOracleWmsUtilitiesFiltering
from flext_oracle_wms.errors import FlextOracleWmsErrors
from tests import c, m

if TYPE_CHECKING:
    from tests import t

Filter = FlextOracleWmsUtilitiesFiltering.Filter
Operator = m.OracleWms.FlextOracleWmsOperatorFilter
Op = c.OracleWms.WmsFilterOperator


class TestsFlextOracleWmsFiltering:
    """Behavioral contract of the Oracle WMS filtering utility."""

    # ------------------------------------------------------------------ #
    # Shared test data (public record shape).
    # ------------------------------------------------------------------ #
    @property
    def sample_records(self) -> list[t.OracleWms.FilterRecord]:
        """Four records with a stable, well-known id/status/score layout."""
        return [
            {"id": 1, "name": "Company A", "status": "active", "score": 85.5},
            {"id": 2, "name": "Company B", "status": "inactive", "score": 72.0},
            {"id": 3, "name": "Company C", "status": "active", "score": 90.0},
            {"id": 4, "name": "Company D", "status": "pending", "score": 65.5},
        ]

    def _ids(self, records: t.SequenceOf[t.OracleWms.FilterRecord]) -> set[int]:
        """Collect the ``id`` field of every record for set comparison."""
        ids: set[int] = set()
        for record in records:
            id_value = record["id"]
            assert isinstance(id_value, int)
            ids.add(id_value)
        return ids

    # ------------------------------------------------------------------ #
    # Construction / configuration contract.
    # ------------------------------------------------------------------ #
    def test_construction_exposes_configuration(self) -> None:
        engine = Filter(case_sensitive=True, max_conditions=25)
        assert engine.case_sensitive is True
        assert engine.max_conditions == 25

    def test_construction_defaults_are_case_insensitive(self) -> None:
        engine = Filter()
        assert engine.case_sensitive is False
        assert engine.max_conditions == c.OracleWms.Filtering.MAX_FILTER_CONDITIONS

    @pytest.mark.parametrize(
        "max_conditions",
        [0, -1, c.OracleWms.Filtering.MAX_FILTER_CONDITIONS + 1],
    )
    def test_construction_rejects_invalid_max_conditions(
        self,
        max_conditions: int,
    ) -> None:
        with pytest.raises(e.BaseError, match="Invalid max_conditions"):
            Filter(max_conditions=max_conditions)

    @pytest.mark.parametrize(
        "max_conditions",
        [0, c.OracleWms.Filtering.MAX_FILTER_CONDITIONS + 1],
    )
    def test_create_filter_rejects_invalid_max_conditions(
        self,
        max_conditions: int,
    ) -> None:
        with pytest.raises(e.BaseError, match="Invalid max_conditions"):
            Filter.create_filter(max_conditions=max_conditions)

    def test_create_filter_matches_constructor_contract(self) -> None:
        engine = Filter.create_filter(case_sensitive=True, max_conditions=10)
        assert engine.case_sensitive is True
        assert engine.max_conditions == 10

    def test_construction_accepts_valid_initial_filters(self) -> None:
        engine = Filter(filters={"status": "active"}, max_conditions=5)
        result = engine.filter_records(self.sample_records, {"status": "active"})
        assert result.success
        assert self._ids(result.value) == {1, 3}

    def test_construction_rejects_initial_filters_over_limit(self) -> None:
        filters: t.MappingKV[str, t.OracleWms.FilterEntry] = {
            "field1": "v1",
            "field2": "v2",
            "field3": "v3",
            "field4": "v4",
        }
        with pytest.raises(FlextOracleWmsErrors.ValidationError):
            Filter(filters=filters, max_conditions=3)

    # ------------------------------------------------------------------ #
    # filter_records: scalar / list / limit / empty.
    # ------------------------------------------------------------------ #
    def test_empty_filters_returns_all_records_unchanged(self) -> None:
        engine = Filter()
        result = engine.filter_records(self.sample_records, {})
        assert result.success
        assert list(result.value) == self.sample_records

    def test_scalar_equality_selects_matching_records(self) -> None:
        engine = Filter()
        result = engine.filter_records(self.sample_records, {"status": "active"})
        assert result.success
        assert self._ids(result.value) == {1, 3}

    def test_numeric_equality_selects_single_record(self) -> None:
        engine = Filter()
        result = engine.filter_records(self.sample_records, {"id": 2})
        assert result.success
        assert self._ids(result.value) == {2}

    def test_list_value_matches_membership(self) -> None:
        engine = Filter()
        result = engine.filter_records(
            self.sample_records,
            {"status": ["active", "pending"]},
        )
        assert result.success
        assert self._ids(result.value) == {1, 3, 4}

    def test_no_matching_records_yields_empty_success(self) -> None:
        engine = Filter()
        result = engine.filter_records(self.sample_records, {"status": "gone"})
        assert result.success
        assert not result.value

    def test_limit_truncates_result_set(self) -> None:
        engine = Filter()
        result = engine.filter_records(
            self.sample_records,
            {"status": "active"},
            limit=1,
        )
        assert result.success
        assert len(result.value) == 1
        assert result.value[0]["status"] == "active"

    def test_limit_applied_over_large_record_set(self) -> None:
        records: list[t.OracleWms.FilterRecord] = [
            {"id": i, "status": "active" if i % 2 == 0 else "inactive"}
            for i in range(1000)
        ]
        engine = Filter()
        result = engine.filter_records(records, {"status": "active"}, limit=100)
        assert result.success
        assert len(result.value) == 100
        assert all(record["status"] == "active" for record in result.value)

    # ------------------------------------------------------------------ #
    # Case sensitivity / normalization (observed through equality).
    # ------------------------------------------------------------------ #
    def test_default_equality_is_case_insensitive(self) -> None:
        engine = Filter(case_sensitive=False)
        result = engine.filter_records(self.sample_records, {"status": "ACTIVE"})
        assert result.success
        assert self._ids(result.value) == {1, 3}

    def test_case_sensitive_equality_respects_case(self) -> None:
        engine = Filter(case_sensitive=True)
        result = engine.filter_records(self.sample_records, {"status": "ACTIVE"})
        assert result.success
        assert not result.value

    def test_case_insensitive_equality_folds_unicode(self) -> None:
        engine = Filter(case_sensitive=False)
        records: list[t.OracleWms.FilterRecord] = [{"id": 1, "name": "Café"}]
        result = engine.filter_records(records, {"name": "café"})
        assert result.success
        assert self._ids(result.value) == {1}

    # ------------------------------------------------------------------ #
    # Operator-dict conditions (eq/ne/in/contains/gt/gte/lt/lte/unknown).
    # ------------------------------------------------------------------ #
    @pytest.mark.parametrize(
        ("operator", "value", "expected_ids"),
        [
            ("gt", 80.0, {1, 3}),
            ("gte", 85.5, {1, 3}),
            ("lt", 72.0, {4}),
            ("lte", 72.0, {2, 4}),
        ],
    )
    def test_numeric_comparison_operators_select_range(
        self,
        operator: str,
        value: float,
        expected_ids: set[int],
    ) -> None:
        engine = Filter()
        result = engine.filter_records(
            self.sample_records,
            {"score": Operator(operator=operator, value=value)},
        )
        assert result.success
        assert self._ids(result.value) == expected_ids

    def test_eq_operator_dict_matches_value(self) -> None:
        engine = Filter()
        result = engine.filter_records(
            self.sample_records,
            {"status": Operator(operator="eq", value="active")},
        )
        assert result.success
        assert self._ids(result.value) == {1, 3}

    def test_ne_operator_dict_excludes_value(self) -> None:
        engine = Filter()
        result = engine.filter_records(
            self.sample_records,
            {"status": Operator(operator="ne", value="inactive")},
        )
        assert result.success
        assert self._ids(result.value) == {1, 3, 4}

    def test_in_operator_dict_matches_membership(self) -> None:
        engine = Filter()
        result = engine.filter_records(
            self.sample_records,
            {"status": Operator(operator="in", value=["active", "pending"])},
        )
        assert result.success
        assert self._ids(result.value) == {1, 3, 4}

    def test_contains_operator_dict_matches_substring(self) -> None:
        engine = Filter()
        result = engine.filter_records(
            self.sample_records,
            {"name": Operator(operator="contains", value="Company B")},
        )
        assert result.success
        assert self._ids(result.value) == {2}

    def test_unknown_operator_matches_nothing(self) -> None:
        engine = Filter()
        result = engine.filter_records(
            self.sample_records,
            {"status": Operator(operator="mystery", value="active")},
        )
        assert result.success
        assert not result.value

    def test_comparison_requires_matching_types(self) -> None:
        """A numeric ``gt`` filter must not match a stringified field value."""
        engine = Filter()
        records: list[t.OracleWms.FilterRecord] = [{"id": 1, "score": "10"}]
        result = engine.filter_records(
            records,
            {"score": Operator(operator="gt", value=5.0)},
        )
        assert result.success
        assert not result.value

    def test_none_field_does_not_match_valued_condition(self) -> None:
        engine = Filter()
        records: list[t.OracleWms.FilterRecord] = [{"id": 1, "score": None}]
        result = engine.filter_records(
            records,
            {"score": Operator(operator="gt", value=5.0)},
        )
        assert result.success
        assert not result.value

    def test_none_field_does_not_match_list_condition(self) -> None:
        engine = Filter()
        records: list[t.OracleWms.FilterRecord] = [{"id": 1, "status": None}]
        result = engine.filter_records(records, {"status": ["a", "b"]})
        assert result.success
        assert not result.value

    # ------------------------------------------------------------------ #
    # Nested / dotted path resolution (observed through matching).
    # ------------------------------------------------------------------ #
    def test_dotted_path_resolves_nested_mapping(self) -> None:
        engine = Filter()
        records: list[t.OracleWms.FilterRecord] = [
            {"id": 1, "company": {"city": "New York"}},
            {"id": 2, "company": {"city": "London"}},
        ]
        result = engine.filter_records(records, {"company.city": "New York"})
        assert result.success
        assert self._ids(result.value) == {1}

    def test_dotted_path_falls_back_to_flattened_key(self) -> None:
        engine = Filter()
        records: list[t.OracleWms.FilterRecord] = [
            {"id": 1, "company_address_city": "New York"},
            {"id": 2, "company_address_city": "London"},
        ]
        result = engine.filter_records(
            records,
            {"company.address.city": "London"},
        )
        assert result.success
        assert self._ids(result.value) == {2}

    def test_missing_field_matches_no_records(self) -> None:
        engine = Filter()
        result = engine.filter_records(
            self.sample_records,
            {"nonexistent": "whatever"},
        )
        assert result.success
        assert not result.value

    # ------------------------------------------------------------------ #
    # Condition-count validation (observed through failure result).
    # ------------------------------------------------------------------ #
    def test_scalar_conditions_over_limit_fail(self) -> None:
        engine = Filter(max_conditions=1)
        result = engine.filter_records(self.sample_records, {"a": "1", "b": "2"})
        assert result.failure
        assert result.error is not None
        assert "Too many" in result.error

    def test_list_condition_counted_by_length(self) -> None:
        engine = Filter(max_conditions=2)
        result = engine.filter_records(
            self.sample_records,
            {"status": ["a", "b", "c"]},
        )
        assert result.failure
        assert result.error is not None
        assert "Too many" in result.error

    # ------------------------------------------------------------------ #
    # filter_by_field classmethod helper.
    # ------------------------------------------------------------------ #
    def test_filter_by_field_scalar_default_operator(self) -> None:
        result = Filter.filter_by_field(self.sample_records, "status", "active")
        assert result.success
        assert self._ids(result.value) == {1, 3}

    def test_filter_by_field_numeric_value(self) -> None:
        result = Filter.filter_by_field(self.sample_records, "id", 2)
        assert result.success
        assert self._ids(result.value) == {2}

    def test_filter_by_field_explicit_operator(self) -> None:
        result = Filter.filter_by_field(
            self.sample_records,
            "status",
            "inactive",
            Op.NE,
        )
        assert result.success
        assert self._ids(result.value) == {1, 3, 4}

    # ------------------------------------------------------------------ #
    # filter_by_id_range classmethod helper.
    # ------------------------------------------------------------------ #
    def test_id_range_both_bounds_inclusive(self) -> None:
        result = Filter.filter_by_id_range(
            self.sample_records,
            "id",
            min_id=2,
            max_id=3,
        )
        assert result.success
        assert self._ids(result.value) == {2, 3}

    def test_id_range_min_only(self) -> None:
        result = Filter.filter_by_id_range(self.sample_records, "id", min_id=3)
        assert result.success
        assert self._ids(result.value) == {3, 4}

    def test_id_range_max_only(self) -> None:
        result = Filter.filter_by_id_range(self.sample_records, "id", max_id=2)
        assert result.success
        assert self._ids(result.value) == {1, 2}

    def test_id_range_no_bounds_returns_all(self) -> None:
        result = Filter.filter_by_id_range(self.sample_records, "id")
        assert result.success
        assert self._ids(result.value) == {1, 2, 3, 4}

    def test_id_range_on_string_field(self) -> None:
        result = Filter.filter_by_id_range(
            self.sample_records,
            "name",
            min_id="Company C",
        )
        assert result.success
        assert self._ids(result.value) == {3, 4}

    def test_id_range_empty_records(self) -> None:
        result = Filter.filter_by_id_range([], "id", min_id=1)
        assert result.success
        assert not result.value

    # ------------------------------------------------------------------ #
    # sort_records.
    # ------------------------------------------------------------------ #
    @property
    def unsorted_records(self) -> list[t.OracleWms.FilterRecord]:
        return [
            {"id": 3, "name": "Charlie", "score": 75.5},
            {"id": 1, "name": "Alice", "score": 90.0},
            {"id": 2, "name": "Bob", "score": 85.0},
        ]

    @pytest.mark.parametrize(
        ("field", "ascending", "expected"),
        [
            ("name", True, ["Alice", "Bob", "Charlie"]),
            ("name", False, ["Charlie", "Bob", "Alice"]),
        ],
    )
    def test_sort_by_string_field(
        self,
        field: str,
        ascending: bool,
        expected: list[str],
    ) -> None:
        engine = Filter()
        result = engine.sort_records(self.unsorted_records, field, ascending=ascending)
        assert result.success
        assert [record[field] for record in result.value] == expected

    @pytest.mark.parametrize(
        ("field", "ascending", "expected"),
        [
            ("id", True, [1, 2, 3]),
            ("score", False, [90.0, 85.0, 75.5]),
        ],
    )
    def test_sort_by_numeric_field(
        self,
        field: str,
        ascending: bool,
        expected: list[float],
    ) -> None:
        engine = Filter()
        result = engine.sort_records(self.unsorted_records, field, ascending=ascending)
        assert result.success
        assert [record[field] for record in result.value] == expected

    def test_sort_preserves_all_records_with_none_values(self) -> None:
        records: list[t.OracleWms.FilterRecord] = [
            {"id": 1, "name": "Alice", "score": None},
            {"id": 2, "name": "Bob", "score": 85.0},
            {"id": 3, "name": None, "score": 90.0},
        ]
        engine = Filter()
        result = engine.sort_records(records, "name")
        assert result.success
        assert self._ids(result.value) == {1, 2, 3}

    def test_sort_by_missing_field_keeps_all_records(self) -> None:
        engine = Filter()
        result = engine.sort_records(self.unsorted_records, "nonexistent")
        assert result.success
        assert self._ids(result.value) == {1, 2, 3}

    def test_sort_empty_records_returns_empty_success(self) -> None:
        engine = Filter()
        result = engine.sort_records([], "any_field")
        assert result.success
        assert not result.value


__all__: list[str] = ["TestsFlextOracleWmsFiltering"]
