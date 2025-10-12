"""Oracle WMS integration protocols for FLEXT ecosystem."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from flext_core import FlextCore


class FlextOracleWmsProtocols(FlextCore.Protocols):
    """Oracle WMS integration protocols extending FlextCore.Protocols with Oracle Warehouse Management System interfaces.

    This class provides protocol definitions for Oracle WMS operations including
    WMS client operations, entity discovery, inventory management, shipping operations,
    and warehouse workflow automation.
    """

    @runtime_checkable
    class WmsClientProtocol(FlextCore.Protocols.Domain.Service, Protocol):
        """Protocol for Oracle WMS client operations."""

        def authenticate_with_wms(
            self,
            auth_config: FlextCore.Types.Dict,
        ) -> FlextCore.Result[FlextCore.Types.Dict]:
            """Authenticate with Oracle WMS system.

            Args:
                auth_config: WMS authentication configuration

            Returns:
                FlextCore.Result[FlextCore.Types.Dict]: Authentication result or error

            """
            ...

        def get_wms_entities(
            self,
            entity_type: str,
            filters: FlextCore.Types.Dict,
        ) -> FlextCore.Result[list[FlextCore.Types.Dict]]:
            """Get WMS entities with filtering.

            Args:
                entity_type: Type of WMS entity to retrieve
                filters: WMS entity filters

            Returns:
                FlextCore.Result[list[FlextCore.Types.Dict]]: WMS entities or error

            """

        def execute_wms_operation(
            self,
            operation: str,
            parameters: FlextCore.Types.Dict,
        ) -> FlextCore.Result[FlextCore.Types.Dict]:
            """Execute WMS operation.

            Args:
                operation: WMS operation to execute
                parameters: Operation parameters

            Returns:
                FlextCore.Result[FlextCore.Types.Dict]: Operation result or error

            """

        def validate_wms_connectivity(
            self,
            connection_config: FlextCore.Types.Dict,
        ) -> FlextCore.Result[FlextCore.Types.Dict]:
            """Validate WMS connectivity.

            Args:
                connection_config: WMS connection configuration

            Returns:
                FlextCore.Result[FlextCore.Types.Dict]: Connectivity status or error

            """

    @runtime_checkable
    class EntityDiscoveryProtocol(FlextCore.Protocols.Domain.Service, Protocol):
        """Protocol for Oracle WMS entity discovery operations."""

        def discover_wms_entities(
            self,
            discovery_config: FlextCore.Types.Dict,
        ) -> FlextCore.Result[list[FlextCore.Types.Dict]]:
            """Discover WMS entities with schema information.

            Args:
                discovery_config: Entity discovery configuration

            Returns:
                FlextCore.Result[list[FlextCore.Types.Dict]]: Discovered entities or error

            """

        def process_dynamic_schema(
            self,
            entity_name: str,
            schema_config: FlextCore.Types.Dict,
        ) -> FlextCore.Result[FlextCore.Types.Dict]:
            """Process dynamic WMS entity schema.

            Args:
                entity_name: Name of WMS entity
                schema_config: Schema processing configuration

            Returns:
                FlextCore.Result[FlextCore.Types.Dict]: Processed schema or error

            """

        def cache_entity_metadata(
            self,
            entity_metadata: FlextCore.Types.Dict,
            cache_config: FlextCore.Types.Dict,
        ) -> FlextCore.Result[FlextCore.Types.Dict]:
            """Cache WMS entity metadata.

            Args:
                entity_metadata: Entity metadata to cache
                cache_config: Cache configuration

            Returns:
                FlextCore.Result[FlextCore.Types.Dict]: Cache operation result or error

            """

        def validate_entity_schema(
            self,
            entity_schema: FlextCore.Types.Dict,
            validation_rules: FlextCore.Types.Dict,
        ) -> FlextCore.Result[FlextCore.Types.Dict]:
            """Validate WMS entity schema.

            Args:
                entity_schema: Entity schema to validate
                validation_rules: Schema validation rules

            Returns:
                FlextCore.Result[FlextCore.Types.Dict]: Validation result or error

            """

    @runtime_checkable
    class InventoryManagementProtocol(FlextCore.Protocols.Domain.Service, Protocol):
        """Protocol for Oracle WMS inventory management operations."""

        def process_inventory_transaction(
            self,
            transaction_data: FlextCore.Types.Dict,
            processing_config: FlextCore.Types.Dict,
        ) -> FlextCore.Result[FlextCore.Types.Dict]:
            """Process inventory transaction in WMS.

            Args:
                transaction_data: Inventory transaction data
                processing_config: Transaction processing configuration

            Returns:
                FlextCore.Result[FlextCore.Types.Dict]: Transaction result or error

            """

        def check_inventory_availability(
            self,
            item_id: str,
            location_id: str,
            quantity_required: int,
        ) -> FlextCore.Result[FlextCore.Types.Dict]:
            """Check inventory availability in WMS.

            Args:
                item_id: Item identifier
                location_id: Location identifier
                quantity_required: Required quantity

            Returns:
                FlextCore.Result[FlextCore.Types.Dict]: Availability status or error

            """

        def update_inventory_levels(
            self,
            inventory_updates: list[FlextCore.Types.Dict],
            update_config: FlextCore.Types.Dict,
        ) -> FlextCore.Result[FlextCore.Types.Dict]:
            """Update inventory levels in WMS.

            Args:
                inventory_updates: Inventory level updates
                update_config: Update configuration

            Returns:
                FlextCore.Result[FlextCore.Types.Dict]: Update result or error

            """

        def execute_cycle_count(
            self,
            count_parameters: FlextCore.Types.Dict,
            execution_config: FlextCore.Types.Dict,
        ) -> FlextCore.Result[FlextCore.Types.Dict]:
            """Execute cycle count in WMS.

            Args:
                count_parameters: Cycle count parameters
                execution_config: Execution configuration

            Returns:
                FlextCore.Result[FlextCore.Types.Dict]: Cycle count result or error

            """

    @runtime_checkable
    class ShippingOperationsProtocol(FlextCore.Protocols.Domain.Service, Protocol):
        """Protocol for Oracle WMS shipping operations."""

        def process_outbound_shipment(
            self,
            shipment_data: FlextCore.Types.Dict,
            processing_config: FlextCore.Types.Dict,
        ) -> FlextCore.Result[FlextCore.Types.Dict]:
            """Process outbound shipment in WMS.

            Args:
                shipment_data: Shipment data
                processing_config: Shipment processing configuration

            Returns:
                FlextCore.Result[FlextCore.Types.Dict]: Shipment processing result or error

            """

        def create_picking_wave(
            self,
            wave_parameters: FlextCore.Types.Dict,
            creation_config: FlextCore.Types.Dict,
        ) -> FlextCore.Result[FlextCore.Types.Dict]:
            """Create picking wave in WMS.

            Args:
                wave_parameters: Picking wave parameters
                creation_config: Wave creation configuration

            Returns:
                FlextCore.Result[FlextCore.Types.Dict]: Wave creation result or error

            """

        def execute_picking_operations(
            self,
            picking_instructions: list[FlextCore.Types.Dict],
            execution_config: FlextCore.Types.Dict,
        ) -> FlextCore.Result[FlextCore.Types.Dict]:
            """Execute picking operations in WMS.

            Args:
                picking_instructions: Picking instructions
                execution_config: Picking execution configuration

            Returns:
                FlextCore.Result[FlextCore.Types.Dict]: Picking result or error

            """

        def confirm_shipment_dispatch(
            self,
            shipment_id: str,
            dispatch_details: FlextCore.Types.Dict,
        ) -> FlextCore.Result[FlextCore.Types.Dict]:
            """Confirm shipment dispatch in WMS.

            Args:
                shipment_id: Shipment identifier
                dispatch_details: Dispatch confirmation details

            Returns:
                FlextCore.Result[FlextCore.Types.Dict]: Dispatch confirmation or error

            """

    @runtime_checkable
    class WarehouseOperationsProtocol(FlextCore.Protocols.Domain.Service, Protocol):
        """Protocol for Oracle WMS warehouse operations."""

        def process_inbound_receipt(
            self,
            receipt_data: FlextCore.Types.Dict,
            processing_config: FlextCore.Types.Dict,
        ) -> FlextCore.Result[FlextCore.Types.Dict]:
            """Process inbound receipt in WMS.

            Args:
                receipt_data: Receipt data
                processing_config: Receipt processing configuration

            Returns:
                FlextCore.Result[FlextCore.Types.Dict]: Receipt processing result or error

            """

        def execute_putaway_operations(
            self,
            putaway_instructions: list[FlextCore.Types.Dict],
            execution_config: FlextCore.Types.Dict,
        ) -> FlextCore.Result[FlextCore.Types.Dict]:
            """Execute putaway operations in WMS.

            Args:
                putaway_instructions: Putaway instructions
                execution_config: Putaway execution configuration

            Returns:
                FlextCore.Result[FlextCore.Types.Dict]: Putaway result or error

            """

        def manage_warehouse_tasks(
            self,
            task_parameters: FlextCore.Types.Dict,
            management_config: FlextCore.Types.Dict,
        ) -> FlextCore.Result[FlextCore.Types.Dict]:
            """Manage warehouse tasks in WMS.

            Args:
                task_parameters: Task management parameters
                management_config: Task management configuration

            Returns:
                FlextCore.Result[FlextCore.Types.Dict]: Task management result or error

            """

        def optimize_warehouse_layout(
            self,
            optimization_parameters: FlextCore.Types.Dict,
            layout_config: FlextCore.Types.Dict,
        ) -> FlextCore.Result[FlextCore.Types.Dict]:
            """Optimize warehouse layout in WMS.

            Args:
                optimization_parameters: Layout optimization parameters
                layout_config: Layout configuration

            Returns:
                FlextCore.Result[FlextCore.Types.Dict]: Optimization result or error

            """

    @runtime_checkable
    class DataProcessingProtocol(FlextCore.Protocols.Domain.Service, Protocol):
        """Protocol for Oracle WMS data processing operations."""

        def filter_wms_data(
            self,
            data: list[FlextCore.Types.Dict],
            filter_config: FlextCore.Types.Dict,
        ) -> FlextCore.Result[list[FlextCore.Types.Dict]]:
            """Filter WMS data based on criteria.

            Args:
                data: WMS data to filter
                filter_config: Filter configuration

            Returns:
                FlextCore.Result[list[FlextCore.Types.Dict]]: Filtered data or error

            """

        def flatten_wms_data(
            self,
            hierarchical_data: FlextCore.Types.Dict,
            flattening_config: FlextCore.Types.Dict,
        ) -> FlextCore.Result[FlextCore.Types.Dict]:
            """Flatten hierarchical WMS data.

            Args:
                hierarchical_data: Hierarchical WMS data
                flattening_config: Flattening configuration

            Returns:
                FlextCore.Result[FlextCore.Types.Dict]: Flattened data or error

            """

        def transform_wms_data(
            self,
            source_data: FlextCore.Types.Dict,
            transformation_config: FlextCore.Types.Dict,
        ) -> FlextCore.Result[FlextCore.Types.Dict]:
            """Transform WMS data format.

            Args:
                source_data: Source WMS data
                transformation_config: Transformation configuration

            Returns:
                FlextCore.Result[FlextCore.Types.Dict]: Transformed data or error

            """

        def validate_wms_data_quality(
            self,
            data: FlextCore.Types.Dict,
            quality_rules: FlextCore.Types.Dict,
        ) -> FlextCore.Result[FlextCore.Types.Dict]:
            """Validate WMS data quality.

            Args:
                data: WMS data to validate
                quality_rules: Data quality rules

            Returns:
                FlextCore.Result[FlextCore.Types.Dict]: Quality validation result or error

            """

    @runtime_checkable
    class AuthenticationProtocol(FlextCore.Protocols.Domain.Service, Protocol):
        """Protocol for Oracle WMS authentication operations."""

        def authenticate_oauth2(
            self,
            oauth2_config: FlextCore.Types.Dict,
        ) -> FlextCore.Result[FlextCore.Types.Dict]:
            """Authenticate using OAuth2 with WMS.

            Args:
                oauth2_config: OAuth2 authentication configuration

            Returns:
                FlextCore.Result[FlextCore.Types.Dict]: Authentication tokens or error

            """

        def refresh_authentication_token(
            self,
            token_config: FlextCore.Types.Dict,
        ) -> FlextCore.Result[FlextCore.Types.Dict]:
            """Refresh WMS authentication token.

            Args:
                token_config: Token refresh configuration

            Returns:
                FlextCore.Result[FlextCore.Types.Dict]: Refreshed token or error

            """

        def validate_session_status(
            self,
            session_config: FlextCore.Types.Dict,
        ) -> FlextCore.Result[FlextCore.Types.Dict]:
            """Validate WMS session status.

            Args:
                session_config: Session validation configuration

            Returns:
                FlextCore.Result[FlextCore.Types.Dict]: Session status or error

            """

        def manage_authentication_plugins(
            self,
            plugin_config: FlextCore.Types.Dict,
        ) -> FlextCore.Result[FlextCore.Types.Dict]:
            """Manage WMS authentication plugins.

            Args:
                plugin_config: Plugin management configuration

            Returns:
                FlextCore.Result[FlextCore.Types.Dict]: Plugin management result or error

            """

    @runtime_checkable
    class PerformanceProtocol(FlextCore.Protocols.Domain.Service, Protocol):
        """Protocol for Oracle WMS performance optimization operations."""

        def optimize_wms_operations(
            self, performance_config: FlextCore.Types.Dict
        ) -> FlextCore.Result[FlextCore.Types.Dict]:
            """Optimize WMS operations performance.

            Args:
                performance_config: Performance optimization configuration

            Returns:
                FlextCore.Result[FlextCore.Types.Dict]: Optimization results or error

            """

        def configure_connection_pooling(
            self, pool_config: FlextCore.Types.Dict
        ) -> FlextCore.Result[FlextCore.Types.Dict]:
            """Configure connection pooling for WMS operations.

            Args:
                pool_config: Connection pooling configuration

            Returns:
                FlextCore.Result[FlextCore.Types.Dict]: Pool configuration result or error

            """

        def monitor_wms_performance(
            self, performance_metrics: FlextCore.Types.Dict
        ) -> FlextCore.Result[FlextCore.Types.Dict]:
            """Monitor WMS performance metrics.

            Args:
                performance_metrics: Performance monitoring data

            Returns:
                FlextCore.Result[FlextCore.Types.Dict]: Performance analysis or error

            """

        def optimize_data_caching(
            self, cache_config: FlextCore.Types.Dict
        ) -> FlextCore.Result[FlextCore.Types.Dict]:
            """Optimize WMS data caching.

            Args:
                cache_config: Cache optimization configuration

            Returns:
                FlextCore.Result[FlextCore.Types.Dict]: Cache optimization results or error

            """

    @runtime_checkable
    class MonitoringProtocol(FlextCore.Protocols.Domain.Service, Protocol):
        """Protocol for Oracle WMS monitoring operations."""

        def track_wms_metrics(
            self, wms_id: str, metrics: FlextCore.Types.Dict
        ) -> FlextCore.Result[bool]:
            """Track WMS operation metrics.

            Args:
                wms_id: WMS operation identifier
                metrics: WMS metrics data

            Returns:
                FlextCore.Result[bool]: Metric tracking success status

            """

        def monitor_wms_health(
            self, health_config: FlextCore.Types.Dict
        ) -> FlextCore.Result[FlextCore.Types.Dict]:
            """Monitor WMS system health status.

            Args:
                health_config: Health monitoring configuration

            Returns:
                FlextCore.Result[FlextCore.Types.Dict]: Health status or error

            """

        def get_operation_status(
            self, operation_id: str
        ) -> FlextCore.Result[FlextCore.Types.Dict]:
            """Get WMS operation status.

            Args:
                operation_id: Operation identifier

            Returns:
                FlextCore.Result[FlextCore.Types.Dict]: Operation status or error

            """

        def create_monitoring_dashboard(
            self, dashboard_config: FlextCore.Types.Dict
        ) -> FlextCore.Result[FlextCore.Types.Dict]:
            """Create monitoring dashboard for WMS operations.

            Args:
                dashboard_config: Dashboard configuration

            Returns:
                FlextCore.Result[FlextCore.Types.Dict]: Dashboard creation result or error

            """

    # Convenience aliases for easier downstream usage
    OracleWmsClientProtocol = WmsClientProtocol
    OracleWmsEntityDiscoveryProtocol = EntityDiscoveryProtocol
    OracleWmsInventoryManagementProtocol = InventoryManagementProtocol
    OracleWmsShippingOperationsProtocol = ShippingOperationsProtocol
    OracleWmsWarehouseOperationsProtocol = WarehouseOperationsProtocol
    OracleWmsDataProcessingProtocol = DataProcessingProtocol
    OracleWmsAuthenticationProtocol = AuthenticationProtocol
    OracleWmsPerformanceProtocol = PerformanceProtocol
    OracleWmsMonitoringProtocol = MonitoringProtocol


__all__ = [
    "FlextOracleWmsProtocols",
]
