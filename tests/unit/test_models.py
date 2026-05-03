"""Tests for Oracle WMS data models.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import pytest

from tests import c, m


class TestsFlextOracleWmsModelsUnit:
    """Behavior contract for test_models."""

    def test_entity_defaults(self) -> None:
        """Test entity default values."""
        entity = m.OracleWms.Entity(name="item", endpoint="/api/items")
        assert entity.description is None
        assert entity.primary_key is None
        assert entity.replication_key is None
        assert entity.supports_incremental is False

    def test_entity_validation_empty_name_raises(self) -> None:
        """Test entity with empty name raises c.ValidationError (min_length=1)."""
        with pytest.raises(c.ValidationError):
            m.OracleWms.Entity(name="", endpoint="/api/items")

    def test_entity_validation_bad_endpoint_raises(self) -> None:
        """Test entity with non-slash endpoint raises c.ValidationError."""
        with pytest.raises(c.ValidationError):
            m.OracleWms.Entity(name="item", endpoint="api/items")

    def test_entity_validate_entity_success(self) -> None:
        """Test validate_entity returns success for valid entity."""
        entity = m.OracleWms.Entity(name="item_master", endpoint="/api/items")
        result = entity.validate_entity()
        assert result.success
