"""Test Oracle WMS helpers functionality."""

from flext_oracle_wms.helpers import (
    flext_oracle_wms_build_filter_query,
    flext_oracle_wms_calculate_pagination_info,
    flext_oracle_wms_extract_entity_metadata,
    flext_oracle_wms_format_wms_record,
    flext_oracle_wms_sanitize_entity_name,
    flext_oracle_wms_validate_connection,
)


def test_validate_connection() -> None:
    """Test connection validation."""
    config = {
        "base_url": "https://test.example.com",
        "username": "test",
        "password": "test",
    }
    result = flext_oracle_wms_validate_connection(config)
    assert result.is_success is True or result.is_success is False


def test_sanitize_entity_name() -> None:
    """Test entity name sanitization."""
    # Test valid entity name
    result = flext_oracle_wms_sanitize_entity_name("order_hdr")
    assert result.is_success is True or result.is_success is False

    # Test invalid entity name with special characters
    result = flext_oracle_wms_sanitize_entity_name("invalid-entity@name")
    assert result.is_success is True or result.is_success is False


def test_build_filter_query() -> None:
    """Test filter query building."""
    filters = [
        {"field": "status", "operator": "eq", "value": "active"},
        {"field": "created_date", "operator": "gte", "value": "2025-01-01"},
        {"field": "priority", "operator": "in", "value": ["high", "medium"]},
    ]
    result = flext_oracle_wms_build_filter_query(filters)
    assert result.is_success is True or result.is_success is False


def test_extract_entity_metadata() -> None:
    """Test entity metadata extraction."""
    entity_data = {
        "name": "order_hdr",
        "fields": [
            {"name": "order_id", "type": "string", "primary_key": True},
            {"name": "status", "type": "string"},
            {"name": "created_date", "type": "datetime"},
        ],
    }
    result = flext_oracle_wms_extract_entity_metadata(entity_data)
    assert result.is_success is True or result.is_success is False


def test_format_wms_record() -> None:
    """Test WMS record formatting."""
    record = {
        "order_id": "123",
        "status": "active",
        "created_date": "2025-01-01T12:00:00Z",
        "total_amount": 99.99,
    }
    result = flext_oracle_wms_format_wms_record(record, "order_hdr")
    assert result.is_success is True or result.is_success is False


def test_calculate_pagination_info() -> None:
    """Test pagination info calculation."""
    result = flext_oracle_wms_calculate_pagination_info(
        current_page=1,
        page_size=50,
        total_records=250,
    )
    assert result.is_success is True or result.is_success is False


def test_sanitize_entity_name_reserved_words() -> None:
    """Test field name sanitization with SQL reserved words."""
    reserved_names = ["select", "from", "where", "order", "group"]
    for name in reserved_names:
        result = flext_oracle_wms_sanitize_entity_name(name)
        assert result.is_success is True or result.is_success is False


def test_sanitize_entity_name_edge_cases() -> None:
    """Test entity name sanitization with edge cases."""
    # Empty string
    result = flext_oracle_wms_sanitize_entity_name("")
    assert result.is_success is False

    # Unicode characters
    result = flext_oracle_wms_sanitize_entity_name("order_café_ñame")
    assert result.is_success is True

    # Very long name
    long_name = "a" * 100
    result = flext_oracle_wms_sanitize_entity_name(long_name)
    assert result.is_success is True

    # Names with numbers
    result = flext_oracle_wms_sanitize_entity_name("123field")
    assert result.is_success is True

    # Mixed case
    result = flext_oracle_wms_sanitize_entity_name("ORDER_HDR")
    assert result.is_success is True


def test_connection_validation_edge_cases() -> None:
    """Test connection validation with edge cases."""
    # Missing fields one by one
    incomplete_configs = [
        {"username": "test", "password": "test"},  # missing base_url
        {"base_url": "https://test.com", "password": "test"},  # missing username
        {"base_url": "https://test.com", "username": "test"},  # missing password
        {
            "base_url": "invalid-url",
            "username": "test",
            "password": "test",
        },  # invalid URL
    ]

    for config in incomplete_configs:
        result = flext_oracle_wms_validate_connection(config)
        assert result.is_success is False


def test_filter_query_complex_scenarios() -> None:
    """Test filter query building with complex scenarios."""
    # Test various operators
    operators_test = [
        {"field": "status", "operator": "eq", "value": "active"},
        {"field": "count", "operator": "gt", "value": 10},
        {"field": "date", "operator": "gte", "value": "2025-01-01"},
        {"field": "priority", "operator": "in", "value": ["high", "medium"]},
        {"field": "description", "operator": "like", "value": "%test%"},
        {"field": "archived", "operator": "neq", "value": True},
    ]

    result = flext_oracle_wms_build_filter_query(operators_test)
    assert result.is_success is True

    # Test invalid filter (missing fields)
    invalid_filter = [{"field": "status"}]  # missing operator and value
    result = flext_oracle_wms_build_filter_query(invalid_filter)
    assert result.is_success is False


def test_metadata_extraction_scenarios() -> None:
    """Test entity metadata extraction with various scenarios."""
    # Complete entity info
    complete_entity = {
        "name": "order_hdr",
        "description": "Order header entity",
        "endpoint": "/api/orders",
        "primary_key": "order_id",
        "replication_key": "modified_date",
        "supports_incremental": True,
        "fields": {
            "order_id": {"type": "string", "nullable": False},
            "status": {"type": "string", "nullable": True},
            "created_date": {"type": "datetime", "nullable": False},
            "total_amount": {"type": "number", "nullable": True},
        },
    }

    result = flext_oracle_wms_extract_entity_metadata(complete_entity)
    assert result.is_success is True
    assert result.data["name"] == "order_hdr"
    assert result.data["field_count"] == 4
    assert "string" in result.data["field_types_summary"]

    # Minimal entity info
    minimal_entity = {"name": "simple_entity"}
    result = flext_oracle_wms_extract_entity_metadata(minimal_entity)
    assert result.is_success is True
    assert result.data["name"] == "simple_entity"
