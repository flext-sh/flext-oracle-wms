"""Test Oracle WMS models - Entity and ApiResponse functionality.

Replaces legacy flattening tests (module removed).

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

import pytest
from flext_oracle_wms import (
    FlextOracleWmsApiResponse,
    FlextOracleWmsEntity,
    FlextOracleWmsModels,
)
from pydantic import ValidationError


class TestFlextOracleWmsEntity:
    """Test the Oracle WMS Entity model."""

    def test_entity_creation_valid(self) -> None:
        """Test entity creation with valid parameters."""
        entity = m.OracleWms.Entity(name="inventory", endpoint="/inventory")
        assert entity.name == "inventory"
        assert entity.endpoint == "/inventory"
        assert entity.description is None
        assert entity.primary_key is None
        assert entity.replication_key is None
        assert entity.supports_incremental is False

    def test_entity_creation_all_fields(self) -> None:
        """Test entity creation with all fields."""
        entity = m.OracleWms.Entity(
            name="orders",
            endpoint="/orders",
            description="Order data",
            primary_key="order_id",
            replication_key="updated_at",
            supports_incremental=True,
        )
        assert entity.name == "orders"
        assert entity.endpoint == "/orders"
        assert entity.description == "Order data"
        assert entity.primary_key == "order_id"
        assert entity.replication_key == "updated_at"
        assert entity.supports_incremental is True

    def test_entity_name_min_length(self) -> None:
        """Test entity name must have min length 1."""
        with pytest.raises(ValidationError):
            m.OracleWms.Entity(name="", endpoint="/test")

    def test_entity_endpoint_pattern(self) -> None:
        """Test entity endpoint must start with /."""
        with pytest.raises(ValidationError):
            m.OracleWms.Entity(name="test", endpoint="no-slash")

    def test_entity_validate_entity_success(self) -> None:
        """Test entity validation success."""
        entity = m.OracleWms.Entity(name="inventory", endpoint="/inventory")
        result = entity.validate_entity()
        assert result.is_success

    def test_entity_validate_entity_name_too_long(self) -> None:
        """Test entity validation fails for long name."""
        entity = m.OracleWms.Entity(name="x" * 101, endpoint="/test")
        result = entity.validate_entity()
        assert result.is_failure
        assert result.error is not None
        assert "too long" in result.error

    def test_entity_namespace_access(self) -> None:
        """Test entity accessible via namespace."""
        entity = FlextOracleWmsModels.OracleWms.Entity(
            name="test",
            endpoint="/test",
        )
        assert isinstance(entity, m.OracleWms.Entity)


class TestFlextOracleWmsApiResponse:
    """Test the Oracle WMS ApiResponse model."""

    def test_response_defaults(self) -> None:
        """Test response creation with defaults."""
        response = m.OracleWms.ApiResponse()
        assert response.data == {}
        assert response.status_code == 200
        assert response.success is True
        assert response.error_message is None

    def test_response_custom_fields(self) -> None:
        """Test response creation with custom fields."""
        response = m.OracleWms.ApiResponse(
            data={"key": "value"},
            status_code=201,
            success=True,
            error_message=None,
        )
        assert response.data == {"key": "value"}
        assert response.status_code == 201

    def test_response_error(self) -> None:
        """Test response with error."""
        response = m.OracleWms.ApiResponse(
            success=False,
            error_message="Something went wrong",
            status_code=500,
        )
        assert response.success is False
        assert response.error_message == "Something went wrong"

    def test_response_validate_success(self) -> None:
        """Test response validation success."""
        response = m.OracleWms.ApiResponse(success=True)
        result = response.validate_response()
        assert result.is_success

    def test_response_validate_failure_needs_message(self) -> None:
        """Test failed response without error message fails validation."""
        response = m.OracleWms.ApiResponse(success=False, error_message=None)
        result = response.validate_response()
        assert result.is_failure
        assert result.error is not None
        assert "error message" in result.error

    def test_response_validate_failure_with_message(self) -> None:
        """Test failed response with error message passes validation."""
        response = m.OracleWms.ApiResponse(
            success=False,
            error_message="Error occurred",
        )
        result = response.validate_response()
        assert result.is_success

    def test_response_status_code_bounds(self) -> None:
        """Test status code validation bounds."""
        with pytest.raises(ValidationError):
            m.OracleWms.ApiResponse(status_code=199)

        with pytest.raises(ValidationError):
            m.OracleWms.ApiResponse(status_code=600)

    def test_response_namespace_access(self) -> None:
        """Test response accessible via namespace."""
        response = FlextOracleWmsModels.OracleWms.ApiResponse(
            data={"test": True},
            status_code=200,
        )
        assert isinstance(response, m.OracleWms.ApiResponse)
