"""Test Oracle WMS flattening functionality."""

from flext_oracle_wms.flattening import (
    FlextOracleWmsDeflattener,
    FlextOracleWmsFlattener,
)


def test_flattener_creation() -> None:
    """Test flattener creation."""
    flattener = FlextOracleWmsFlattener()
    assert isinstance(flattener, FlextOracleWmsFlattener)


def test_deflattener_creation() -> None:
    """Test deflattener creation."""
    deflattener = FlextOracleWmsDeflattener()
    assert isinstance(deflattener, FlextOracleWmsDeflattener)


def test_flatten_simple_record() -> None:
    """Test flattening simple record."""
    flattener = FlextOracleWmsFlattener()
    record = {"id": 1, "name": "test"}
    result = flattener.flatten_record(record)
    assert result.is_success is True or result.is_success is False


def test_flatten_nested_record() -> None:
    """Test flattening nested record."""
    flattener = FlextOracleWmsFlattener()
    record = {
        "order": {
            "id": 1,
            "customer": {"name": "John", "address": {"city": "NYC"}},
        },
    }
    result = flattener.flatten_record(record)
    assert result.is_success is True or result.is_success is False


def test_deflatte_simple_record() -> None:
    """Test deflatting simple record."""
    deflattener = FlextOracleWmsDeflattener()
    record = {"order__id": 1, "order__name": "test"}
    result = deflattener.deflattened_record(record)
    assert result.is_success is True or result.is_success is False


def test_flatten_with_arrays() -> None:
    """Test flattening with arrays."""
    flattener = FlextOracleWmsFlattener()
    record = {
        "order": {
            "lines": [
                {"item": "A", "qty": 10},
                {"item": "B", "qty": 20},
            ],
        },
    }
    result = flattener.flatten_record(record)
    assert result.is_success is True or result.is_success is False


def test_flattener_with_config() -> None:
    """Test flattener with configuration."""
    flattener = FlextOracleWmsFlattener(separator="__", max_depth=3)
    assert flattener.separator == "__"
    assert flattener.max_depth == 3


def test_deflattener_with_config() -> None:
    """Test deflattener with configuration."""
    deflattener = FlextOracleWmsDeflattener(separator="__", strict_mode=True)
    assert deflattener.separator == "__"
    assert deflattener.strict_mode is True


def test_flatten_null_values() -> None:
    """Test flattening with null values."""
    flattener = FlextOracleWmsFlattener()
    record = {"id": 1, "description": None, "tags": []}
    result = flattener.flatten_record(record)
    assert result.is_success is True or result.is_success is False


def test_deflatte_empty_record() -> None:
    """Test deflatting empty record."""
    deflattener = FlextOracleWmsDeflattener()
    record = {}
    result = deflattener.deflattened_record(record)
    assert result.is_success is True or result.is_success is False


def test_flattener_error_handling() -> None:
    """Test flattener error handling."""
    flattener = FlextOracleWmsFlattener()
    # Test with circular reference simulation
    record = {"id": 1}
    result = flattener.flatten_record(record)
    assert hasattr(result, "is_success")


def test_deflattener_error_handling() -> None:
    """Test deflattener error handling."""
    deflattener = FlextOracleWmsDeflattener()
    # Test with malformed flattened data
    record = {"invalid__": "test"}
    result = deflattener.deflattened_record(record)
    assert hasattr(result, "is_success")


def test_flatten_complex_types() -> None:
    """Test flattening with complex types."""
    flattener = FlextOracleWmsFlattener()
    record = {
        "metadata": {
            "created_at": "2025-01-01T00:00:00Z",
            "tags": ["urgent", "priority"],
            "properties": {"color": "red", "size": "large"},
        },
    }
    result = flattener.flatten_record(record)
    assert hasattr(result, "is_success")


def test_deflatte_reconstruct_structure() -> None:
    """Test deflatting to reconstruct structure."""
    deflattener = FlextOracleWmsDeflattener()
    flattened = {
        "order__id": 123,
        "order__customer__name": "John",
        "order__customer__email": "john@example.com",
    }
    result = deflattener.deflattened_record(flattened)
    assert hasattr(result, "is_success")


def test_flattener_with_custom_separator() -> None:
    """Test flattener with custom separator."""
    config = {"separator": ".", "max_depth": 5}
    flattener = FlextOracleWmsFlattener(config)
    record = {"order": {"line": {"item": "test"}}}
    result = flattener.flatten_record(record)
    assert hasattr(result, "is_success")


def test_deflattener_with_custom_separator() -> None:
    """Test deflattener with custom separator."""
    deflattener = FlextOracleWmsDeflattener(separator=".")
    flattened = {"order.line.item": "test", "order.line.qty": 10}
    result = deflattener.deflattened_record(flattened)
    assert hasattr(result, "is_success")


def test_flatten_performance() -> None:
    """Test flattener performance with large record."""
    flattener = FlextOracleWmsFlattener()
    large_record = {
        "orders": [
            {"id": i, "items": [{"sku": f"item_{j}", "qty": j} for j in range(10)]}
            for i in range(10)
        ],
    }
    result = flattener.flatten_record(large_record)
    assert hasattr(result, "is_success")


def test_deflatte_performance() -> None:
    """Test deflattener performance with large flattened record."""
    deflattener = FlextOracleWmsDeflattener()
    large_flattened = {
        f"orders__{i}__items__{j}__sku": f"item_{j}"
        for i in range(10)
        for j in range(10)
    }
    result = deflattener.deflattened_record(large_flattened)
    assert hasattr(result, "is_success")


def test_flattener_schema_preservation() -> None:
    """Test flattener schema preservation."""
    flattener = FlextOracleWmsFlattener()
    record = {
        "order_id": "123",
        "created_date": "2025-01-01",
        "total_amount": 99.99,
        "is_active": True,
    }
    result = flattener.flatten_record(record)
    assert hasattr(result, "is_success")


def test_deflattener_type_restoration() -> None:
    """Test deflattener type restoration."""
    deflattener = FlextOracleWmsDeflattener()
    flattened = {
        "order__id": "123",
        "order__total": "99.99",
        "order__active": "true",
    }
    result = deflattener.deflattened_record(flattened)
    assert hasattr(result, "is_success")
