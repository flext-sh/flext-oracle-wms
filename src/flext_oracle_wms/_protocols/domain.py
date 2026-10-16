"""Oracle WMS discovery and service protocol contracts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

from flext_api import FlextApiProtocols

if TYPE_CHECKING:
    from flext_oracle_wms import t


class FlextOracleWmsProtocolsDomain:
    """Oracle WMS domain protocol contracts composed into ``p.OracleWms``."""

    @runtime_checkable
    class EntityDiscoveryClient(Protocol):
        """Protocol for the entity discovery client used by the discovery."""

        def discover_entities(self) -> FlextApiProtocols.Result[t.StrSequence]:
            """Discover available entities.

            Returns:
                Result wrapping the discovered entity names.

            """
            ...

    @runtime_checkable
    class WmsService(FlextApiProtocols.Service[None], Protocol):
        """Unified WMS service protocol with operation dispatch."""

        def execute_wms_operation(
            self,
            operation: str,
            settings: t.JsonMapping,
            **params: t.Scalar,
        ) -> FlextApiProtocols.Result[t.JsonValue]:
            """Execute WMS operation with unified interface.

            Args:
                operation: Operation type (auth, discovery, inventory,
                    and so on).
                settings: Operation configuration.
                **params: Operation parameters.

            Returns:
                Result wrapping the operation output or an error.

            """
            ...


__all__: list[str] = [
    "EntityDiscoveryClient",
    "FlextOracleWmsProtocolsDomain",
    "WmsService",
]
