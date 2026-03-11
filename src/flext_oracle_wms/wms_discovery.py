"""FLEXT Oracle WMS Discovery module.

Provides discovery classes for Oracle WMS entities.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Protocol

from flext_core import r, t

from flext_oracle_wms.constants import FlextOracleWmsConstants as c


class _EntityDiscoveryClient(Protocol):
    def discover_entities(self) -> r[list[str]]: ...


class FlextOracleWmsEntityDiscovery:
    """Discovery service for Oracle WMS entities."""

    def __init__(self, client: _EntityDiscoveryClient) -> None:
        """Initialize discovery service with a client."""
        self.client = client

    @staticmethod
    def _to_discovered_entity(entity_name: str) -> Mapping[str, t.ContainerValue]:
        return {
            "name": entity_name,
            "path": f"/entities/{entity_name}",
            "strategy": c.EndpointDiscoveryStrategy.API_BASED,
        }

    def discover_entities(self) -> r[list[Mapping[str, t.ContainerValue]]]:
        """Discover entities from Oracle WMS API."""
        entities_result = self.client.discover_entities()
        if entities_result.is_failure:
            return r[list[Mapping[str, t.ContainerValue]]].fail(entities_result.error)
        discovered = [
            self._to_discovered_entity(entity_name)
            for entity_name in entities_result.value
            if entity_name
        ]
        return r[list[Mapping[str, t.ContainerValue]]].ok(discovered)


DISCOVERY_SUCCESS = "discovery_success"
DISCOVERY_FAILURE = "discovery_failure"
__all__ = ["DISCOVERY_FAILURE", "DISCOVERY_SUCCESS", "FlextOracleWmsEntityDiscovery"]
