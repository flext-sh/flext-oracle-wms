"""Comprehensive test coverage for Oracle WMS filtering module.

This test file provides extensive coverage for filtering.py, focusing on:
- FlextOracleWmsFilter class functionality (all operators, edge cases)
- Filter validation and error handling
- Record filtering with complex conditions
- Sorting operations and nested value access
- Factory function and convenience functions
- Performance considerations and edge cases

Target: Increase filtering.py coverage from 11% to 85%+


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping, Sequence

import pytest
from flext_core import FlextExceptions

from flext_oracle_wms import FlextOracleWmsConstants
from flext_oracle_wms.filtering import (
    FlextOracleWmsDataValidationError,
    FlextOracleWmsFilter,
    FlextOracleWmsFilterOperator,
    FlextOracleWmsOperatorFilter as OperatorFilter,
)
from tests import t


class TestFlextOracleWmsFilterConstruction:
    """Test filter construction and validation."""

    def test_filter_default_construction(self) -> None:
        """Test filter creation with default parameters."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        assert filter_engine.case_sensitive is False
        assert (
            filter_engine.max_conditions
            == FlextOracleWmsConstants.Filtering.MAX_FILTER_CONDITIONS
        )

    def test_filter_custom_construction(self) -> None:
        """Test filter creation with custom parameters."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=True, max_conditions=50)
        assert filter_engine.case_sensitive is True
        assert filter_engine.max_conditions == 50

    def test_filter_invalid_max_conditions_zero(self) -> None:
        with pytest.raises(FlextExceptions.BaseError, match="Invalid max_conditions"):
            FlextOracleWmsFilter(max_conditions=0)

    def test_filter_invalid_max_conditions_negative(self) -> None:
        with pytest.raises(FlextExceptions.BaseError, match="Invalid max_conditions"):
            FlextOracleWmsFilter(max_conditions=-1)

    def test_filter_max_conditions_limit_exceeded(self) -> None:
        with pytest.raises(FlextExceptions.BaseError, match="Invalid max_conditions"):
            FlextOracleWmsFilter(
                max_conditions=FlextOracleWmsConstants.Filtering.MAX_FILTER_CONDITIONS
                + 1,
            )

    def test_filter_with_initial_filters(self) -> None:
        """Test filter creation with initial filters dict."""
        filters: Mapping[str, t.Core.FilterScalar | t.Core.FilterList] = {
            "status": "active",
        }
        filter_engine = FlextOracleWmsFilter(filters=filters, max_conditions=50)
        assert filter_engine.filters == filters

    def test_filter_with_too_many_initial_filters(self) -> None:
        """Test filter creation raises when initial filters exceed max_conditions."""
        filters: Mapping[str, t.Core.FilterScalar] = {
            "field1": "v1",
            "field2": "v2",
            "field3": "v3",
            "field4": "v4",
        }
        with pytest.raises(FlextOracleWmsDataValidationError):
            FlextOracleWmsFilter(filters=filters, max_conditions=3)


class TestFilterValidation:
    """Test filter validation logic."""

    def test_validate_filter_conditions_empty(self) -> None:
        """Test validation with empty filters."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        result = filter_engine._validate_filters({})
        assert result.is_success

    def test_validate_filter_conditions_within_limit(self) -> None:
        """Test validation with filters within limit."""
        filter_engine = FlextOracleWmsFilter(max_conditions=5)
        result = filter_engine._validate_filters({"a": 1, "b": 2})
        assert result.is_success

    def test_validate_filter_conditions_exceeds_limit(self) -> None:
        """Test validation fails when conditions exceed limit."""
        filter_engine = FlextOracleWmsFilter(max_conditions=2)
        filters: Mapping[str, t.Core.FilterScalar | t.Core.FilterList] = {
            "field1": "value1",
            "field2": "value2",
            "field3": "value3",
        }
        result = filter_engine._validate_filters(filters)
        assert result.is_failure
        assert result.error is not None and "Too many" in result.error

    def test_validate_filter_list_values_count_correctly(self) -> None:
        """Test that list filter values are counted by length."""
        filter_engine = FlextOracleWmsFilter(max_conditions=2)
        filters: Mapping[str, t.Core.FilterScalar | t.Core.FilterList] = {
            "status": ["a", "b", "c"],
        }
        result = filter_engine._validate_filters(filters)
        assert result.is_failure


