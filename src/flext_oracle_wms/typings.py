"""FLEXT Oracle WMS Types - Domain-specific Oracle WMS type definitions.

This module provides Oracle WMS-specific type definitions extending FlextCore.Types.
Follows FLEXT standards:
- Domain-specific complex types only
- No simple aliases to primitive types
- Python 3.13+ syntax
- Extends FlextCore.Types properly

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import Literal

from flext_core import FlextCore

# =============================================================================
# ORACLE WMS-SPECIFIC TYPE VARIABLES - Domain-specific TypeVars for Oracle WMS operations
# =============================================================================


# Oracle WMS domain TypeVars
class FlextOracleWmsTypes(FlextCore.Types):
    """Oracle WMS-specific type definitions extending FlextCore.Types.

    Domain-specific type system for Oracle Warehouse Management System operations.
    Contains ONLY complex Oracle WMS-specific types, no simple aliases.
    Uses Python 3.13+ type syntax and patterns.
    """

    # =========================================================================
    # WMS CONNECTION TYPES - Oracle WMS system connection configuration
    # =========================================================================

    class Connection:
        """Oracle WMS connection complex types."""

        type WmsConnectionConfig = dict[str, str | int | bool | FlextCore.Types.Dict]
        type DatabaseConnection = dict[
            str, FlextOracleWmsTypes.Core.ConfigValue | FlextCore.Types.Dict
        ]
        type ApiConnection = dict[
            str, str | dict[str, FlextOracleWmsTypes.Core.JsonValue]
        ]
        type AuthenticationConfig = dict[str, str | FlextCore.Types.Dict]
        type SessionConfig = dict[str, int | bool | str | FlextCore.Types.Dict]
        type SecurityConfig = dict[
            str, bool | str | dict[str, FlextOracleWmsTypes.Core.ConfigValue]
        ]

    # =========================================================================
    # WAREHOUSE TYPES - Warehouse structure and configuration types
    # =========================================================================

    class Warehouse:
        """Oracle WMS warehouse complex types."""

        type WarehouseConfiguration = dict[
            str, FlextOracleWmsTypes.Core.JsonValue | FlextCore.Types.Dict
        ]
        type LocationDefinition = dict[
            str, str | dict[str, FlextOracleWmsTypes.Core.JsonValue]
        ]
        type ZoneConfiguration = dict[
            str, str | FlextCore.Types.StringList | FlextCore.Types.Dict
        ]
        type AreaDefinition = dict[
            str, str | int | dict[str, FlextOracleWmsTypes.Core.JsonValue]
        ]
        type CapacityConfiguration = dict[str, int | float | FlextCore.Types.Dict]
        type LayoutConfiguration = dict[
            str, FlextOracleWmsTypes.Core.JsonValue | FlextCore.Types.Dict
        ]

    # =========================================================================
    # INVENTORY TYPES - Inventory management and tracking types
    # =========================================================================

    class Inventory:
        """Oracle WMS inventory complex types."""

        type InventoryItem = dict[
            str, FlextOracleWmsTypes.Core.JsonValue | FlextCore.Types.Dict
        ]
        type StockLevel = dict[str, int | float | str | FlextCore.Types.Dict]
        type MovementRecord = dict[
            str, str | int | dict[str, FlextOracleWmsTypes.Core.JsonValue]
        ]
        type AllocationRule = dict[str, str | bool | FlextCore.Types.Dict]
        type ReservationConfig = dict[
            str, FlextOracleWmsTypes.Core.JsonValue | FlextCore.Types.Dict
        ]
        type CycleCountConfig = dict[str, int | bool | str | FlextCore.Types.Dict]

    # =========================================================================
    # TASK MANAGEMENT TYPES - WMS task execution and workflow types
    # =========================================================================

    class TaskManagement:
        """Oracle WMS task management complex types."""

        type TaskDefinition = dict[
            str, str | dict[str, FlextOracleWmsTypes.Core.JsonValue]
        ]
        type TaskExecution = dict[str, str | bool | int | FlextCore.Types.Dict]
        type WorkOrder = dict[
            str, FlextOracleWmsTypes.Core.JsonValue | FlextCore.Types.Dict
        ]
        type TaskPriority = dict[str, int | str | FlextCore.Types.Dict]
        type ResourceAllocation = dict[
            str, str | int | FlextCore.Types.StringList | FlextCore.Types.Dict
        ]
        type PerformanceMetrics = dict[str, int | float | FlextCore.Types.Dict]

    # =========================================================================
    # WORKFLOW TYPES - Business process workflow types
    # =========================================================================

    class Workflow:
        """Oracle WMS workflow complex types."""

        type WorkflowDefinition = dict[
            str, str | list[dict[str, FlextOracleWmsTypes.Core.JsonValue]]
        ]
        type ProcessStep = dict[
            str, str | dict[str, FlextOracleWmsTypes.Core.JsonValue]
        ]
        type BusinessRule = dict[str, bool | str | FlextCore.Types.Dict]
        type ApprovalProcess = dict[
            str, str | bool | FlextCore.Types.StringList | FlextCore.Types.Dict
        ]
        type StatusTracking = dict[
            str, str | dict[str, FlextOracleWmsTypes.Core.JsonValue]
        ]
        type EventHandling = dict[str, str | FlextCore.Types.Dict]

    # =========================================================================
    # INTEGRATION TYPES - External system integration types
    # =========================================================================

    class Integration:
        """Oracle WMS integration complex types."""

        type IntegrationConfig = dict[
            str, FlextOracleWmsTypes.Core.ConfigValue | FlextCore.Types.Dict
        ]
        type DataMapping = dict[
            str, str | dict[str, FlextOracleWmsTypes.Core.JsonValue]
        ]
        type MessageFormat = dict[str, str | FlextCore.Types.Dict]
        type SyncConfiguration = dict[str, bool | int | str | FlextCore.Types.Dict]
        type ErrorHandling = dict[
            str, str | bool | dict[str, FlextOracleWmsTypes.Core.JsonValue]
        ]
        type RetryPolicy = dict[str, int | float | bool | FlextCore.Types.Dict]

    # =========================================================================
    # REPORTING TYPES - WMS reporting and analytics types
    # =========================================================================

    class Reporting:
        """Oracle WMS reporting complex types."""

        type ReportConfiguration = dict[
            str, FlextOracleWmsTypes.Core.JsonValue | FlextCore.Types.Dict
        ]
        type MetricDefinition = dict[
            str, str | dict[str, FlextOracleWmsTypes.Core.JsonValue]
        ]
        type DashboardConfig = dict[str, str | list[FlextCore.Types.Dict]]
        type AlertConfiguration = dict[str, str | bool | int | FlextCore.Types.Dict]
        type DataExport = dict[str, str | dict[str, FlextOracleWmsTypes.Core.JsonValue]]
        type AnalyticsConfig = dict[
            str, FlextOracleWmsTypes.Core.JsonValue | FlextCore.Types.Dict
        ]

    # =========================================================================
    # CORE TYPES - Essential Oracle WMS types extending FlextOracleWmsTypes.Core
    # =========================================================================

    class Core(FlextCore.Types.Core):
        """Core Oracle WMS types extending FlextOracleWmsTypes.Core.

        Essential domain-specific types for Oracle WMS operations.
        Replaces generic FlextCore.Types.Dict with semantic Oracle WMS types.
        """

        # Connection and API types
        type ConnectionDict = dict[str, str | int | bool | FlextCore.Types.Dict]
        type ConfigDict = dict[
            str, FlextOracleWmsTypes.Core.ConfigValue | FlextCore.Types.Dict
        ]
        type ApiResponseDict = dict[
            str, FlextOracleWmsTypes.Core.JsonValue | FlextCore.Types.Dict
        ]
        type AuthDict = dict[str, str | FlextCore.Types.Dict]

        # Warehouse and inventory types
        type WarehouseDict = dict[
            str, FlextOracleWmsTypes.Core.JsonValue | FlextCore.Types.Dict
        ]
        type InventoryDict = dict[
            str, FlextOracleWmsTypes.Core.JsonValue | FlextCore.Types.Dict
        ]
        type LocationDict = dict[
            str, str | dict[str, FlextOracleWmsTypes.Core.JsonValue]
        ]
        type StockDict = dict[str, int | float | str | FlextCore.Types.Dict]

        # Task and workflow types
        type TaskDict = dict[str, str | bool | int | FlextCore.Types.Dict]
        type WorkflowDict = dict[
            str, FlextOracleWmsTypes.Core.JsonValue | FlextCore.Types.Dict
        ]
        type ProcessDict = dict[
            str, str | dict[str, FlextOracleWmsTypes.Core.JsonValue]
        ]
        type BusinessRuleDict = dict[str, bool | str | FlextCore.Types.Dict]

        # Integration and reporting types
        type IntegrationDict = dict[
            str, FlextOracleWmsTypes.Core.ConfigValue | FlextCore.Types.Dict
        ]
        type MessageDict = dict[str, str | FlextCore.Types.Dict]
        type ReportDict = dict[
            str, FlextOracleWmsTypes.Core.JsonValue | FlextCore.Types.Dict
        ]
        type MetricDict = dict[str, str | dict[str, FlextOracleWmsTypes.Core.JsonValue]]

        # Data processing types
        type RecordDict = FlextCore.Types.Dict
        type FilterDict = FlextCore.Types.Dict
        type ResultDict = FlextCore.Types.Dict
        type ContextDict = FlextCore.Types.Dict
        type EntityDict = FlextCore.Types.Dict
        type DataDict = FlextCore.Types.Dict

        # Collection types for Oracle WMS operations
        type RecordList = list[RecordDict]
        type EntityList = list[EntityDict]
        type ResultList = list[ResultDict]
        type StringList = FlextCore.Types.StringList

    # =========================================================================
    # ORACLE WMS PROJECT TYPES - Domain-specific project types extending FlextCore.Types
    # =========================================================================

    class Project(FlextCore.Types.Project):
        """Oracle WMS-specific project types extending FlextCore.Types.Project.

        Adds Oracle WMS/warehouse management-specific project types while inheriting
        generic types from FlextCore.Types. Follows domain separation principle:
        Oracle WMS domain owns warehouse management and logistics-specific types.
        """

        # Oracle WMS-specific project types extending the generic ones
        type ProjectType = Literal[
            # Generic types inherited from FlextCore.Types.Project
            "library",
            "application",
            "service",
            # Oracle WMS-specific types
            "wms-service",
            "warehouse-management",
            "inventory-system",
            "shipping-service",
            "picking-system",
            "wms-integration",
            "warehouse-api",
            "logistics-platform",
            "inventory-tracker",
            "warehouse-monitor",
            "wms-connector",
            "fulfillment-engine",
            "warehouse-analytics",
            "wms-client",
            "logistics-service",
            "warehouse-optimizer",
        ]

        # Oracle WMS-specific project configurations
        type WmsProjectConfig = dict[str, FlextOracleWmsTypes.Core.ConfigValue | object]
        type WarehouseConfig = dict[str, str | int | bool | FlextCore.Types.StringList]
        type InventoryConfig = dict[str, bool | str | FlextCore.Types.Dict]
        type LogisticsConfig = dict[str, FlextOracleWmsTypes.Core.ConfigValue | object]


# =============================================================================
# PUBLIC API EXPORTS - Oracle WMS TypeVars and types
# =============================================================================

__all__: FlextCore.Types.StringList = [
    "FlextOracleWmsTypes",
]
