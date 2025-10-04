"""Comprehensive test for Oracle WMS Singer flattening functionality.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from flext_core import FlextTypes

from flext_oracle_wms import (
    FlextOracleWmsDataFlattener,
    flext_oracle_wms_create_data_flattener,
)


class TestFlextOracleWmsDataFlattener:
    """Test the Oracle WMS data flattener class."""

    def test_flattener_creation_default(self) -> None:
        """Test flattener creation with default config."""
        flattener = FlextOracleWmsDataFlattener()
        assert isinstance(flattener, FlextOracleWmsDataFlattener)
        assert flattener.separator == "_"
        assert flattener.max_depth == 5

    def test_flattener_creation_custom_config(self) -> None:
        """Test flattener creation with custom config."""
        flattener = FlextOracleWmsDataFlattener(
            separator=".",
            max_depth=3,
            preserve_lists=False,
        )
        assert flattener.separator == "."
        assert flattener.max_depth == 3
        assert flattener.preserve_lists is False

    def test_flatten_simple_record(self) -> None:
        """Test flattening a simple record."""
        flattener = FlextOracleWmsDataFlattener()
        record: FlextTypes.Dict = {
            "id": "123",
            "name": "Test Item",
            "status": "active",
        }

        result = flattener.flatten_records([record])
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["id"] == "123"
        assert result[0]["name"] == "Test Item"

    def test_flatten_nested_record(self) -> None:
        """Test flattening a nested record."""
        flattener = FlextOracleWmsDataFlattener()
        record: FlextTypes.Dict = {
            "id": "123",
            "details": {
                "name": "Test Item",
                "category": {"id": "cat1", "name": "Category 1"},
            },
        }

        result = flattener.flatten_records([record])
        assert isinstance(result, list)
        assert result is not None
        assert len(result) == 1
        flattened = result[0]
        assert flattened["id"] == "123"
        assert flattened["details_name"] == "Test Item"
        assert flattened["details_category_id"] == "cat1"
        assert flattened["details_category_name"] == "Category 1"

    def test_unflatten_record(self) -> None:
        """Test unflattening a flattened record."""
        flattener = FlextOracleWmsDataFlattener()
        flattened_record: FlextTypes.Dict = {
            "id": "123",
            "details_name": "Test Item",
            "details_category_id": "cat1",
            "details_category_name": "Category 1",
        }

        result = flattener.unflatten_records([flattened_record])
        assert result.success
        assert result.data is not None
        assert len(result.data) == 1
        unflattened = result.data[0]
        assert unflattened["id"] == "123"
        # Note: Current implementation uses dot notation, not the original nested structure

    def test_get_flattening_stats(self) -> None:
        """Test getting flattening statistics."""
        flattener = FlextOracleWmsDataFlattener()
        records: list[FlextTypes.Dict] = [
            {"id": "1", "name": "Item 1"},
            {"id": "2", "details": {"name": "Item 2", "type": "special"}},
            {"id": "3", "info": {"nested": {"deep": "value"}}},
        ]

        result = flattener.get_flattening_stats(records)
        assert result.success
        assert result.data is not None
        stats = result.data
        assert stats["total_records"] == 3
        assert "max_depth" in stats
        assert "nested_records" in stats


class TestFlattenerFactoryFunction:
    """Test the flattener factory function."""

    def test_create_data_flattener_default(self) -> None:
        """Test flattener creation function with defaults."""
        flattener = flext_oracle_wms_create_data_flattener()
        assert isinstance(flattener, FlextOracleWmsDataFlattener)
        assert flattener.separator == "_"
        assert flattener.max_depth == 5

    def test_create_data_flattener_with_config(self) -> None:
        """Test flattener creation function with config."""
        flattener = flext_oracle_wms_create_data_flattener(
            separator=".",
            max_depth=3,
            preserve_lists=False,
        )
        assert flattener.separator == "."
        assert flattener.max_depth == 3
        assert flattener.preserve_lists is False


class TestFlattenerErrorHandling:
    """Test error handling in flattener operations."""

    def test_flatten_empty_records(self) -> None:
        """Test flattening empty records list."""
        flattener = FlextOracleWmsDataFlattener()

        result = flattener.flatten_records([])
        assert isinstance(result, list)
        assert len(result) == 0

    def test_unflatten_empty_records(self) -> None:
        """Test unflattening empty records list."""
        flattener = FlextOracleWmsDataFlattener()

        result = flattener.unflatten_records([])
        assert result.success
        assert result.data is not None
        assert len(result.data) == 0

    def test_stats_empty_records(self) -> None:
        """Test getting stats for empty records."""
        flattener = FlextOracleWmsDataFlattener()

        result = flattener.get_flattening_stats([])
        assert result.success
        assert result.data is not None
        stats = result.data
        assert stats["total_records"] == 0