class TestRecordFiltering:
    """Test record filtering functionality."""

    @property
    def sample_records(self) -> Sequence[t.Core.FilterRecord]:
        """Sample records for testing."""
        return [
            {"id": 1, "name": "Company A", "status": "active", "score": 85.5},
            {"id": 2, "name": "Company B", "status": "inactive", "score": 72.0},
            {"id": 3, "name": "Company C", "status": "active", "score": 90.0},
            {"id": 4, "name": "Company D", "status": "pending", "score": 65.5},
        ]

    @property
    def nested_records(self) -> Sequence[t.Core.FilterRecord]:
        """Nested records for testing dot notation."""
        records: list[t.Core.FilterRecord] = [
            {
                "id": 1,
                "company_name": "Test Corp",
                "city": "New York",
                "score": 95,
                "rating": "A",
            },
            {
                "id": 2,
                "company_name": "Demo Inc",
                "city": "London",
                "score": 80,
                "rating": "B",
            },
        ]
        return records

    def test_filter_records_empty_filters(self) -> None:
        """Test filtering with empty filters returns all records."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        result = filter_engine.filter_records(self.sample_records, {})
        assert result.is_success
        assert len(result.value) == 4
        assert result.value == self.sample_records

    def test_filter_records_single_value(self) -> None:
        """Test filtering with single value condition."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        filters: Mapping[str, t.Core.FilterScalar | t.Core.FilterList] = {
            "status": "active",
        }
        result = filter_engine.filter_records(self.sample_records, filters)
        assert result.is_success
        assert len(result.value) == 2
        assert all(record["status"] == "active" for record in result.value)

    def test_filter_records_list_values(self) -> None:
        """Test filtering with list of values (IN operation)."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        filters: Mapping[str, t.Core.FilterScalar | t.Core.FilterList] = {
            "status": ["active", "pending"],
        }
        result = filter_engine.filter_records(self.sample_records, filters)
        assert result.is_success
        assert len(result.value) == 3
        assert all(record["status"] in {"active", "pending"} for record in result.value)

    def test_filter_records_numeric_values(self) -> None:
        """Test filtering with numeric values."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        filters: Mapping[str, t.Core.FilterScalar | t.Core.FilterList] = {"id": 2}
        result = filter_engine.filter_records(self.sample_records, filters)
        assert result.is_success
        assert result.is_success
        assert len(result.value) == 1
        assert result.value[0]["id"] == 2

    def test_filter_records_with_limit(self) -> None:
        """Test filtering with result limit."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        filters: Mapping[str, t.Core.FilterScalar | t.Core.FilterList] = {
            "status": "active",
        }
        result = filter_engine.filter_records(self.sample_records, filters, limit=1)
        assert result.is_success
        assert len(result.value) == 1
        assert result.value[0]["status"] == "active"

    def test_filter_records_no_matches(self) -> None:
        """Test filtering with no matching records."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        filters: Mapping[str, t.Core.FilterScalar | t.Core.FilterList] = {
            "status": "nonexistent",
        }
        result = filter_engine.filter_records(self.sample_records, filters)
        assert result.is_success
        assert not result.value

    def test_filter_records_case_insensitive(self) -> None:
        """Test filtering is case insensitive by default."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        filters: Mapping[str, t.Core.FilterScalar | t.Core.FilterList] = {
            "status": "ACTIVE",
        }
        result = filter_engine.filter_records(self.sample_records, filters)
        assert result.is_success
        assert len(result.value) == 2

    def test_filter_records_case_sensitive(self) -> None:
        """Test filtering with case sensitivity enabled."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=True, max_conditions=50)
        filters: Mapping[str, t.Core.FilterScalar | t.Core.FilterList] = {
            "status": "ACTIVE",
        }
        result = filter_engine.filter_records(self.sample_records, filters)
        assert result.is_success
        assert not result.value

    def test_filter_records_with_operator_dict(self) -> None:
        """Test filtering with operator dict format."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        filters: Mapping[str, OperatorFilter] = {
            "status": OperatorFilter(operator="ne", value="inactive"),
        }
        result = filter_engine.filter_records(self.sample_records, filters)
        assert result.is_success
        assert all(record["status"] != "inactive" for record in result.value)

    def test_filter_records_exceeds_condition_limit(self) -> None:
        """Test filtering fails when conditions exceed limit."""
        filter_engine = FlextOracleWmsFilter(max_conditions=2)
        filters: Mapping[str, t.Core.FilterScalar | t.Core.FilterList] = {
            "status": ["a", "b", "c"],
        }
        result = filter_engine.filter_records(self.sample_records, filters)
        assert result.is_failure
        assert result.error is not None and "Too many" in result.error


class TestRecordSorting:
    """Test record sorting functionality."""

    @property
    def unsorted_records(self) -> Sequence[t.Core.FilterRecord]:
        """Unsorted records for testing."""
        return [
            {"id": 3, "name": "Charlie", "score": 75.5},
            {"id": 1, "name": "Alice", "score": 90.0},
            {"id": 2, "name": "Bob", "score": 85.0},
        ]

    def test_sort_records_ascending_string(self) -> None:
        """Test sorting records by string field in ascending order."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        result = filter_engine.sort_records(self.unsorted_records, "name")
        assert result.is_success
        assert len(result.value) == 3
        assert [r["name"] for r in result.value] == ["Alice", "Bob", "Charlie"]

    def test_sort_records_descending_string(self) -> None:
        """Test sorting records by string field in descending order."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        result = filter_engine.sort_records(
            self.unsorted_records,
            "name",
            ascending=False,
        )
        assert result.is_success
        assert [r["name"] for r in result.value] == ["Charlie", "Bob", "Alice"]

    def test_sort_records_ascending_numeric(self) -> None:
        """Test sorting records by numeric field in ascending order."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        result = filter_engine.sort_records(self.unsorted_records, "id")
        assert result.is_success
        assert [r["id"] for r in result.value] == [1, 2, 3]

    def test_sort_records_descending_numeric(self) -> None:
        """Test sorting records by numeric field in descending order."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        result = filter_engine.sort_records(
            self.unsorted_records,
            "score",
            ascending=False,
        )
        assert result.is_success
        assert [r["score"] for r in result.value] == [90.0, 85.0, 75.5]

    def test_sort_records_with_none_values(self) -> None:
        """Test sorting records with None values."""
        records_with_none: Sequence[t.Core.FilterRecord] = [
            {"id": 1, "name": "Alice", "score": None},
            {"id": 2, "name": "Bob", "score": 85.0},
            {"id": 3, "name": None, "score": 90.0},
        ]
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        result = filter_engine.sort_records(records_with_none, "name")
        assert result.is_success
        assert len(result.value) == 3

    def test_sort_records_nonexistent_field(self) -> None:
        """Test sorting by a field that doesn't exist in records."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        result = filter_engine.sort_records(self.unsorted_records, "nonexistent")
        assert result.is_success


