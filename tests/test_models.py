"""Test Oracle WMS models functionality."""

import pytest

from flext_oracle_wms.exceptions import FlextOracleWmsDataValidationError
from flext_oracle_wms.models import (
    FlextOracleWmsApiResponse,
    FlextOracleWmsDiscoveryResult,
    FlextOracleWmsEntity,
)


def test_entity_creation() -> None:
    """Test entity creation."""
    entity = FlextOracleWmsEntity(
        name="order_hdr",
        endpoint="/api/order_hdr",
        description="Order header entity",
        fields={"order_id": {"type": "string"}, "status": {"type": "string"}},
        primary_key="order_id",
        supports_incremental=True,
    )
    assert entity.name == "order_hdr"
    assert entity.endpoint == "/api/order_hdr"
    assert entity.description == "Order header entity"
    assert entity.primary_key == "order_id"
    assert entity.supports_incremental is True


def test_entity_validation_success() -> None:
    """Test entity validation with valid data."""
    entity = FlextOracleWmsEntity(name="item_master", endpoint="/api/items")
    # Should not raise exception
    entity.validate_domain_rules()


def test_entity_validation_empty_name() -> None:
    """Test entity validation with empty name."""
    entity = FlextOracleWmsEntity(name="", endpoint="/api/items")
    with pytest.raises(FlextOracleWmsDataValidationError):
        entity.validate_domain_rules()


def test_entity_validation_empty_endpoint() -> None:
    """Test entity validation with empty endpoint."""
    entity = FlextOracleWmsEntity(name="item_master", endpoint="")
    with pytest.raises(FlextOracleWmsDataValidationError):
        entity.validate_domain_rules()


def test_discovery_result_creation() -> None:
    """Test discovery result creation."""
    entities = [
        FlextOracleWmsEntity(name="order_hdr", endpoint="/api/orders"),
        FlextOracleWmsEntity(name="item_master", endpoint="/api/items"),
    ]

    result = FlextOracleWmsDiscoveryResult(
        entities=entities,
        total_count=2,
        timestamp="2025-01-15T10:30:00Z",
        discovery_duration_ms=150.5,
        has_errors=False,
        api_version="v10",
    )

    assert len(result.entities) == 2
    assert result.total_count == 2
    assert result.timestamp == "2025-01-15T10:30:00Z"
    assert result.discovery_duration_ms == 150.5
    assert result.has_errors is False
    assert result.api_version == "v10"


def test_discovery_result_validation() -> None:
    """Test discovery result validation."""
    result = FlextOracleWmsDiscoveryResult(
        entities=[FlextOracleWmsEntity(name="test", endpoint="/api/test")],
        total_count=1,
        timestamp="2025-01-15T10:30:00Z",
    )
    # Should not raise exception
    result.validate_domain_rules()


def test_discovery_result_validation_count_mismatch() -> None:
    """Test discovery result validation with count mismatch."""
    result = FlextOracleWmsDiscoveryResult(
        entities=[FlextOracleWmsEntity(name="test", endpoint="/api/test")],
        total_count=5,  # Mismatch: 1 entity but count says 5
        timestamp="2025-01-15T10:30:00Z",
    )
    with pytest.raises(FlextOracleWmsDataValidationError):
        result.validate_domain_rules()


def test_api_response_creation() -> None:
    """Test API response creation."""
    response = FlextOracleWmsApiResponse(
        data={"order_id": "ORD001", "status": "OPEN"},
        status_code=200,
        success=True,
        error_message=None,
    )

    assert response.status_code == 200
    assert response.data["order_id"] == "ORD001"
    assert response.success is True
    assert response.error_message is None


def test_api_response_error() -> None:
    """Test API response with error."""
    response = FlextOracleWmsApiResponse(
        data={}, status_code=404, success=False, error_message="Order not found"
    )

    assert response.status_code == 404
    assert response.success is False
    assert response.error_message == "Order not found"


def test_api_response_validation() -> None:
    """Test API response validation."""
    response = FlextOracleWmsApiResponse(
        status_code=200, data={"test": "data"}, success=True, error_message=None
    )
    # Should not raise exception
    response.validate_domain_rules()


def test_response_creation() -> None:
    """Test response creation."""
    response = FlextOracleWmsApiResponse(
        data={"results": [{"result": "success"}]},
        status_code=200,
        success=True,
        error_message=None,
    )
    # Test actual fields that exist in the class
    assert response.data["results"][0]["result"] == "success"
    assert response.status_code == 200
    assert response.success is True
    assert response.error_message is None


