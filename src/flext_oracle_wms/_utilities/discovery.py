"""Oracle WMS Entity Discovery utilities.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_oracle_wms import c, m, p, r


class FlextOracleWmsUtilitiesDiscovery:
    """Discovery utilities for Oracle WMS -- u.OracleWms.Discovery.*."""

    @staticmethod
    def validate_wms_entity(entity: m.OracleWms.Entity) -> p.Result[bool]:
        """Validate an Oracle WMS entity definition against domain rules."""
        # NOTE (multi-agent): U17 — entity business validation lives in u.*, not on
        # the model (declaration layer). Moved verbatim from m.OracleWms.Entity.
        if not entity.name:
            return r[bool].fail("Entity name is required")
        if len(entity.name) > c.OracleWms.WmsEntities.MAX_ENTITY_NAME_LENGTH:
            return r[bool].fail("Entity name is too long")
        if not entity.endpoint:
            return r[bool].fail("Entity endpoint is required")
        return r[bool].ok(True)


__all__: list[str] = ["FlextOracleWmsUtilitiesDiscovery"]