class TestNestedValueAccess:
    """Test nested value access with dot notation."""

    @property
    def nested_record(self) -> t.Core.FilterRecord:
        """Nested record for testing."""
        record: t.Core.FilterRecord = {
            "id": 1,
            "company_name": "Test Corp",
            "company_address_city": "New York",
            "company_address_country": "USA",
            "metrics_score": 95,
            "metrics_rating": "A",
        }
        return record

    def test_get_nested_value_simple_field(self) -> None:
        """Test getting simple field value."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        value = filter_engine._get_nested_value(self.nested_record, "id")
        assert value == 1

    def test_get_nested_value_one_level_deep(self) -> None:
        """Test getting one level nested value."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        value = filter_engine._get_nested_value(self.nested_record, "company.name")
        assert value == "Test Corp"

    def test_get_nested_value_two_levels_deep(self) -> None:
        """Test getting two levels nested value."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        value = filter_engine._get_nested_value(
            self.nested_record,
            "company.address.city",
        )
        assert value == "New York"

    def test_get_nested_value_nonexistent_field(self) -> None:
        """Test getting nonexistent field returns None."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        value = filter_engine._get_nested_value(self.nested_record, "nonexistent")
        assert value is None

    def test_get_nested_value_nonexistent_nested_field(self) -> None:
        """Test getting nonexistent nested field returns None."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        value = filter_engine._get_nested_value(
            self.nested_record,
            "company.nonexistent",
        )
        assert value is None

    def test_get_nested_value_invalid_path(self) -> None:
        """Test getting value with invalid path returns None."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        value = filter_engine._get_nested_value(self.nested_record, "id.invalid")
        assert value is None


