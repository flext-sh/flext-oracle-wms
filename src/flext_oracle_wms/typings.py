"""FLEXT Oracle WMS Types - Domain-specific Oracle WMS type definitions.

This module provides Oracle WMS-specific type definitions extending FlextTypes.
Follows FLEXT standards:
- Domain-specific complex types only
- No simple aliases to primitive types
- Python 3.13+ syntax
- Extends FlextTypes properly

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Literal

from flext_core import FlextTypes

# =============================================================================
# ORACLE WMS-SPECIFIC TYPE VARIABLES - Domain-specific TypeVars for Oracle WMS operations
# =============================================================================


# Oracle WMS domain TypeVars
class FlextOracleWmsTypes(FlextTypes):
    """Oracle WMS-specific type definitions extending FlextTypes.

    Domain-specific type system for Oracle Warehouse Management System operations.
    Contains ONLY complex Oracle WMS-specific types, no simple aliases.
    Uses Python 3.13+ type syntax and patterns.
    """

    # =========================================================================
    # WMS CONNECTION TYPES - Oracle WMS system connection configuration
    # =========================================================================

    class Connection:
        """Oracle WMS connection complex types."""

        type WmsConnectionConfig = dict[str, str | int | bool | dict[str, object]]
        type DatabaseConnection = dict[
            str, FlextTypes.Core.ConfigValue | dict[str, object]
        ]
        type ApiConnection = dict[str, str | dict[str, FlextTypes.Core.JsonValue]]
        type AuthenticationConfig = dict[str, str | dict[str, object]]
        type SessionConfig = dict[str, int | bool | str | dict[str, object]]
        type SecurityConfig = dict[
            str, bool | str | dict[str, FlextTypes.Core.ConfigValue]
        ]

    # =========================================================================
    # WAREHOUSE TYPES - Warehouse structure and configuration types
    # =========================================================================

    class Warehouse:
        """Oracle WMS warehouse complex types."""

        type WarehouseConfiguration = dict[
            str, FlextTypes.Core.JsonValue | dict[str, object]
        ]
        type LocationDefinition = dict[str, str | dict[str, FlextTypes.Core.JsonValue]]
        type ZoneConfiguration = dict[str, str | list[str] | dict[str, object]]
        type AreaDefinition = dict[
            str, str | int | dict[str, FlextTypes.Core.JsonValue]
        ]
        type CapacityConfiguration = dict[str, int | float | dict[str, object]]
        type LayoutConfiguration = dict[
            str, FlextTypes.Core.JsonValue | dict[str, object]
        ]

    # =========================================================================
    # INVENTORY TYPES - Inventory management and tracking types
    # =========================================================================

    class Inventory:
        """Oracle WMS inventory complex types."""

        type InventoryItem = dict[str, FlextTypes.Core.JsonValue | dict[str, object]]
        type StockLevel = dict[str, int | float | str | dict[str, object]]
        type MovementRecord = dict[
            str, str | int | dict[str, FlextTypes.Core.JsonValue]
        ]
        type AllocationRule = dict[str, str | bool | dict[str, object]]
        type ReservationConfig = dict[
            str, FlextTypes.Core.JsonValue | dict[str, object]
        ]
        type CycleCountConfig = dict[str, int | bool | str | dict[str, object]]

    # =========================================================================
    # TASK MANAGEMENT TYPES - WMS task execution and workflow types
    # =========================================================================

    class TaskManagement:
        """Oracle WMS task management complex types."""

        type TaskDefinition = dict[str, str | dict[str, FlextTypes.Core.JsonValue]]
        type TaskExecution = dict[str, str | bool | int | dict[str, object]]
        type WorkOrder = dict[str, FlextTypes.Core.JsonValue | dict[str, object]]
        type TaskPriority = dict[str, int | str | dict[str, object]]
        type ResourceAllocation = dict[str, str | int | list[str] | dict[str, object]]
        type PerformanceMetrics = dict[str, int | float | dict[str, object]]

    # =========================================================================
    # WORKFLOW TYPES - Business process workflow types
    # =========================================================================

    class Workflow:
        """Oracle WMS workflow complex types."""

        type WorkflowDefinition = dict[
            str, str | list[dict[str, FlextTypes.Core.JsonValue]]
        ]
        type ProcessStep = dict[str, str | dict[str, FlextTypes.Core.JsonValue]]
        type BusinessRule = dict[str, bool | str | dict[str, object]]
        type ApprovalProcess = dict[str, str | bool | list[str] | dict[str, object]]
        type StatusTracking = dict[str, str | dict[str, FlextTypes.Core.JsonValue]]
        type EventHandling = dict[str, str | dict[str, object]]

    # =========================================================================
    # INTEGRATION TYPES - External system integration types
    # =========================================================================

    class Integration:
        """Oracle WMS integration complex types."""

        type IntegrationConfig = dict[
            str, FlextTypes.Core.ConfigValue | dict[str, object]
        ]
        type DataMapping = dict[str, str | dict[str, FlextTypes.Core.JsonValue]]
        type MessageFormat = dict[str, str | dict[str, object]]
        type SyncConfiguration = dict[str, bool | int | str | dict[str, object]]
        type ErrorHandling = dict[
            str, str | bool | dict[str, FlextTypes.Core.JsonValue]
        ]
        type RetryPolicy = dict[str, int | float | bool | dict[str, object]]

    # =========================================================================
    # REPORTING TYPES - WMS reporting and analytics types
    # =========================================================================

    class Reporting:
        """Oracle WMS reporting complex types."""

        type ReportConfiguration = dict[
            str, FlextTypes.Core.JsonValue | dict[str, object]
        ]
        type MetricDefinition = dict[str, str | dict[str, FlextTypes.Core.JsonValue]]
        type DashboardConfig = dict[str, str | list[dict[str, object]]]
        type AlertConfiguration = dict[str, str | bool | int | dict[str, object]]
        type DataExport = dict[str, str | dict[str, FlextTypes.Core.JsonValue]]
        type AnalyticsConfig = dict[str, FlextTypes.Core.JsonValue | dict[str, object]]

    # =========================================================================
    # ORACLE WMS PROJECT TYPES - Domain-specific project types extending FlextTypes
    # =========================================================================

    class Project(FlextTypes.Project):
        """Oracle WMS-specific project types extending FlextTypes.Project.

        Adds Oracle WMS/warehouse management-specific project types while inheriting
        generic types from FlextTypes. Follows domain separation principle:
        Oracle WMS domain owns warehouse management and logistics-specific types.
        """

        # Oracle WMS-specific project types extending the generic ones
        type ProjectType = Literal[
            # Generic types inherited from FlextTypes.Project
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
        type WmsProjectConfig = dict[str, FlextTypes.Core.ConfigValue | object]
        type WarehouseConfig = dict[str, str | int | bool | list[str]]
        type InventoryConfig = dict[str, bool | str | dict[str, object]]
        type LogisticsConfig = dict[str, FlextTypes.Core.ConfigValue | object]


# =============================================================================
# PUBLIC API EXPORTS - Oracle WMS TypeVars and types
# =============================================================================

__all__: list[str] = [
    "FlextOracleWmsTypes",
]
