"""Tests for Oracle WMS data models.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import pytest

from flext_oracle_wms import FlextOracleWmsUtilitiesDiscovery
from flext_tests import tm
from tests import c, m, t


class TestsFlextOracleWmsModelsUnit:
    """Observable contract for m.OracleWms.Entity."""

    def test_entity_exposes_supplied_required_fields(self) -> None:
        """Required fields are readable through the public model state."""
        entity = m.OracleWms.Entity(name="item", endpoint="/api/items")
        tm.that(entity.name, eq="item")
        tm.that(entity.endpoint, eq="/api/items")

    def test_entity_optional_fields_default_to_none_and_false(self) -> None:
        """Unset optional fields expose documented defaults."""
        entity = m.OracleWms.Entity(name="item", endpoint="/api/items")
        tm.that(entity.description, none=True)
        tm.that(entity.primary_key, none=True)
        tm.that(entity.replication_key, none=True)
        tm.that(entity.supports_incremental, eq=False)

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
        tm.that(
            entity.model_dump(),
            eq={
                "name": "item_master",
                "endpoint": "/api/items",
                "description": "Master items",
                "primary_key": "id",
                "replication_key": "mod_ts",
                "supports_incremental": True,
            },
        )

    @pytest.mark.parametrize(("field", "value"), [("name", ""), ("endpoint", "")])
    def test_entity_rejects_empty_required_string(self, field: str, value: str) -> None:
        """Empty required strings violate min_length and raise ValidationError."""
        kwargs: t.MutableMappingKV[str, str] = {
            "name": "item",
            "endpoint": "/api/items",
        }
        kwargs[field] = value
        with pytest.raises(c.ValidationError):
            m.OracleWms.Entity(**kwargs)

    @pytest.mark.parametrize("endpoint", ["api/items", "items", "http://x/api"])
    def test_entity_rejects_endpoint_without_leading_slash(self, endpoint: str) -> None:
        """Endpoint validator enforces a leading slash contract."""
        with pytest.raises(c.ValidationError):
            m.OracleWms.Entity(name="item", endpoint=endpoint)

    def test_entity_forbids_unknown_fields(self) -> None:
        """extra='forbid' rejects fields outside the declared contract."""
        with pytest.raises(c.ValidationError):
            m.OracleWms.Entity(name="item", endpoint="/api/items", unexpected="x")

    def test_validate_entity_succeeds_for_valid_entity(self) -> None:
        """validate_entity returns a success result carrying True."""
        entity = m.OracleWms.Entity(name="item_master", endpoint="/api/items")
        result = FlextOracleWmsUtilitiesDiscovery.validate_wms_entity(entity)
        tm.ok(result)
        tm.that(result.unwrap(), eq=True)

    def test_validate_entity_fails_when_name_exceeds_max_length(self) -> None:
        """A too-long name is a business-rule failure, not a construction error."""
        limit = c.OracleWms.WmsEntities.MAX_ENTITY_NAME_LENGTH
        entity = m.OracleWms.Entity(name="x" * (limit + 1), endpoint="/api/items")
        result = FlextOracleWmsUtilitiesDiscovery.validate_wms_entity(entity)
        tm.fail(result)
        tm.that(result.error, none=False)
        tm.that(result.error, has="too long")

    def test_validate_entity_accepts_name_at_max_length(self) -> None:
        """Name exactly at the boundary is still valid (inclusive limit)."""
        limit = c.OracleWms.WmsEntities.MAX_ENTITY_NAME_LENGTH
        entity = m.OracleWms.Entity(name="x" * limit, endpoint="/api/items")
        tm.ok(FlextOracleWmsUtilitiesDiscovery.validate_wms_entity(entity))


__all__: list[str] = ["TestsFlextOracleWmsModelsUnit"]
