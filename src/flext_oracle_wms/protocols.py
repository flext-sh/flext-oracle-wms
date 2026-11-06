# AUTO-GENERATED FILE — Regenerate with: make gen
"""Oracle WMS protocols for FLEXT ecosystem.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_api import p

from flext_oracle_wms._protocols import (
    FlextOracleWmsProtocolsConfig,
    FlextOracleWmsProtocolsDomain,
)


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

    class OracleWms(FlextOracleWmsProtocolsConfig, FlextOracleWmsProtocolsDomain):
        """Oracle WMS domain-specific protocols."""


p = FlextOracleWmsProtocols
__all__: list[str] = ["FlextOracleWmsProtocols", "p"]
