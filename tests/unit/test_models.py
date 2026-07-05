"""Tests for Oracle WMS data models.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import pytest

from tests.constants import c
from tests.models import m

__all__: list[str] = ["TestsFlextOracleWmsModelsUnit"]


class TestsFlextOracleWmsModelsUnit:
    """Observable contract for m.OracleWms.Entity."""

    def test_entity_exposes_supplied_required_fields(self) -> None:
        """Required fields are readable through the public model state."""
        entity = m.OracleWms.Entity(name="item", endpoint="/api/items")
        assert entity.name == "item"
        assert entity.endpoint == "/api/items"

    def test_entity_optional_fields_default_to_none_and_false(self) -> None:
        """Unset optional fields expose documented defaults."""
        entity = m.OracleWms.Entity(name="item", endpoint="/api/items")
        assert entity.description is None
        assert entity.primary_key is None
        assert entity.replication_key is None
        assert entity.supports_incremental is False

    def test_entity_model_dump_roundtrips_public_state(self) -> None:
        """model_dump reflects exactly the supplied public state."""
        entity = m.OracleWms.Entity(
            name="item_master",
            endpoint="/api/items",
            description="Master items",
            primary_key="id",
            replication_key="mod_ts",
            supports_incremental=True,
        )
        assert entity.model_dump() == {
            "name": "item_master",
            "endpoint": "/api/items",
            "description": "Master items",
            "primary_key": "id",
            "replication_key": "mod_ts",
            "supports_incremental": True,
        }

    @pytest.mark.parametrize(
        ("field", "value"),
        [
            ("name", ""),
            ("endpoint", ""),
        ],
    )
    def test_entity_rejects_empty_required_string(
        self,
        field: str,
        value: str,
    ) -> None:
        """Empty required strings violate min_length and raise ValidationError."""
        kwargs: dict[str, str] = {"name": "item", "endpoint": "/api/items"}
        kwargs[field] = value
        with pytest.raises(c.ValidationError):
            m.OracleWms.Entity(**kwargs)

    @pytest.mark.parametrize(
        "endpoint",
        ["api/items", "items", "http://x/api"],
    )
    def test_entity_rejects_endpoint_without_leading_slash(
        self,
        endpoint: str,
    ) -> None:
        """Endpoint validator enforces a leading slash contract."""
        with pytest.raises(c.ValidationError):
            m.OracleWms.Entity(name="item", endpoint=endpoint)

    def test_entity_forbids_unknown_fields(self) -> None:
        """extra='forbid' rejects fields outside the declared contract."""
        with pytest.raises(c.ValidationError):
            m.OracleWms.Entity(
                name="item",
                endpoint="/api/items",
                unexpected="x",
            )

    def test_validate_entity_succeeds_for_valid_entity(self) -> None:
        """validate_entity returns a success result carrying True."""
        entity = m.OracleWms.Entity(name="item_master", endpoint="/api/items")
        result = entity.validate_entity()
        assert result.success
        assert result.unwrap() is True

    def test_validate_entity_fails_when_name_exceeds_max_length(self) -> None:
        """A too-long name is a business-rule failure, not a construction error."""
        limit = c.OracleWms.WmsEntities.MAX_ENTITY_NAME_LENGTH
        entity = m.OracleWms.Entity(name="x" * (limit + 1), endpoint="/api/items")
        result = entity.validate_entity()
        assert result.failure
        assert result.error is not None
        assert "too long" in result.error

    def test_validate_entity_accepts_name_at_max_length(self) -> None:
        """Name exactly at the boundary is still valid (inclusive limit)."""
        limit = c.OracleWms.WmsEntities.MAX_ENTITY_NAME_LENGTH
        entity = m.OracleWms.Entity(name="x" * limit, endpoint="/api/items")
        assert entity.validate_entity().success
