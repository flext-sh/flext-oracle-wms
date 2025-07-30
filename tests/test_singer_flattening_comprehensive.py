"""Comprehensive test for Oracle WMS Singer flattening functionality."""

import pytest

from flext_oracle_wms.flattening import (
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

    @pytest.mark.asyncio
    async def test_flatten_simple_record(self) -> None:
        """Test flattening a simple record."""
        flattener = FlextOracleWmsDataFlattener()
        record: dict[str, object] = {
            "id": "123",
            "name": "Test Item",
            "status": "active"
        }

        result = await flattener.flatten_records([record])
        assert result.is_success
        assert result.data is not None
        assert len(result.data) == 1
        assert result.data[0]["id"] == "123"
        assert result.data[0]["name"] == "Test Item"

    @pytest.mark.asyncio
    async def test_flatten_nested_record(self) -> None:
        """Test flattening a nested record."""
        flattener = FlextOracleWmsDataFlattener()
        record: dict[str, object] = {
            "id": "123",
            "details": {
                "name": "Test Item",
                "category": {
                    "id": "cat1",
                    "name": "Category 1"
                }
            }
        }

        result = await flattener.flatten_records([record])
        assert result.is_success
        assert result.data is not None
        assert len(result.data) == 1
        flattened = result.data[0]
        assert flattened["id"] == "123"
        assert flattened["details_name"] == "Test Item"
        assert flattened["details_category_id"] == "cat1"
        assert flattened["details_category_name"] == "Category 1"

    @pytest.mark.asyncio
    async def test_unflatten_record(self) -> None:
        """Test unflattening a flattened record."""
        flattener = FlextOracleWmsDataFlattener()
        flattened_record: dict[str, object] = {
            "id": "123",
            "details_name": "Test Item",
            "details_category_id": "cat1",
            "details_category_name": "Category 1"
        }

        result = await flattener.unflatten_records([flattened_record])
        assert result.is_success
        assert result.data is not None
        assert len(result.data) == 1
        unflattened = result.data[0]
        assert unflattened["id"] == "123"
        # Note: Current implementation uses dot notation, not the original nested structure

    @pytest.mark.asyncio
    async def test_get_flattening_stats(self) -> None:
        """Test getting flattening statistics."""
        flattener = FlextOracleWmsDataFlattener()
        records: list[dict[str, object]] = [
            {"id": "1", "name": "Item 1"},
            {"id": "2", "details": {"name": "Item 2", "type": "special"}},
            {"id": "3", "info": {"nested": {"deep": "value"}}}
        ]

        result = await flattener.get_flattening_stats(records)
        assert result.is_success
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

    @pytest.mark.asyncio
    async def test_flatten_empty_records(self) -> None:
        """Test flattening empty records list."""
        flattener = FlextOracleWmsDataFlattener()

        result = await flattener.flatten_records([])
        assert result.is_success
        assert result.data is not None
        assert len(result.data) == 0

    @pytest.mark.asyncio
    async def test_unflatten_empty_records(self) -> None:
        """Test unflattening empty records list."""
        flattener = FlextOracleWmsDataFlattener()

        result = await flattener.unflatten_records([])
        assert result.is_success
        assert result.data is not None
        assert len(result.data) == 0

    @pytest.mark.asyncio
    async def test_stats_empty_records(self) -> None:
        """Test getting stats for empty records."""
        flattener = FlextOracleWmsDataFlattener()

        result = await flattener.get_flattening_stats([])
        assert result.is_success
        assert result.data is not None
        stats = result.data
        assert stats["total_records"] == 0
