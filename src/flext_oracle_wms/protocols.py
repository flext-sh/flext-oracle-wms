"""FLEXT Oracle WMS Protocols - composition patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from flext_core import FlextTypes as t
from flext_core.protocols import FlextProtocols

p = FlextProtocols


class FlextOracleWmsProtocols(p):
    """Oracle WMS protocols with composition.

    Uses Python 3.13+ syntax, reduces declarations through patterns.
    One class per module following SOLID principles.
    """

    # Consolidated protocol using generic operation pattern
    class OracleWms:
        """OracleWms domain namespace."""

        @runtime_checkable
        class WmsServiceProtocol(p.Service, Protocol):
            """Unified WMS service protocol with operation dispatch."""

            def execute_wms_operation(
                self,
                operation: str,
                config: dict[str, t.GeneralValueType],
                **params: object,
            ) -> FlextProtocols.Result[dict[str, t.GeneralValueType]]:
                """Execute WMS operation with unified interface.

                Args:
                operation: Operation type (auth, discovery, inventory, etc.)
                config: Operation configuration
                **params: Operation parameters

                Returns:
                FlextResult[dict[str, t.GeneralValueType]]: Operation result or error

                """
                ...

        # Legacy aliases for backward compatibility during transition
        WmsClientProtocol = WmsServiceProtocol
        EntityDiscoveryProtocol = WmsServiceProtocol
        InventoryManagementProtocol = WmsServiceProtocol
        ShippingOperationsProtocol = WmsServiceProtocol
        WarehouseOperationsProtocol = WmsServiceProtocol
        DataProcessingProtocol = WmsServiceProtocol
        AuthenticationProtocol = WmsServiceProtocol
        PerformanceProtocol = WmsServiceProtocol
        MonitoringProtocol = WmsServiceProtocol

        # Convenience aliases
        OracleWmsClientProtocol = WmsServiceProtocol
        OracleWmsEntityDiscoveryProtocol = WmsServiceProtocol
        OracleWmsInventoryManagementProtocol = WmsServiceProtocol
        OracleWmsShippingOperationsProtocol = WmsServiceProtocol
        OracleWmsWarehouseOperationsProtocol = WmsServiceProtocol
        OracleWmsDataProcessingProtocol = WmsServiceProtocol
        OracleWmsAuthenticationProtocol = WmsServiceProtocol
        OracleWmsPerformanceProtocol = WmsServiceProtocol
        OracleWmsMonitoringProtocol = WmsServiceProtocol


# Runtime alias for simplified usage
p = FlextOracleWmsProtocols

__all__ = [
    "FlextOracleWmsProtocols",
    "p",
]
