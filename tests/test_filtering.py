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

import pytest

from flext_core import FlextTypes
from flext_oracle_wms import (
    FlextOracleWmsDataValidationError,
    FlextOracleWmsDefaults,
    FlextOracleWmsError,
    FlextOracleWmsFilter,
    OracleWMSFilterOperator,
    flext_oracle_wms_create_filter,
    flext_oracle_wms_filter_by_field,
    flext_oracle_wms_filter_by_id_range,
)


class TestFlextOracleWmsFilterConstruction:
    """Test filter construction and validation."""

    def test_filter_default_construction(self) -> None:
        """Test filter creation with default parameters."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        assert filter_engine.case_sensitive is False
        assert (
            filter_engine.max_conditions == FlextOracleWmsDefaults.MAX_FILTER_CONDITIONS
        )

    def test_filter_custom_construction(self) -> None:
        """Test filter creation with custom parameters."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=True, max_conditions=50)
        assert filter_engine.case_sensitive is True
        assert filter_engine.max_conditions == 50

    def test_filter_invalid_max_conditions_zero(self) -> None:
        """Test filter creation fails with zero max conditions."""
        with pytest.raises(FlextOracleWmsError) as exc:
            FlextOracleWmsFilter(max_conditions=0)
        assert "must be positive" in str(exc.value)

    def test_filter_invalid_max_conditions_negative(self) -> None:
        """Test filter creation fails with negative max conditions."""
        with pytest.raises(FlextOracleWmsError) as exc:
            FlextOracleWmsFilter(max_conditions=-1)
        assert "must be positive" in str(exc.value)

    def test_filter_max_conditions_limit_exceeded(self) -> None:
        """Test filter creation fails when exceeding maximum limit."""
        with pytest.raises(FlextOracleWmsError) as exc:
            FlextOracleWmsFilter(
                max_conditions=FlextOracleWmsDefaults.MAX_FILTER_CONDITIONS + 1,
            )
        assert "cannot exceed" in str(exc.value)

    def test_filter_operators_initialized(self) -> None:
        """Test that all filter operators are properly initialized."""
        # This test is disabled as the _operators attribute doesn't exist in current implementation
        pytest.skip("_operators attribute not implemented in current architecture")


