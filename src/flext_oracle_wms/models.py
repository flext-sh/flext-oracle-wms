"""FLEXT WMS Models - Generic WMS Domain Model.

domain-driven design with minimal declarations using composition.
Python 3.13+ syntax, one class per module, SOLID principles. Generic for any WMS.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Annotated, Literal

from flext_core import FlextModels, r
from pydantic import BaseModel, ConfigDict, Field, StringConstraints, field_validator

from flext_oracle_wms.constants import FlextOracleWmsConstants as c
from flext_oracle_wms.typings import t


class FlextOracleWmsModels(FlextModels):
    """Generic WMS domain models with composition patterns.

    Single class per module following DDD, SOLID, and flext-core patterns.
    Uses Python 3.13+ syntax and AST-optimized declarations for minimal line count.
    Generic for any WMS system.
    """

    def __init_subclass__(cls, **kwargs: t.Scalar) -> None:
        """Allow downstream projects to inherit FlextOracleWmsModels for namespace composition."""
        super().__init_subclass__(**kwargs)

    # =========================================================================
    # ORACLE WMS NAMESPACE - Domain-specific models
    # =========================================================================

    class OracleWms:
        """Oracle WMS domain namespace -- m.OracleWms.*."""

        class Entity(BaseModel):
            """Oracle WMS entity definition."""

            model_config = ConfigDict(extra="forbid")

            name: Annotated[str, Field(min_length=1, description="Entity name")]
            endpoint: Annotated[
                str, Field(min_length=1, description="API endpoint path")
            ]
            description: Annotated[
                str | None, Field(default=None, description="Entity description")
            ]
            primary_key: Annotated[
                str | None, Field(default=None, description="Primary key field")
            ]
            replication_key: Annotated[
                str | None, Field(default=None, description="Replication key field")
            ]
            supports_incremental: Annotated[
                bool,
                Field(
                    default=False,
                    description="Whether entity supports incremental sync",
                ),
            ]

            @field_validator("endpoint")
            @classmethod
            def _validate_endpoint_starts_with_slash(cls, v: str) -> str:
                if not v.startswith("/"):
                    msg = "Endpoint must start with '/'"
                    raise ValueError(msg)
                return v

            def validate_entity(self) -> r[bool]:
                """Validate entity configuration."""
                if not self.name:
                    return r[bool].fail("Entity name is required")
                if not self.endpoint:
                    return r[bool].fail("Entity endpoint is required")
                return r[bool].ok(True)

        class ApiResponse(BaseModel):
            """Oracle WMS API response model."""

            data: Annotated[
                dict[str, t.ContainerValue],
                Field(default_factory=dict, description="Response data"),
            ]
            status_code: Annotated[
                int, Field(default=200, ge=200, le=599, description="HTTP status code")
            ]
            success: Annotated[
                bool, Field(default=True, description="Whether request succeeded")
            ]
            error_message: Annotated[
                str | None, Field(default=None, description="Error message if any")
            ]

            def validate_response(self) -> r[bool]:
                """Validate response state."""
                if not self.success and not self.error_message:
                    return r[bool].fail("Failed response must include error message")
                return r[bool].ok(True)

    # =========================================================================
    # TYPE ALIASES - Advanced composition for minimal declarations
    # =========================================================================

    type TRecord = dict[str, t.ContainerValue]
    type TRecordBatch = list[dict[str, t.ContainerValue]]
    type TSchema = dict[str, dict[str, t.ContainerValue]]
    type TApiResponse = dict[str, t.ContainerValue]
    type TApiVersion = Literal["v2", "v1"]
    type TEntityId = Annotated[str, StringConstraints(min_length=1, max_length=100)]
    type TEntityName = Annotated[
        str,
        StringConstraints(min_length=1, max_length=50, pattern=r"^[a-z0-9_]+$"),
    ]
    type TFilterValue = t.Scalar | None
    type TFilters = dict[str, t.Scalar | None]
    type TPaginationInfo = dict[str, int]
    type TTimeout = Annotated[int, Field(ge=1, le=300)]

    # =========================================================================
    # DOMAIN ENTITIES - Composed DDD patterns
    # =========================================================================

    class WmsEntity(BaseModel):
        """Base WMS entity with identity."""

        model_config = ConfigDict(extra="forbid")

        id: Annotated[str, Field(default="", description="Entity identifier")]
        name: Annotated[str, Field(default="", description="Entity name")]
        created_at: Annotated[
            str | None, Field(default=None, description="Creation timestamp")
        ]
        updated_at: Annotated[
            str | None,
            Field(
                default=None,
                description="Last update timestamp",
            ),
        ]

    class InventoryItem(WmsEntity):
        """Inventory domain entity."""

        sku: Annotated[str, Field(default="", description="Stock keeping unit")]
        quantity: Annotated[
            t.NonNegativeInt, Field(default=0, description="Item quantity")
        ]
        location_id: Annotated[
            str, Field(default="", description="Storage location identifier")
        ]
        status: Annotated[str, Field(default="active", description="Item status")]

    class Order(WmsEntity):
        """Order domain entity."""

        customer_id: Annotated[
            str, Field(default="", description="Customer identifier")
        ]
        status: Annotated[str, Field(default="pending", description="Order status")]
        total_amount: Annotated[
            t.NonNegativeFloat,
            Field(
                default=0.0,
                description="Total order amount",
            ),
        ]
        items: Annotated[
            list[dict[str, t.ContainerValue]],
            Field(default_factory=list, description="Order items"),
        ]

    class Shipment(WmsEntity):
        """Shipment domain entity."""

        order_id: Annotated[
            str, Field(default="", description="Associated order identifier")
        ]
        status: Annotated[str, Field(default="pending", description="Shipment status")]
        carrier: Annotated[
            str | None, Field(default=None, description="Shipping carrier name")
        ]
        tracking_number: Annotated[
            str | None,
            Field(
                default=None,
                description="Shipment tracking number",
            ),
        ]

    class PickingTask(WmsEntity):
        """Picking task domain entity."""

        wave_id: Annotated[str, Field(default="", description="Wave identifier")]
        status: Annotated[str, Field(default="pending", description="Task status")]
        items: Annotated[
            list[dict[str, t.ContainerValue]],
            Field(default_factory=list, description="Task items"),
        ]

    class Location(WmsEntity):
        """Location domain entity."""

        aisle: Annotated[str, Field(default="", description="Aisle identifier")]
        shelf: Annotated[str, Field(default="", description="Shelf identifier")]
        bin_: Annotated[str, Field(default="", description="Bin identifier")]
        zone: Annotated[str, Field(default="", description="Zone identifier")]

    # =========================================================================
    # VALUE OBJECTS - Immutable domain values
    # =========================================================================

    class WarehouseLocation(BaseModel):
        """Warehouse location value object."""

        model_config = ConfigDict(frozen=True, extra="forbid")

        aisle: Annotated[str, Field(description="Aisle identifier")]
        shelf: Annotated[str, Field(description="Shelf identifier")]
        bin_: Annotated[str, Field(description="Bin identifier")]
        zone: Annotated[str, Field(default="", description="Zone identifier")]

        @property
        def full_location(self) -> str:
            """Get full location string."""
            return f"{self.zone}-{self.aisle}-{self.shelf}-{self.bin_}"

    class ApiCredentials(BaseModel):
        """API credentials value object."""

        model_config = ConfigDict(frozen=True, extra="forbid")

        username: Annotated[str, Field(description="API username")]
        password: Annotated[str | None, Field(default=None, description="API password")]
        token: Annotated[str | None, Field(default=None, description="API token")]

    # =========================================================================
    # ENUMS - Aliases from constants.py (single source of truth)
    # =========================================================================

    EntityType: type[c.WmsEntityType] = c.WmsEntityType
    OperationStatus: type[c.WmsOperationStatus] = c.WmsOperationStatus

    # =========================================================================
    # DOMAIN SERVICES - Business logic composition
    # =========================================================================

    # Domain constants
    MAX_ENTITY_NAME_LENGTH: int = 50

    @staticmethod
    def calculate_inventory_value(item: InventoryItem, price: float) -> float:
        """Calculate inventory value using domain logic."""
        return item.quantity * price

    @staticmethod
    def validate_entity_name(name: str) -> r[str]:
        """Validate entity name using domain rules."""
        if not name or len(name) > FlextOracleWmsModels.MAX_ENTITY_NAME_LENGTH:
            return r[str].fail("Invalid entity name")
        return r[str].ok(name)

    # =========================================================================
    # AGGREGATE ROOTS - Consistency boundaries
    # =========================================================================

    class WarehouseAggregate(FlextModels.AggregateRoot):
        """Warehouse aggregate root."""

        id: str
        name: str
        locations: Annotated[
            list[FlextOracleWmsModels.WarehouseLocation],
            Field(default_factory=list),
        ]
        inventory: Annotated[
            list[FlextOracleWmsModels.InventoryItem],
            Field(default_factory=list),
        ]

        def add_inventory(self, item: FlextOracleWmsModels.InventoryItem) -> r[bool]:
            """Add inventory to warehouse."""
            if any(i.sku == item.sku for i in self.inventory):
                return r[bool].fail("SKU already exists")
            self.inventory.append(item)
            return r[bool].ok(True)


__all__ = ["FlextOracleWmsModels"]

m = FlextOracleWmsModels
