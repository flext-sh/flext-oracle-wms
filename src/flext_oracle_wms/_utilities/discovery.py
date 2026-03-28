"""Oracle WMS Entity Discovery utilities.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from flext_core import r

from flext_oracle_wms.constants import FlextOracleWmsConstants as c
from flext_oracle_wms.protocols import FlextOracleWmsProtocols as p
from flext_oracle_wms.typings import FlextOracleWmsTypes as t

DISCOVERY_SUCCESS = "discovery_success"
DISCOVERY_FAILURE = "discovery_failure"


class FlextOracleWmsUtilitiesDiscovery:
    """Discovery utilities for Oracle WMS -- u.OracleWms.Discovery.*."""

    DISCOVERY_SUCCESS = DISCOVERY_SUCCESS
    DISCOVERY_FAILURE = DISCOVERY_FAILURE

    class EntityDiscovery:
        """Discovery service for Oracle WMS entities."""

        def __init__(self, client: p.OracleWms.EntityDiscoveryClient) -> None:
            """Initialize discovery service with a client."""
            self.client = client

        @staticmethod
        def _to_discovered_entity(entity_name: str) -> Mapping[str, t.ContainerValue]:
            return {
                "name": entity_name,
                "path": f"/entities/{entity_name}",
                "strategy": c.OracleWms.EndpointDiscoveryStrategy.API_BASED,
            }

        def discover_entities(self) -> r[Sequence[Mapping[str, t.ContainerValue]]]:
            """Discover entities from Oracle WMS API."""
            entities_result = self.client.discover_entities()
            if entities_result.is_failure:
                return r[Sequence[t.ContainerValueMapping]].fail(entities_result.error)
            discovered = [
                self._to_discovered_entity(entity_name)
                for entity_name in entities_result.value
                if entity_name
            ]
            return r[Sequence[t.ContainerValueMapping]].ok(discovered)


__all__ = ["DISCOVERY_FAILURE", "DISCOVERY_SUCCESS", "FlextOracleWmsUtilitiesDiscovery"]
