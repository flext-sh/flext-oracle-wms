"""FLEXT Oracle WMS API module.

Provides the main FlextOracleWmsApi class following FLEXT standards with proper inheritance levels.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import (
    FlextBus,
    FlextContainer,
    FlextContext,
    FlextDispatcher,
    FlextHandlers,
    FlextLogger,
    FlextModels,
    FlextProcessors,
    FlextRegistry,
    FlextService,
)

from flext_oracle_wms.config import FlextOracleWmsConfig
from flext_oracle_wms.wms_client import FlextOracleWmsClient

# from flext_oracle_wms.wms_discovery import FlextOracleWmsEntityDiscovery
# from flext_oracle_wms.wms_operations import FlextOracleWmsUnifiedOperations


class FlextOracleWmsApi(FlextService[FlextOracleWmsConfig]):
    """Thin facade for Oracle WMS operations with complete FLEXT integration.

    Integrates:
    - FlextBus: Event emission for WMS operations
    - FlextContainer: Dependency injection for WMS services
    - FlextContext: Operation context management
    - FlextCqrs: CQRS pattern for WMS commands/queries
    - FlextDispatcher: Message routing for WMS operations
    - FlextProcessors: Processing utilities for WMS data
    - FlextRegistry: Component registration for WMS plugins
    - FlextLogger: Structured logging for WMS operations

    This facade provides easy access to all Oracle WMS functionality
    while maintaining clean separation between business logic and infrastructure.
    """

    def __init__(
        self,
        config: FlextOracleWmsConfig | None = None,
    ) -> None:
        """Initialize Oracle WMS facade with FLEXT integration.

        Args:
            config: Oracle WMS configuration. Uses default if None.

        """
        super().__init__()

        # Configuration
        self._config = config or FlextOracleWmsConfig()

        # Complete FLEXT ecosystem integration
        self._container = FlextContainer.get_global()
        self._context = FlextContext()
        self._bus = FlextBus()
        self._dispatcher = FlextDispatcher()
        # Create handler config
        handler_config = FlextModels.CqrsConfig.Handler(
            handler_id="flext_oracle_wms_handler",
            handler_name="FlextOracleWmsHandler",
            handler_type="command",
        )
        self._handlers = FlextHandlers(config=handler_config)
        self._processors = FlextProcessors()
        self._registry = FlextRegistry(dispatcher=self._dispatcher)
        self.logger = FlextLogger(__name__)

        # Domain services (delegate all business logic here)
        self._client = FlextOracleWmsClient(self._config)
        # self._discovery = FlextOracleWmsEntityDiscovery(self._client)
        # self._operations = FlextOracleWmsUnifiedOperations(self._client)

    # Delegate to domain services - NO business logic in facade

    # async def discover_entities(
    #     self, entity_type: str, **kwargs: object
    # ) -> FlextResult[list[FlextOracleWmsEntity]]:
    #     """Discover Oracle WMS entities.

    #     Args:
    #         entity_type: Type of entities to discover
    #         **kwargs: Additional discovery parameters

    #     Returns:
    #         Result containing discovered entities

    #     """
    #     return await self._discovery.discover_entities(entity_type, **kwargs)

    # async def get_inventory_data(
    #     self, entity_name: str, **kwargs: object
    # ) -> FlextResult[list[FlextOracleWmsEntity]]:
    #     """Get inventory data from Oracle WMS.

    #     Args:
    #         entity_name: Name of inventory entity
    #         **kwargs: Additional query parameters

    #     Returns:
    #         Result containing inventory data

    #     """
    #     return await self._operations.get_inventory_data(entity_name, **kwargs)

    # async def process_shipment(
    #     self, shipment_id: str, **kwargs: object
    # ) -> FlextResult[FlextTypes.Dict]:
    #     """Process shipment in Oracle WMS.

    #     Args:
    #         shipment_id: Shipment identifier
    #         **kwargs: Additional processing parameters

    #     Returns:
    #         Result containing processing outcome

    #     """
    #     return await self._operations.process_shipment(shipment_id, **kwargs)

    # async def execute_picking_wave(
    #     self, wave_id: str, **kwargs: object
    # ) -> FlextResult[FlextTypes.Dict]:
    #     """Execute picking wave in Oracle WMS.

    #     Args:
    #         wave_id: Picking wave identifier
    #         **kwargs: Additional execution parameters

    #     Returns:
    #         Result containing execution outcome

    #     """
    #     return await self._operations.execute_picking_wave(wave_id, **kwargs)

    # Additional facade methods can be added as the domain services expand
    # All business logic stays in the specialized service classes


__all__ = ["FlextOracleWmsApi"]
