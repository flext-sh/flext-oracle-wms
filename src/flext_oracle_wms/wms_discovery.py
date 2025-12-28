"""FLEXT Oracle WMS Discovery module.

Provides discovery classes for Oracle WMS entities.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import ClassVar

from flext_core import FlextResult, FlextTypes as t

from flext_oracle_wms.constants import c
from flext_oracle_wms.http_client import FlextHttpClient

# Alias for backward compatibility - EndpointDiscoveryStrategy is now in constants.py
EndpointDiscoveryStrategy = c.EndpointDiscoveryStrategy


# Simple placeholders for missing classes
class CacheValue:
    """Cache value placeholder."""


class DiscoveryContext:
    """Discovery context placeholder."""


class EntityResponseParser:
    """Entity response parser placeholder."""


class FlextOracleWmsDefaults:
    """Defaults placeholder."""

    CACHE_TTL: ClassVar[int] = 3600


class FlextOracleWmsEntityDiscovery:
    """Entity discovery placeholder."""

    def __init__(self, client: FlextHttpClient) -> None:
        """Initialize entity discovery with HTTP client."""
        self.client = client

    def discover_entities(self) -> FlextResult[list[dict[str, t.GeneralValueType]]]:
        """Discover entities placeholder."""
        return FlextResult.ok([])


# Constants
DISCOVERY_SUCCESS = "discovery_success"
DISCOVERY_FAILURE = "discovery_failure"


__all__ = [
    "DISCOVERY_FAILURE",
    "DISCOVERY_SUCCESS",
    "CacheValue",
    "DiscoveryContext",
    "EndpointDiscoveryStrategy",
    "EntityResponseParser",
    "FlextOracleWmsDefaults",
    "FlextOracleWmsEntityDiscovery",
]