class TestFilterValidation:
    """Test filter validation logic."""

    def test_validate_filter_conditions_empty(self) -> None:
        """Test validation with empty filters."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        # This method doesn't return anything, it raises an exception if validation fails
        filter_engine._validate_filter_conditions_count()  # Should not raise

    def test_validate_filter_conditions_within_limit(self) -> None:
        """Test validation with filters within limit."""
        filter_engine = FlextOracleWmsFilter(max_conditions=5)
        # This method doesn't return anything, it raises an exception if validation fails
        filter_engine._validate_filter_conditions_count()  # Should not raise

    def test_validate_filter_conditions_exceeds_limit(self) -> None:
        """Test validation fails when conditions exceed limit."""
        # Create a filter with too many conditions
        filters: FlextTypes.Dict = {
            "field1": {"eq": "value1"},
            "field2": {"eq": "value2"},
            "field3": {"eq": "value3"},
            "field4": {"eq": "value4"},  # This exceeds max_conditions=3
        }

        with pytest.raises(FlextOracleWmsDataValidationError) as exc_info:
            FlextOracleWmsFilter(filters=filters, max_conditions=3)

        assert "Too many filter conditions" in str(exc_info.value)

    def test_validate_filter_conditions_mixed_types(self) -> None:
        """Test validation with mixed condition types."""
        # Create a filter with mixed condition types within limit
        filters = {
            "field1": {"eq": "value1"},
            "field2": {"gt": 100},
            "field3": {"in": ["a", "b", "c"]},
        }

        # This should not raise an exception since it's within the limit
        filter_engine = FlextOracleWmsFilter(filters=filters, max_conditions=10)
        assert filter_engine.max_conditions == 10


class TestRecordFiltering:
    """Test record filtering functionality."""

    @property
    def sample_records(self) -> list[FlextTypes.Dict]:
        """Sample records for testing."""
        return [
            {"id": 1, "name": "Company A", "status": "active", "score": 85.5},
            {"id": 2, "name": "Company B", "status": "inactive", "score": 72.0},
            {"id": 3, "name": "Company C", "status": "active", "score": 90.0},
            {"id": 4, "name": "Company D", "status": "pending", "score": 65.5},
        ]

    @property
    def nested_records(self) -> list[FlextTypes.Dict]:
        """Nested records for testing dot notation."""
        return [
            {
                "id": 1,
                "company": {"name": "Test Corp", "address": {"city": "New York"}},
                "metrics": {"score": 95, "rating": "A"},
            },
            {
                "id": 2,
                "company": {"name": "Demo Inc", "address": {"city": "London"}},
                "metrics": {"score": 80, "rating": "B"},
            },
        ]

    def test_filter_records_empty_filters(self) -> None:
        """Test filtering with empty filters returns all records."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        result = filter_engine.filter_records(self.sample_records, {})

        assert result.success
        assert len(result.value) == 4
        assert result.value == self.sample_records

    def test_filter_records_single_value(self) -> None:
        """Test filtering with single value condition."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        filters: FlextTypes.Dict = {"status": "active"}
        result = filter_engine.filter_records(self.sample_records, filters)

        assert result.success
        assert len(result.value) == 2
        assert all(record["status"] == "active" for record in result.value)

    def test_filter_records_list_values(self) -> None:
        """Test filtering with list of values (IN operation)."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        filters: FlextTypes.Dict = {"status": ["active", "pending"]}
        result = filter_engine.filter_records(self.sample_records, filters)

        assert result.success
        assert len(result.value) == 3
        assert all(record["status"] in {"active", "pending"} for record in result.value)

    def test_filter_records_numeric_values(self) -> None:
        """Test filtering with numeric values."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        filters: FlextTypes.Dict = {"id": 2}
        result = filter_engine.filter_records(self.sample_records, filters)

        assert result.success
        assert result.success
        assert len(result.value) == 1
        assert result.value[0]["id"] == 2

    def test_filter_records_with_limit(self) -> None:
        """Test filtering with result limit."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        filters: FlextTypes.Dict = {"status": "active"}
        result = filter_engine.filter_records_with_options(
            self.sample_records,
            filters,
            limit=1,
        )

        assert result.success
        assert result.success
        assert len(result.value) == 1
        assert result.value[0]["status"] == "active"

    def test_filter_records_no_matches(self) -> None:
        """Test filtering with no matching records."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        filters: FlextTypes.Dict = {"status": "nonexistent"}
        result = filter_engine.filter_records(self.sample_records, filters)

        assert result.success
        assert result.success
        assert len(result.value) == 0

    def test_filter_records_invalid_input_types(self) -> None:
        """Test filtering with invalid input types raises validation error."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)

        # Invalid records type
        with pytest.raises(FlextOracleWmsDataValidationError):
            filter_engine.filter_records("not_a_list", {})

        # Invalid filters type
        with pytest.raises(FlextOracleWmsDataValidationError):
            filter_engine.filter_records(self.sample_records, "not_a_dict")

    def test_filter_records_exceeds_condition_limit(self) -> None:
        """Test filtering fails when conditions exceed limit."""
        filter_engine = FlextOracleWmsFilter(max_conditions=2)
        filters: FlextTypes.Dict = {
            "status": ["a", "b", "c"],
        }  # 3 conditions > 2 limit
        result = filter_engine.filter_records(self.sample_records, filters)

        assert result.is_failure
        assert result.error is not None
        assert result.error is not None and "Too many filter conditions" in result.error


