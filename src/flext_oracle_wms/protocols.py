"""Oracle WMS protocols for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

from flext_api import p

from flext_oracle_wms import p

if TYPE_CHECKING:
    from flext_oracle_wms import t


class FlextOracleWmsProtocols(p):
    """Oracle WMS protocols extending p.

    Extends p to inherit all foundation protocols (Result, Service, etc.)
    and adds Oracle WMS-specific protocols in the OracleWms namespace.

    Architecture:
    - EXTENDS: p (inherits Foundation, Domain, Application, etc.)
    - ADDS: Oracle WMS-specific protocols in OracleWms namespace
    - PROVIDES: Root-level alias `p` for convenient access

    Usage:
    from flext_oracle_wms import p

    # Foundation protocols (inherited)
    result: p.Result[str]
    service: p.Service[str]

    # Oracle WMS-specific protocols
    wms_service: p.OracleWms.WmsService
    """

    @runtime_checkable
    class OracleWms(Protocol):
        """Oracle WMS domain-specific protocols."""

        @runtime_checkable
        class EntityDiscoveryClient(Protocol):
            """Protocol for entity discovery client used by FlextOracleWmsEntityDiscovery."""

            def discover_entities(self) -> p.Result[t.StrSequence]:
                """Discover available entities."""
                ...

        @runtime_checkable
        class WmsService(p.Service[None], Protocol):
            """Unified WMS service protocol with operation dispatch."""

            def execute_wms_operation(
                self,
                operation: str,
                settings: t.JsonMapping,
                **params: t.Scalar,
            ) -> p.Result[t.JsonValue]:
                """Execute WMS operation with unified interface.

                Args:
                operation: Operation type (auth, discovery, inventory, etc.)
                settings: Operation configuration
                **params: Operation parameters

                Returns:
                r[t.JsonMapping]: Operation result or error

                """
                ...


p = FlextOracleWmsProtocols

__all__: list[str] = ["FlextOracleWmsProtocols", "p"]