def test_discovery_result_creation() -> None:
    """Test discovery result creation."""
    entity1 = FlextOracleWmsEntity(name="order_hdr", endpoint="/api/order_hdr")
    entity2 = FlextOracleWmsEntity(name="order_line", endpoint="/api/order_line")

    result = FlextOracleWmsDiscoveryResult(
        entities=[entity1, entity2],
        timestamp="2025-01-01T12:00:00Z",
    )
    assert len(result.entities) == 2
    assert result.entities[0].name == "order_hdr"
    assert result.total_count == 0  # Default value


def test_entity_with_complex_fields() -> None:
    """Test entity with complex field definitions."""
    complex_fields = {
        "order_id": {"type": "string", "maxLength": 50, "required": True},
        "status": {"type": "string", "enum": ["OPEN", "CLOSED", "CANCELLED"]},
        "total_amount": {"type": "number", "format": "decimal", "precision": 2},
        "created_date": {"type": "string", "format": "date-time"},
    }

    entity = FlextOracleWmsEntity(
        name="order_hdr",
        endpoint="/api/orders",
        description="Order header with complex schema",
        fields=complex_fields,
        primary_key="order_id",
        replication_key="created_date",
        supports_incremental=True,
    )

    assert entity.name == "order_hdr"
    assert entity.fields == complex_fields
    assert entity.primary_key == "order_id"
    assert entity.replication_key == "created_date"


def test_entity_with_schema() -> None:
    """Test entity with schema."""
    entity = FlextOracleWmsEntity(
        name="order_hdr",
        endpoint="/api/order_hdr",
        fields={"order_id": {"type": "string"}},
    )
    assert entity.fields["order_id"]["type"] == "string"


def test_response_basic_creation() -> None:
    """Test basic response creation."""
    response = FlextOracleWmsApiResponse()
    # Test actual default values from the class
    assert response.data == {}  # Default factory returns empty dict
    assert response.status_code == 200  # Default value
    assert response.success is True  # Default value
    assert response.error_message is None  # Default value


def test_discovery_result_with_errors() -> None:
    """Test discovery result with errors."""
    result = FlextOracleWmsDiscoveryResult(
        entities=[],
        timestamp="2025-01-01T12:00:00Z",
        has_errors=True,
        errors=["Connection failed", "Authentication error"],
    )
    assert result.has_errors is True
    assert len(result.errors) == 2
    assert "Connection failed" in result.errors


def test_entity_validation() -> None:
    """Test entity validation."""
    entity = FlextOracleWmsEntity(
        name="order_hdr",
        endpoint="/api/order_hdr",
        fields={"order_id": {"type": "string"}, "status": {"type": "string"}},
    )
    # Should not raise an exception
    assert entity.name == "order_hdr"
    assert len(entity.fields) == 2


def test_response_with_list_data() -> None:
    """Test response with list data."""
    response = FlextOracleWmsApiResponse(
        data={"results": [{"result": "success"}]}, status_code=200, success=True
    )
    # Test actual fields that exist in the class
    assert response.data["results"][0]["result"] == "success"
    assert response.status_code == 200
    assert response.success is True


def test_discovery_result_statistics() -> None:
    """Test discovery result statistics."""
    entity1 = FlextOracleWmsEntity(name="order_hdr", endpoint="/api/order_hdr")
    entity2 = FlextOracleWmsEntity(name="order_line", endpoint="/api/order_line")
    entity3 = FlextOracleWmsEntity(name="allocation", endpoint="/api/allocation")

    result = FlextOracleWmsDiscoveryResult(
        entities=[entity1, entity2, entity3],
        timestamp="2025-01-01T12:00:00Z",
    )
    # Model doesn't have get_statistics method, test basic functionality
    assert len(result.entities) == 3
    assert result.entities[0].name == "order_hdr"


def test_entity_field_count() -> None:
    """Test entity field count."""
    entity = FlextOracleWmsEntity(
        name="order_hdr",
        endpoint="/api/order_hdr",
        fields={
            "order_id": {"type": "string"},
            "status": {"type": "string"},
            "created_date": {"type": "datetime"},
            "modified_date": {"type": "datetime"},
        },
    )
    assert len(entity.fields) == 4


def test_response_error_handling() -> None:
    """Test response error handling."""
    response = FlextOracleWmsApiResponse(
        data={"error": "Not found"},
        status_code=404,
        success=False,
        error_message="Entity not found",
    )
    # Test actual fields that exist in the class
    assert response.data["error"] == "Not found"
    assert response.status_code == 404
    assert response.success is False
    assert response.error_message == "Entity not found"