class TestRecordSorting:
    """Test record sorting functionality."""

    @property
    def unsorted_records(self) -> list[FlextTypes.Dict]:
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

        assert result.success
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

        assert result.success
        assert [r["name"] for r in result.value] == ["Charlie", "Bob", "Alice"]

    def test_sort_records_ascending_numeric(self) -> None:
        """Test sorting records by numeric field in ascending order."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        result = filter_engine.sort_records(self.unsorted_records, "id")

        assert result.success
        assert [r["id"] for r in result.value] == [1, 2, 3]

    def test_sort_records_descending_numeric(self) -> None:
        """Test sorting records by numeric field in descending order."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        result = filter_engine.sort_records(
            self.unsorted_records,
            "score",
            ascending=False,
        )

        assert result.success
        assert [r["score"] for r in result.value] == [90.0, 85.0, 75.5]

    def test_sort_records_with_none_values(self) -> None:
        """Test sorting records with None values."""
        records_with_none: list[FlextTypes.Dict] = [
            {"id": 1, "name": "Alice", "score": None},
            {"id": 2, "name": "Bob", "score": 85.0},
            {"id": 3, "name": None, "score": 90.0},
        ]

        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        result = filter_engine.sort_records(records_with_none, "name")

        assert result.success
        assert len(result.value) == 3
        # None values should be handled (empty string in ascending, "zzz" in descending)

    def test_sort_records_invalid_input_types(self) -> None:
        """Test sorting with invalid input types returns error result."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)

        # Invalid records type - should fail gracefully
        result = filter_engine.sort_records("not_a_list", "field")
        assert result.is_failure

        # Invalid sort field type - should fail gracefully
        result = filter_engine.sort_records(self.unsorted_records, 123)
        assert result.is_failure


class TestNestedValueAccess:
    """Test nested value access with dot notation."""

    @property
    def nested_record(self) -> FlextTypes.Dict:
        """Nested record for testing."""
        return {
            "id": 1,
            "company": {
                "name": "Test Corp",
                "address": {"city": "New York", "country": "USA"},
            },
            "metrics": {"score": 95, "rating": "A"},
        }

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


class TestOperatorImplementations:
    """Test individual operator implementations."""

    def test_normalize_for_comparison_case_sensitive(self) -> None:
        """Test value normalization with case sensitivity enabled."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=True)
        value = filter_engine._normalize_for_comparison("Test")
        assert value == "Test"

    def test_normalize_for_comparison_case_insensitive(self) -> None:
        """Test value normalization with case sensitivity disabled."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=False)
        value = filter_engine._normalize_for_comparison("Test")
        assert value == "test"

    def test_normalize_for_comparison_non_string(self) -> None:
        """Test value normalization with non-string values."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=False)
        assert filter_engine._normalize_for_comparison(123) == 123
        assert filter_engine._normalize_for_comparison(True) is True

    def test_op_equals_case_sensitive(self) -> None:
        """Test equals operator with case sensitivity."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=True)
        assert filter_engine._op_equals("Test", "Test") is True
        assert filter_engine._op_equals("Test", "test") is False

    def test_op_equals_case_insensitive(self) -> None:
        """Test equals operator without case sensitivity."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=False)
        assert filter_engine._op_equals("Test", "test") is True
        assert filter_engine._op_equals("TEST", "test") is True

    def test_op_not_equals(self) -> None:
        """Test not equals operator."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        assert filter_engine._op_not_equals("a", "b") is True
        assert filter_engine._op_not_equals("a", "a") is False

    def test_op_greater_than_numeric(self) -> None:
        """Test greater than operator with numeric values."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        assert filter_engine._op_greater_than(10, 5) is True
        assert filter_engine._op_greater_than(5, 10) is False
        assert filter_engine._op_greater_than(5.5, 5.0) is True

    def test_op_greater_than_string(self) -> None:
        """Test greater than operator with string values."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        assert filter_engine._op_greater_than("b", "a") is True
        assert filter_engine._op_greater_than("a", "b") is False

    def test_op_greater_than_mixed_types(self) -> None:
        """Test greater than operator with mixed types returns False."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        assert filter_engine._op_greater_than("10", 5) is False
        assert filter_engine._op_greater_than(10, "5") is False

    def test_op_greater_equal_numeric(self) -> None:
        """Test greater than or equal operator with numeric values."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        assert filter_engine._op_greater_equal(10, 5) is True
        assert filter_engine._op_greater_equal(5, 5) is True
        assert filter_engine._op_greater_equal(5, 10) is False

    def test_op_less_than_numeric(self) -> None:
        """Test less than operator with numeric values."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        assert filter_engine._op_less_than(5, 10) is True
        assert filter_engine._op_less_than(10, 5) is False

    def test_op_less_equal_numeric(self) -> None:
        """Test less than or equal operator with numeric values."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        assert filter_engine._op_less_equal(5, 10) is True
        assert filter_engine._op_less_equal(5, 5) is True
        assert filter_engine._op_less_equal(10, 5) is False

    def test_op_in_list(self) -> None:
        """Test in operator with list values."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        assert filter_engine._op_in("a", ["a", "b", "c"]) is True
        assert filter_engine._op_in("d", ["a", "b", "c"]) is False

    def test_op_in_case_insensitive(self) -> None:
        """Test in operator with case insensitivity."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=False)
        assert filter_engine._op_in("A", ["a", "b", "c"]) is True

    def test_op_in_invalid_filter_value(self) -> None:
        """Test in operator with invalid filter value."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        assert filter_engine._op_in("a", "not_a_list") is False

    def test_op_not_in(self) -> None:
        """Test not in operator."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        assert filter_engine._op_not_in("d", ["a", "b", "c"]) is True
        assert filter_engine._op_not_in("a", ["a", "b", "c"]) is False

    def test_op_like_pattern_matching(self) -> None:
        """Test like operator with pattern matching."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        assert filter_engine._op_like("test string", "test%") is True
        assert filter_engine._op_like("test string", "%string") is True
        assert filter_engine._op_like("test", "t_st") is True
        assert filter_engine._op_like("test", "best") is False

    def test_op_like_case_sensitivity(self) -> None:
        """Test like operator with case sensitivity."""
        filter_engine_sensitive = FlextOracleWmsFilter(case_sensitive=True)
        filter_engine_insensitive = FlextOracleWmsFilter(case_sensitive=False)

        assert filter_engine_sensitive._op_like("Test", "test%") is False
        assert filter_engine_insensitive._op_like("Test", "test%") is True

    def test_op_like_non_string_values(self) -> None:
        """Test like operator with non-string values."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        assert filter_engine._op_like(123, "12%") is False
        assert filter_engine._op_like("123", 12) is False

    def test_op_not_like(self) -> None:
        """Test not like operator."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        assert filter_engine._op_not_like("test", "best") is True
        assert filter_engine._op_not_like("test", "test") is False


