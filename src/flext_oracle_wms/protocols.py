# AUTO-GENERATED FILE — Regenerate with: make gen
"""Oracle WMS protocols for FLEXT ecosystem.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from flext_api import FlextApiProtocols

from flext_oracle_wms._protocols import FlextOracleWmsProtocolsConfig, domain


class FlextOracleWmsProtocols(FlextApiProtocols):
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

        # Validated ``config`` domain surface, aliased as a PEP 695
        # type so the structural protocol stays usable in type expressions.
        Config = FlextOracleWmsProtocolsConfig.Config

        EntityDiscoveryClient = (
            domain.FlextOracleWmsProtocolsDomain.EntityDiscoveryClient
        )
        WmsService = domain.FlextOracleWmsProtocolsDomain.WmsService


p = FlextOracleWmsProtocols

__all__: list[str] = ["FlextOracleWmsProtocols", "p"]