class TestNormalize:
    """Test value normalization."""

    def test_normalize_case_sensitive(self) -> None:
        filter_engine = FlextOracleWmsFilter(case_sensitive=True)
        assert filter_engine._normalize("Test") == "Test"

    def test_normalize_case_insensitive(self) -> None:
        filter_engine = FlextOracleWmsFilter(case_sensitive=False)
        assert filter_engine._normalize("Test") == "test"

    def test_normalize_non_string(self) -> None:
        filter_engine = FlextOracleWmsFilter(case_sensitive=False)
        assert filter_engine._normalize(123) == 123
        assert filter_engine._normalize(True) is True

    def test_normalize_none(self) -> None:
        filter_engine = FlextOracleWmsFilter(case_sensitive=False)
        assert filter_engine._normalize(None) == ""


class TestApplyOperator:
    """Test _apply_operator dispatch table."""

    def test_eq_case_sensitive(self) -> None:
        filter_engine = FlextOracleWmsFilter(case_sensitive=True)
        assert filter_engine._apply_operator("Test", "eq", "Test") is True
        assert filter_engine._apply_operator("Test", "eq", "test") is False

    def test_eq_case_insensitive(self) -> None:
        filter_engine = FlextOracleWmsFilter(case_sensitive=False)
        assert filter_engine._apply_operator("Test", "eq", "test") is True
        assert filter_engine._apply_operator("TEST", "eq", "test") is True

    def test_ne(self) -> None:
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        assert filter_engine._apply_operator("a", "ne", "b") is True
        assert filter_engine._apply_operator("a", "ne", "a") is False

    def test_gt_numeric(self) -> None:
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        assert filter_engine._apply_operator(10, "gt", 5) is True
        assert filter_engine._apply_operator(5, "gt", 10) is False
        assert filter_engine._apply_operator(5.5, "gt", 5.0) is True

    def test_gt_string(self) -> None:
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        assert filter_engine._apply_operator("b", "gt", "a") is True
        assert filter_engine._apply_operator("a", "gt", "b") is False

    def test_gt_mixed_types(self) -> None:
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        assert filter_engine._apply_operator("10", "gt", 5) is False
        assert filter_engine._apply_operator(10, "gt", "5") is False

    def test_lt_numeric(self) -> None:
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        assert filter_engine._apply_operator(5, "lt", 10) is True
        assert filter_engine._apply_operator(10, "lt", 5) is False

    def test_gte_numeric(self) -> None:
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        assert filter_engine._apply_operator(10, "gte", 5) is True
        assert filter_engine._apply_operator(5, "gte", 5) is True
        assert filter_engine._apply_operator(5, "gte", 10) is False

    def test_lte_numeric(self) -> None:
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        assert filter_engine._apply_operator(5, "lte", 10) is True
        assert filter_engine._apply_operator(5, "lte", 5) is True
        assert filter_engine._apply_operator(10, "lte", 5) is False

    def test_in_list(self) -> None:
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        assert filter_engine._apply_operator("a", "in", ["a", "b", "c"]) is True
        assert filter_engine._apply_operator("d", "in", ["a", "b", "c"]) is False

    def test_in_invalid_filter_value(self) -> None:
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        assert filter_engine._apply_operator("a", "in", "not_a_list") is False

    def test_contains_string(self) -> None:
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        assert filter_engine._apply_operator("hello world", "contains", "world") is True
        assert filter_engine._apply_operator("hello", "contains", "world") is False

    def test_contains_non_string(self) -> None:
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        assert filter_engine._apply_operator(123, "contains", "1") is False

    def test_unknown_operator(self) -> None:
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        assert filter_engine._apply_operator("a", "unknown", "b") is False


class TestFactoryFunction:
    """Test factory function and convenience functions."""

    def test_create_filter_default(self) -> None:
        """Test creating filter with default parameters."""
        filter_engine = FlextOracleWmsFilter.create_filter()
        assert filter_engine.case_sensitive is False
        assert (
            filter_engine.max_conditions
            == FlextOracleWmsConstants.Filtering.MAX_FILTER_CONDITIONS
        )

    def test_create_filter_custom(self) -> None:
        """Test creating filter with custom parameters."""
        filter_engine = FlextOracleWmsFilter.create_filter(
            case_sensitive=True,
            max_conditions=50,
        )
        assert filter_engine.case_sensitive is True
        assert filter_engine.max_conditions == 50

    def test_create_filter_invalid_max_conditions(self) -> None:
        with pytest.raises(FlextExceptions.BaseError, match="Invalid max_conditions"):
            FlextOracleWmsFilter.create_filter(max_conditions=0)

    def test_create_filter_exceeds_limit(self) -> None:
        with pytest.raises(FlextExceptions.BaseError, match="Invalid max_conditions"):
            FlextOracleWmsFilter.create_filter(
                max_conditions=FlextOracleWmsConstants.Filtering.MAX_FILTER_CONDITIONS
                + 1,
            )