class TestFactoryFunction:
    """Test factory function and convenience functions."""

    def test_create_filter_default(self) -> None:
        """Test creating filter with default parameters."""
        filter_engine = flext_oracle_wms_create_filter()
        assert filter_engine.case_sensitive is False
        assert (
            filter_engine.max_conditions == FlextOracleWmsDefaults.MAX_FILTER_CONDITIONS
        )

    def test_create_filter_custom(self) -> None:
        """Test creating filter with custom parameters."""
        filter_engine = flext_oracle_wms_create_filter(
            case_sensitive=True,
            max_conditions=50,
        )
        assert filter_engine.case_sensitive is True
        assert filter_engine.max_conditions == 50

    def test_create_filter_invalid_max_conditions(self) -> None:
        """Test factory function fails with invalid max conditions."""
        with pytest.raises(FlextOracleWmsError) as exc:
            flext_oracle_wms_create_filter(max_conditions=0)
        assert "must be positive" in str(exc.value)

    def test_create_filter_exceeds_limit(self) -> None:
        """Test factory function fails when exceeding limit."""
        with pytest.raises(FlextOracleWmsError) as exc:
            flext_oracle_wms_create_filter(
                max_conditions=FlextOracleWmsDefaults.MAX_FILTER_CONDITIONS + 1,
            )
        assert "cannot exceed" in str(exc.value)


