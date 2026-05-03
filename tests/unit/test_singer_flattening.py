"""Test Oracle WMS models - Entity and ApiResponse functionality.

Replaces legacy flattening tests (module removed).

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import pytest

from tests import c, m


class TestsFlextOracleWmsSingerFlattening:
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

    def test_entity_name_min_length(self) -> None:
        """Test entity name must have min length 1."""
        with pytest.raises(c.ValidationError):
            m.OracleWms.Entity(name="", endpoint="/test")

    def test_entity_endpoint_pattern(self) -> None:
        """Test entity endpoint must start with /."""
        with pytest.raises(c.ValidationError):
            m.OracleWms.Entity(name="test", endpoint="no-slash")

    def test_entity_validate_entity_success(self) -> None:
        """Test entity validation success."""
        entity = m.OracleWms.Entity(name="inventory", endpoint="/inventory")
        result = entity.validate_entity()
        assert result.success

    def test_entity_validate_entity_name_too_long(self) -> None:
        """Test entity validation fails for long name."""
        entity = m.OracleWms.Entity(name="x" * 101, endpoint="/test")
        result = entity.validate_entity()
        assert result.failure
        assert result.error is not None
        assert "too long" in result.error

    def test_entity_namespace_access(self) -> None:
        """Test entity accessible via namespace."""
        entity = m.OracleWms.Entity(name="test", endpoint="/test")
        assert isinstance(entity, m.OracleWms.Entity)