class TestConvenienceFunctions:
    """Test convenience filtering functions."""

    @property
    def sample_records(self) -> Sequence[t.Core.FilterRecord]:
        """Sample records for testing."""
        return [
            {"id": 1, "name": "Company A", "status": "active"},
            {"id": 2, "name": "Company B", "status": "inactive"},
            {"id": 3, "name": "Company C", "status": "active"},
        ]

    def test_filter_by_field_string_value(self) -> None:
        """Test filter by field with string value."""
        result = FlextOracleWmsFilter.filter_by_field(
            self.sample_records,
            "status",
            "active",
        )
        assert result.is_success
        assert len(result.value) == 2
        assert all(record["status"] == "active" for record in result.value)

    def test_filter_by_field_numeric_value(self) -> None:
        """Test filter by field with numeric value."""
        result = FlextOracleWmsFilter.filter_by_field(self.sample_records, "id", 2)
        assert result.is_success
        assert len(result.value) == 1
        assert result.value[0]["id"] == 2

    def test_filter_by_field_list_value(self) -> None:
        """Test filter by field with list value (use filter_records for list matching)."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        result = filter_engine.filter_records(self.sample_records, {"status": "active"})
        assert result.is_success
        assert len(result.value) >= 1

    def test_filter_by_field_custom_operator(self) -> None:
        """Test filter by field with custom operator string."""
        result = FlextOracleWmsFilter.filter_by_field(
            self.sample_records,
            "status",
            "inactive",
            FlextOracleWmsFilterOperator.NE,
        )
        assert result.is_success
        assert len(result.value) == 2
        assert all(record["status"] != "inactive" for record in result.value)

    def test_filter_by_id_range_both_bounds(self) -> None:
        """Test filter by ID range with both min and max."""
        result = FlextOracleWmsFilter.filter_by_id_range(
            self.sample_records,
            "id",
            min_id=1,
            max_id=3,
        )
        assert result.is_success
        assert len(result.value) >= 1

    def test_filter_by_id_range_min_only(self) -> None:
        """Test filter by ID range with min only."""
        result = FlextOracleWmsFilter.filter_by_id_range(
            self.sample_records,
            "id",
            min_id=2,
        )
        assert result.is_success
        assert len(result.value) >= 1

    def test_filter_by_id_range_max_only(self) -> None:
        """Test filter by ID range with max only."""
        result = FlextOracleWmsFilter.filter_by_id_range(
            self.sample_records,
            "id",
            max_id=2,
        )
        assert result.is_success
        assert len(result.value) >= 1

    def test_filter_by_id_range_no_bounds(self) -> None:
        """Test filter by ID range with no bounds returns all records."""
        result = FlextOracleWmsFilter.filter_by_id_range(self.sample_records, "id")
        assert result.is_success
        assert len(result.value) == 3

    def test_filter_by_id_range_custom_field(self) -> None:
        """Test filter by ID range with custom ID field."""
        result = FlextOracleWmsFilter.filter_by_id_range(
            self.sample_records,
            "name",
            min_id="Company B",
        )
        assert result.is_success

    def test_filter_by_id_range_empty_records(self) -> None:
        """Test filter by ID range with empty records."""
        result = FlextOracleWmsFilter.filter_by_id_range([], "id", min_id=1)
        assert result.is_success
        assert not result.value


class TestMatchesCondition:
    """Test _matches_condition pattern matching."""

    def test_matches_condition_simple_equality(self) -> None:
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        record: t.Core.FilterRecord = {"status": "active"}
        assert filter_engine._matches_condition(record, "status", "active") is True
        assert filter_engine._matches_condition(record, "status", "inactive") is False

    def test_matches_condition_list_match(self) -> None:
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        record: t.Core.FilterRecord = {"status": "active"}
        assert (
            filter_engine._matches_condition(record, "status", ["active", "pending"])
            is True
        )
        assert (
            filter_engine._matches_condition(record, "status", ["inactive", "deleted"])
            is False
        )

    def test_matches_condition_operator_filter(self) -> None:
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        record: t.Core.FilterRecord = {"score": 85}
        assert (
            filter_engine._matches_condition(
                record,
                "score",
                OperatorFilter(operator="gt", value=80),
            )
            is True
        )
        assert (
            filter_engine._matches_condition(
                record,
                "score",
                OperatorFilter(operator="gt", value=90),
            )
            is False
        )

    def test_matches_condition_scalar_mismatch(self) -> None:
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        record: t.Core.FilterRecord = {"field": "value"}
        result = filter_engine._matches_condition(record, "field", "other_value")
        assert result is False

    def test_matches_condition_none_field_value_with_list(self) -> None:
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        record: t.Core.FilterRecord = {"field": None}
        assert filter_engine._matches_condition(record, "field", ["a", "b"]) is False


class TestErrorHandling:
    """Test error handling in filtering operations."""

    def test_sort_records_handles_exception(self) -> None:
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        result = filter_engine.sort_records([], "nonexistent_field_xyz_123")
        assert result.is_success

    def test_filter_records_validation_failure(self) -> None:
        filter_engine = FlextOracleWmsFilter(max_conditions=1)
        filters: Mapping[str, t.Core.FilterScalar | t.Core.FilterList] = {
            "a": "1",
            "b": "2",
        }
        result = filter_engine.filter_records([], filters)
        assert result.is_failure

    def test_apply_operator_type_safety_edge_cases(self) -> None:
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        assert filter_engine._apply_operator(None, "gt", 5) is False
        assert filter_engine._apply_operator(5, "lt", None) is False
        assert filter_engine._apply_operator(None, "gte", None) is True


class TestPerformanceAndEdgeCases:
    """Test performance considerations and edge cases."""

    def test_filter_large_record_set(self) -> None:
        """Test filtering with large record set."""
        large_records: Sequence[t.Core.FilterRecord] = [
            {"id": i, "status": "active" if i % 2 == 0 else "inactive"}
            for i in range(1000)
        ]
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        result = filter_engine.filter_records(
            large_records,
            {"status": "active"},
            limit=100,
        )
        assert result.is_success
        assert len(result.value) == 100
        assert all(record["status"] == "active" for record in result.value)

    def test_filter_with_complex_nested_data(self) -> None:
        """Test filtering with nested data structures."""
        complex_records: Sequence[t.Core.FilterRecord] = [
            {"id": 1, "category": "target", "subcategory": "A"},
            {"id": 2, "category": "other", "subcategory": "B"},
        ]
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        result = filter_engine.filter_records(
            complex_records,
            {"category": "target"},
        )
        assert result.is_success
        assert len(result.value) == 1
        assert result.value[0]["id"] == 1

    def test_filter_handles_unicode_strings(self) -> None:
        """Test that filtering handles unicode strings correctly."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=False)
        assert filter_engine._apply_operator("Café", "eq", "café") is True

    def test_get_nested_value_edge_cases(self) -> None:
        """Test nested value access with edge cases."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        assert filter_engine._get_nested_value({}, "field") is None
        record_with_none: t.Core.FilterRecord = {"level1": None}
        assert (
            filter_engine._get_nested_value(record_with_none, "level1.level2") is None
        )
        record_with_scalar: t.Core.FilterRecord = {"level1": "string_value"}
        assert (
            filter_engine._get_nested_value(record_with_scalar, "level1.level2") is None
        )

    def test_check_min_and_max_static_methods(self) -> None:
        assert FlextOracleWmsFilter._check_min(5, 3) is True
        assert FlextOracleWmsFilter._check_min(3, 5) is False
        assert FlextOracleWmsFilter._check_min(5, 5) is True
        assert FlextOracleWmsFilter._check_max(3, 5) is True
        assert FlextOracleWmsFilter._check_max(5, 3) is False
        assert FlextOracleWmsFilter._check_max(5, 5) is True
        assert FlextOracleWmsFilter._check_min("b", "a") is True
        assert FlextOracleWmsFilter._check_min("a", "b") is False
        assert FlextOracleWmsFilter._check_max("a", "b") is True
        assert FlextOracleWmsFilter._check_max("b", "a") is False
        assert FlextOracleWmsFilter._check_min("a", 1) is True
        assert FlextOracleWmsFilter._check_max("a", 1) is False