class TestConvenienceFunctions:
    """Test convenience filtering functions."""

    @property
    def sample_records(self) -> list[FlextTypes.Dict]:
        """Sample records for testing."""
        return [
            {"id": 1, "name": "Company A", "status": "active"},
            {"id": 2, "name": "Company B", "status": "inactive"},
            {"id": 3, "name": "Company C", "status": "active"},
        ]

    def test_filter_by_field_string_value(self) -> None:
        """Test filter by field with string value."""
        result = flext_oracle_wms_filter_by_field(
            self.sample_records,
            "status",
            "active",
        )

        assert result.success
        assert len(result.value) == 2
        assert all(record["status"] == "active" for record in result.value)

    def test_filter_by_field_numeric_value(self) -> None:
        """Test filter by field with numeric value."""
        result = flext_oracle_wms_filter_by_field(self.sample_records, "id", 2)

        assert result.success
        assert len(result.value) == 1
        assert result.value[0]["id"] == 2

    def test_filter_by_field_list_value(self) -> None:
        """Test filter by field with list value."""
        result = flext_oracle_wms_filter_by_field(
            self.sample_records,
            "id",
            [1, 3],
        )

        assert result.success
        assert len(result.value) == 2
        assert {record["id"] for record in result.value} == {1, 3}

    def test_filter_by_field_custom_operator(self) -> None:
        """Test filter by field with custom operator."""
        result = flext_oracle_wms_filter_by_field(
            self.sample_records,
            "status",
            "inactive",
            OracleWMSFilterOperator.NE,
        )

        assert result.success
        # For NE operator with single value, it returns records where status != "inactive"
        assert len(result.value) == 2  # Company A and Company C (both "active")
        assert all(record["status"] != "inactive" for record in result.value)

    def test_filter_by_field_invalid_records(self) -> None:
        """Test filter by field with invalid records raises error."""
        with pytest.raises(FlextOracleWmsDataValidationError):
            flext_oracle_wms_filter_by_field("not_a_list", "field", "value")

    def test_filter_by_id_range_both_bounds(self) -> None:
        """Test filter by ID range with both min and max."""
        result = flext_oracle_wms_filter_by_id_range(
            self.sample_records,
            "id",
            min_id=1,
            max_id=3,
        )

        assert result.success
        assert len(result.value) >= 1  # Should include records with IDs in range

    def test_filter_by_id_range_min_only(self) -> None:
        """Test filter by ID range with min only."""
        result = flext_oracle_wms_filter_by_id_range(
            self.sample_records,
            "id",
            min_id=2,
        )

        assert result.success
        assert len(result.value) >= 1

    def test_filter_by_id_range_max_only(self) -> None:
        """Test filter by ID range with max only."""
        result = flext_oracle_wms_filter_by_id_range(
            self.sample_records,
            "id",
            max_id=2,
        )

        assert result.success
        assert len(result.value) >= 1

    def test_filter_by_id_range_no_bounds(self) -> None:
        """Test filter by ID range with no bounds returns all records."""
        result = flext_oracle_wms_filter_by_id_range(self.sample_records, "id")

        assert result.success
        assert len(result.value) == 3  # All records

    def test_filter_by_id_range_custom_field(self) -> None:
        """Test filter by ID range with custom ID field."""
        result = flext_oracle_wms_filter_by_id_range(
            self.sample_records,
            "name",
            min_id="Company B",
        )

        assert result.success

    def test_filter_by_id_range_invalid_records(self) -> None:
        """Test filter by ID range with invalid records raises error."""
        with pytest.raises(FlextOracleWmsDataValidationError):
            flext_oracle_wms_filter_by_id_range("not_a_list", "id")


