"""Behavioral tests for the Oracle WMS Entity model public contract.

Replaces legacy flattening tests (module removed). Asserts observable
behavior only: constructed field state, boundary validation errors, and
the r[bool] outcome of validate_entity.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import pytest
from flext_tests import tm

from flext_oracle_wms import FlextOracleWmsUtilitiesDiscovery
from tests import c, m

__all__ = ["TestsFlextOracleWmsSingerFlattening"]

_MAX_NAME_LENGTH = c.OracleWms.WmsEntities.MAX_ENTITY_NAME_LENGTH


class TestsFlextOracleWmsSingerFlattening:
    """Contract tests for m.OracleWms.Entity."""

    def test_minimal_entity_exposes_defaults(self) -> None:
        """Required fields are set and optionals default as documented."""
        entity = m.OracleWms.Entity(name="inventory", endpoint="/inventory")

        tm.that(entity.name, eq="inventory")
        tm.that(entity.endpoint, eq="/inventory")
        tm.that(entity.description, none=True)
        tm.that(entity.primary_key, none=True)
        tm.that(entity.replication_key, none=True)
        tm.that(entity.supports_incremental, eq=False)

    def test_full_entity_round_trips_through_model_dump(self) -> None:
        """model_dump reflects every value passed to the constructor."""
        entity = m.OracleWms.Entity(
            name="orders",
            endpoint="/orders",
            description="Order stream",
            primary_key="id",
            replication_key="updated_at",
            supports_incremental=True,
        )

        tm.that(
            entity.model_dump(),
            eq={
                "name": "orders",
                "endpoint": "/orders",
                "description": "Order stream",
                "primary_key": "id",
                "replication_key": "updated_at",
                "supports_incremental": True,
            },
        )

    @pytest.mark.parametrize(
        ("name", "endpoint"),
        [
            ("", "/valid"),
            ("valid", "no-leading-slash"),
            ("valid", ""),
        ],
    )
    def test_invalid_construction_raises_validation_error(
        self,
        name: str,
        endpoint: str,
    ) -> None:
        """Boundary violations reject construction with a ValidationError."""
        with pytest.raises(c.ValidationError):
            m.OracleWms.Entity(name=name, endpoint=endpoint)

    def test_unknown_field_is_forbidden(self) -> None:
        """extra="forbid" rejects fields outside the public schema."""
        with pytest.raises(c.ValidationError):
            m.OracleWms.Entity(
                name="inventory",
                endpoint="/inventory",
                unexpected="value",
            )

    def test_validate_entity_succeeds_for_valid_entity(self) -> None:
        """A valid entity validates to a successful r[bool] carrying True."""
        entity = m.OracleWms.Entity(name="inventory", endpoint="/inventory")

        result = FlextOracleWmsUtilitiesDiscovery.validate_wms_entity(entity)

        tm.ok(result)
        tm.that(result.unwrap(), eq=True)

    def test_validate_entity_at_max_name_length_succeeds(self) -> None:
        """A name exactly at the length ceiling still validates."""
        entity = m.OracleWms.Entity(name="x" * _MAX_NAME_LENGTH, endpoint="/e")

        result = FlextOracleWmsUtilitiesDiscovery.validate_wms_entity(entity)

        tm.ok(result)
        tm.that(result.unwrap(), eq=True)

    def test_validate_entity_rejects_overlong_name(self) -> None:
        """A name past the ceiling fails with a descriptive error."""
        entity = m.OracleWms.Entity(name="x" * (_MAX_NAME_LENGTH + 1), endpoint="/e")

        result = FlextOracleWmsUtilitiesDiscovery.validate_wms_entity(entity)

        tm.fail(result)
        tm.that(result.error, none=False)
        tm.that(result.error, has="too long")
