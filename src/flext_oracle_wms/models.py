"""FLEXT WMS Models - Generic WMS Domain Model.

 domain-driven design with minimal declarations using composition.
Python 3.13+ syntax, one class per module, SOLID principles. Generic for any WMS.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Annotated

from flext_core import FlextModels, FlextResult
from flext_core.utilities import u
from pydantic import Field, StringConstraints


class FlextWmsModels(FlextModels):
    """Generic WMS domain models with composition patterns.

    Single class per module following DDD, SOLID, and flext-core patterns.
    Uses Python 3.13+ syntax and AST-optimized declarations for minimal line count.
    Generic for any WMS system.
    """

    def __init_subclass__(cls, **kwargs: object) -> None:
        """Warn when FlextWmsModels is subclassed directly."""
        super().__init_subclass__(**kwargs)
        u.Deprecation.warn_once(
            f"subclass:{cls.__name__}",
            "Subclassing FlextWmsModels is deprecated. Use FlextModels.Wms instead.",
        )

    # =========================================================================
    # TYPE ALIASES - Advanced composition for minimal declarations
    # =========================================================================

    type TRecord = dict[str, object]
    type TRecordBatch = list[TRecord]
    type TSchema = dict[str, dict[str, object]]
    type TApiResponse = dict[str, object]
    type TApiVersion = Literal[v2, v1, legacy]
    type TEntityId = Annotated[str, StringConstraints(min_length=1, max_length=100)]
    type TEntityName = Annotated[
        str,
        StringConstraints(min_length=1, max_length=50, pattern=r"^[a-z0-9_]+$"),
    ]
    type TFilterValue = str | int | float | bool | None
    type TFilters = dict[str, TFilterValue]
    type TPaginationInfo = dict[str, int]
    type TTimeout = Annotated[int, Field(ge=1, le=300)]

    # =========================================================================
    # DOMAIN ENTITIES - Composed DDD patterns
    # =========================================================================

    @dataclass
    class WmsEntity:
        """Base WMS entity with identity."""

        id: str
        name: str
        created_at: str | None = field(default=None)
        updated_at: str | None = field(default=None)

    @dataclass
    class InventoryItem(WmsEntity):
        """Inventory domain entity."""

        sku: str = ""
        quantity: int = 0
        location_id: str = ""
        status: str = "active"

    @dataclass
    class Order(WmsEntity):
        """Order domain entity."""

        customer_id: str = ""
        status: str = "pending"
        total_amount: float = 0.0
        items: list[dict[str, object]] = field(default_factory=list)

    @dataclass
    class Shipment(WmsEntity):
        """Shipment domain entity."""

        order_id: str = ""
        status: str = "pending"
        carrier: str | None = None
        tracking_number: str | None = None

    @dataclass
    class PickingTask(WmsEntity):
        """Picking task domain entity."""

        wave_id: str = ""
        status: str = "pending"
        items: list[dict[str, object]] = field(default_factory=list)

    @dataclass
    class Location(WmsEntity):
        """Location domain entity."""

        aisle: str = ""
        shelf: str = ""
        bin_: str = ""
        zone: str = ""

    # =========================================================================
    # VALUE OBJECTS - Immutable domain values
    # =========================================================================

    @dataclass(frozen=True)
    class WarehouseLocation:
        """Warehouse location value object."""

        aisle: str
        shelf: str
        bin_: str
        zone: str = ""

        @property
        def full_location(self) -> str:
            """Get full location string."""
            return f"{self.zone}-{self.aisle}-{self.shelf}-{self.bin_}"

    @dataclass(frozen=True)
    class ApiCredentials:
        """API credentials value object."""

        username: str
        password: str | None = None
        token: str | None = None

    # =========================================================================
    # ENUMS - Composed domain enumerations
    # =========================================================================

    class EntityType(StrEnum):
        """WMS entity types."""

        INVENTORY = "inventory"
        ORDERS = "orders"
        SHIPMENTS = "shipments"
        PICKING = "picking"
        LOCATIONS = "locations"
        ITEMS = "items"
        PRODUCTS = "products"
        WAREHOUSES = "warehouses"

    class OperationStatus(StrEnum):
        """Operation status values."""

        PENDING = "pending"
        RUNNING = "running"
        SUCCESS = "success"
        ERROR = "error"
        CANCELLED = "cancelled"

    # =========================================================================
    # DOMAIN SERVICES - Business logic composition
    # =========================================================================

    # Domain constants
    MAX_ENTITY_NAME_LENGTH: int = 50

    @staticmethod
    def validate_entity_name(name: str) -> FlextResult[str]:
        """Validate entity name using domain rules."""
        if not name or len(name) > FlextWmsModels.MAX_ENTITY_NAME_LENGTH:
            return FlextResult.fail("Invalid entity name")
        return FlextResult.ok(name)

    @staticmethod
    def calculate_inventory_value(item: InventoryItem, price: float) -> float:
        """Calculate inventory value using domain logic."""
        return item.quantity * price

    # =========================================================================
    # AGGREGATE ROOTS - Consistency boundaries
    # =========================================================================

    @dataclass
    class WarehouseAggregate(FlextModels.AggregateRoot):
        """Warehouse aggregate root."""

        id: str
        name: str
        locations: list[WarehouseLocation] = field(default_factory=list)
        inventory: list[InventoryItem] = field(default_factory=list)

        def add_inventory(self, item: InventoryItem) -> FlextResult[None]:
            """Add inventory to warehouse."""
            if any(i.sku == item.sku for i in self.inventory):
                return FlextResult.fail("SKU already exists")
            self.inventory.append(item)
            return FlextResult.ok(None)


# Short aliases
m = FlextWmsModels
m_wms = FlextWmsModels

__all__ = ["FlextWmsModels", "m", "m_wms"]