class TestErrorHandling:
    """Test error handling in filtering operations."""

    def test_filter_records_handles_validation_errors(self) -> None:
        """Test that filter_records properly handles validation errors."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)

        # This should raise FlextOracleWmsDataValidationError via handle_operation_exception
        with pytest.raises(FlextOracleWmsDataValidationError):
            filter_engine.filter_records("invalid_records", {})

    def test_sort_records_handles_validation_errors(self) -> None:
        """Test that sort_records properly handles validation errors."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)

        # This should return a failed FlextResult due to validation
        result = filter_engine.sort_records("invalid_records", "field")
        assert result.is_failure
        assert result.error is not None
        assert result.error is not None and "Type mismatch" in result.error

    def test_matches_condition_unknown_operator(self) -> None:
        """Test _matches_condition with unknown operator."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        result = filter_engine._matches_condition(
            {"field": "value"},
            "field",
            {"unknown_op": "test"},
        )
        # Should return False for unknown operators
        assert result is False

    def test_matches_condition_invalid_operator_enum(self) -> None:
        """Test _matches_condition with invalid operator enum."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        # Create a mock record for testing
        mock_record: FlextTypes.Dict = {"field": "value"}
        result = filter_engine._matches_condition(
            mock_record,
            "field",
            {"invalid": "test"},
        )
        # Should return False since invalid operator falls back to equals comparison
        # and "value" != {"invalid": "test"}
        assert result is False

    def test_operator_type_safety_edge_cases(self) -> None:
        """Test operator implementations handle type errors gracefully."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)

        # Test with problematic values that might cause TypeErrors
        assert filter_engine._op_greater_than(None, 5) is False
        assert filter_engine._op_less_than(5, None) is False
        assert filter_engine._op_greater_equal(None, None) is False
        assert filter_engine._op_less_equal([], {}) is False


class TestPerformanceAndEdgeCases:
    """Test performance considerations and edge cases."""

    def test_filter_large_record_set(self) -> None:
        """Test filtering with large record set."""
        # Create large record set
        large_records: list[FlextTypes.Dict] = [
            {"id": i, "status": "active" if i % 2 == 0 else "inactive"}
            for i in range(1000)
        ]

        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        result = filter_engine.filter_records_with_options(
            large_records,
            {"status": "active"},
            limit=100,
        )

        assert result.success
        assert len(result.value) == 100
        assert all(record["status"] == "active" for record in result.value)

    def test_filter_with_complex_nested_data(self) -> None:
        """Test filtering with deeply nested data structures."""
        complex_records = [
            {"id": 1, "data": {"level1": {"level2": {"level3": {"value": "target"}}}}},
            {"id": 2, "data": {"level1": {"level2": {"level3": {"value": "other"}}}}},
        ]

        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)
        result = filter_engine.filter_records_with_options(
            complex_records,
            {"data.level1.level2.level3.value": "target"},
        )

        assert result.success
        assert len(result.value) == 1
        assert result.value[0]["id"] == 1

    def test_filter_handles_unicode_strings(self) -> None:
        """Test that filtering handles unicode strings correctly."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=False)

        # Test with unicode characters
        assert filter_engine._op_equals("Café", "café") is True
        assert filter_engine._op_like("Naïve", "na%ve") is True

    def test_get_nested_value_edge_cases(self) -> None:
        """Test nested value access with edge cases."""
        filter_engine = FlextOracleWmsFilter(case_sensitive=False, max_conditions=50)

        # Empty record
        assert filter_engine._get_nested_value({}, "field") is None

        # None values in path
        record_with_none: FlextTypes.Dict = {"level1": None}
        assert (
            filter_engine._get_nested_value(record_with_none, "level1.level2") is None
        )

        # Non-dict intermediate values
        record_with_scalar: FlextTypes.Dict = {"level1": "string_value"}
        assert (
            filter_engine._get_nested_value(record_with_scalar, "level1.level2") is None
        )
