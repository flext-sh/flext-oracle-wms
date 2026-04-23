"""Oracle WMS Entity Discovery utilities.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Sequence,
)

from flext_oracle_wms import FlextOracleWmsProtocols as p, c, r, t


class FlextOracleWmsUtilitiesDiscovery:
    """Discovery utilities for Oracle WMS -- u.OracleWms.Discovery.*."""

    DISCOVERY_SUCCESS = "discovery_success"
    DISCOVERY_FAILURE = "discovery_failure"

    class EntityDiscovery:
        """Discovery service for Oracle WMS entities."""

        def __init__(self, client: p.OracleWms.EntityDiscoveryClient) -> None:
            """Initialize discovery service with a client."""
            self.client = client

        @staticmethod
        def _to_discovered_entity(entity_name: str) -> t.JsonMapping:
            return {
                "name": entity_name,
                "path": f"/entities/{entity_name}",
                "strategy": c.OracleWms.EndpointDiscoveryStrategy.API_BASED,
            }

        def discover_entities(self) -> p.Result[Sequence[t.JsonMapping]]:
            """Discover entities from Oracle WMS API."""
            entities_result = self.client.discover_entities()
            if entities_result.failure:
                return r[Sequence[t.JsonMapping]].fail(entities_result.error)
            discovered = [
                self._to_discovered_entity(entity_name)
                for entity_name in entities_result.value
                if entity_name
            ]
            return r[Sequence[t.JsonMapping]].ok(discovered)


__all__: list[str] = [
    "FlextOracleWmsUtilitiesDiscovery",
]
