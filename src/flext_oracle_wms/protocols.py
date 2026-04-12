"""Oracle WMS protocols for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from flext_core import FlextProtocols
from flext_oracle_wms import t


class FlextOracleWmsProtocols(FlextProtocols):
    """Oracle WMS protocols extending FlextProtocols.

    Extends FlextProtocols to inherit all foundation protocols (Result, Service, etc.)
    and adds Oracle WMS-specific protocols in the OracleWms namespace.

    Architecture:
    - EXTENDS: FlextProtocols (inherits Foundation, Domain, Application, etc.)
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

            def discover_entities(self) -> FlextProtocols.Result[t.StrSequence]:
                """Discover available entities."""
                ...

        @runtime_checkable
        class WmsService(FlextProtocols.Service[None], Protocol):
            """Unified WMS service protocol with operation dispatch."""

            def execute_wms_operation(
                self,
                operation: str,
                settings: t.ContainerValueMapping,
                **params: t.Scalar,
            ) -> FlextProtocols.Result[t.ContainerValue]:
                """Execute WMS operation with unified interface.

                Args:
                operation: Operation type (auth, discovery, inventory, etc.)
                settings: Operation configuration
                **params: Operation parameters

                Returns:
                r[t.ContainerValueMapping]: Operation result or error

                """
                ...


__all__: list[str] = ["FlextOracleWmsProtocols", "p"]

p = FlextOracleWmsProtocols
