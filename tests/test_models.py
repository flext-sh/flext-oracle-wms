"""Tests for Oracle WMS data models.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

import pytest
from pydantic import ValidationError

from flext_oracle_wms import (
    FlextOracleWmsApiResponse,
    FlextOracleWmsEntity,
)


def test_entity_creation() -> None:
    """Test entity creation with valid fields."""
    entity = FlextOracleWmsEntity(
        name="order_hdr",
        endpoint="/api/order_hdr",
        description="Order header entity",
        primary_key="order_id",
        supports_incremental=True,
    )
    assert entity.name == "order_hdr"
    assert entity.endpoint == "/api/order_hdr"
    assert entity.description == "Order header entity"
    assert entity.primary_key == "order_id"
    assert entity.supports_incremental is True


def test_entity_defaults() -> None:
    """Test entity default values."""
    entity = FlextOracleWmsEntity(name="item", endpoint="/api/items")
    assert entity.description is None
    assert entity.primary_key is None
    assert entity.replication_key is None
    assert entity.supports_incremental is False


def test_entity_validation_empty_name_raises() -> None:
    """Test entity with empty name raises ValidationError (min_length=1)."""
    with pytest.raises(ValidationError):
        FlextOracleWmsEntity(name="", endpoint="/api/items")


def test_entity_validation_bad_endpoint_raises() -> None:
    """Test entity with non-slash endpoint raises ValidationError."""
    with pytest.raises(ValidationError):
        FlextOracleWmsEntity(name="item", endpoint="api/items")


def test_entity_validate_entity_success() -> None:
    """Test validate_entity returns success for valid entity."""
    entity = FlextOracleWmsEntity(name="item_master", endpoint="/api/items")
    result = entity.validate_entity()
    assert result.is_success


def test_api_response_creation() -> None:
    """Test API response creation."""
    response = FlextOracleWmsApiResponse(
        data={"order_id": "ORD001"},
        status_code=200,
        success=True,
    )
    assert response.status_code == 200
    assert response.data["order_id"] == "ORD001"
    assert response.success is True
    assert response.error_message is None


def test_api_response_error() -> None:
    """Test API response with error."""
    response = FlextOracleWmsApiResponse(
        data={},
        status_code=404,
        success=False,
        error_message="Order not found",
    )
    assert response.status_code == 404
    assert response.success is False
    assert response.error_message == "Order not found"


def test_api_response_defaults() -> None:
    """Test API response default values."""
    response = FlextOracleWmsApiResponse()
    assert response.data == {}
    assert response.status_code == 200
    assert response.success is True
    assert response.error_message is None


def test_api_response_validate_response_success() -> None:
    """Test validate_response returns success for valid response."""
    response = FlextOracleWmsApiResponse(success=True, data={"test": "data"})
    result = response.validate_response()
    assert result.is_success


def test_api_response_validate_response_failure() -> None:
    """Test validate_response fails when success=False with no error_message."""
    response = FlextOracleWmsApiResponse(success=False)
    result = response.validate_response()
    assert result.is_failure


def test_api_response_with_nested_data() -> None:
    """Test API response with nested data."""
    response = FlextOracleWmsApiResponse(
        data={"results": [{"id": 1}, {"id": 2}]},
        status_code=200,
        success=True,
    )
    assert isinstance(response.data["results"], list)
    assert len(response.data["results"]) == 2
