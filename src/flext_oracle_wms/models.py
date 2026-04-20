"""FLEXT WMS Models - Generic WMS Domain Model.

domain-driven design with minimal declarations using composition.
Python 3.13+ syntax, one class per module, SOLID principles. Generic for any WMS.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    MutableSequence,
    Sequence,
)
from typing import Annotated, ClassVar

from flext_api import m, u

from flext_oracle_wms import c, p, r, t


class FlextOracleWmsModels(m):
    """Generic WMS domain models with composition patterns.

    Single class per module following DDD, SOLID, and flext-core patterns.
    Uses Python 3.13+ syntax and AST-optimized declarations for minimal line count.
    Generic for any WMS system.
    """

    # =========================================================================
    # ORACLE WMS NAMESPACE - Domain-specific models
    # =========================================================================

    class OracleWms:
        """Oracle WMS domain namespace -- m.OracleWms.*."""

        class FlextOracleWmsOperatorFilter(m.BaseModel):
            """Operator filter model for WMS filtering operations."""

            operator: str
            value: t.OracleWms.Core.FilterScalar | t.OracleWms.Core.FilterList

        class Entity(m.BaseModel):
            """Oracle WMS entity definition."""

            _flext_enforcement_exempt: ClassVar[bool] = True

            model_config: ClassVar[m.ConfigDict] = m.ConfigDict(extra="forbid")

            name: Annotated[str, u.Field(min_length=1, description="Entity name")]
            endpoint: Annotated[
                str,
                u.Field(min_length=1, description="API endpoint path"),
            ]
            description: Annotated[
                str | None,
                u.Field(description="Entity description"),
            ] = None
            primary_key: Annotated[
                str | None,
                u.Field(description="Primary key field"),
            ] = None
            replication_key: Annotated[
                str | None,
                u.Field(description="Replication key field"),
            ] = None
            supports_incremental: Annotated[
                bool,
                u.Field(
                    description="Whether entity supports incremental sync",
                ),
            ] = False

            @u.field_validator("endpoint")
            @classmethod
            def _validate_endpoint_starts_with_slash(cls, v: str) -> str:
                if not v.startswith("/"):
                    msg = "Endpoint must start with '/'"
                    raise ValueError(msg)
                return v

            def validate_entity(self) -> p.Result[bool]:
                """Validate entity configuration."""
                if not self.name:
                    return r[bool].fail("Entity name is required")
                if len(self.name) > c.OracleWms.WmsEntities.MAX_ENTITY_NAME_LENGTH:
                    return r[bool].fail("Entity name is too long")
                if not self.endpoint:
                    return r[bool].fail("Entity endpoint is required")
                return r[bool].ok(True)

        class ApiResponse(m.BaseModel):
            """Oracle WMS API response model."""

            data: Annotated[
                t.ContainerValueMapping,
                u.Field(description="Response data"),
            ] = u.Field(default_factory=dict)
            status_code: Annotated[
                t.HttpStatusCode,
                u.Field(description="HTTP status code"),
            ] = 200
            success: Annotated[
                bool,
                u.Field(description="Whether request succeeded"),
            ] = True
            error_message: Annotated[
                str | None,
                u.Field(description="Error message if any"),
            ] = None

            def validate_response(self) -> p.Result[bool]:
                """Validate response state."""
                if not self.success and not self.error_message:
                    return r[bool].fail("Failed response must include error message")
                return r[bool].ok(True)

        class ApiEndpoint(m.BaseModel):
            """Typed Oracle WMS API endpoint definition."""

            name: Annotated[str, u.Field(min_length=1)]
            method: Annotated[str, u.Field(min_length=1)]
            path: Annotated[str, u.Field(min_length=1)]
            version: Annotated[str, u.Field(min_length=1)]
            category: Annotated[str, u.Field(min_length=1)]
            description: str = ""
            since_version: str = "6.1"

        class AuthSettings(m.BaseModel):
            """Authentication configuration for Oracle WMS flows."""

            method: str = c.OracleWms.OracleWMSAuthMethod.BASIC
            username: str | None = None
            password: str | None = None
            oauth2_client_id: str | None = None
            oauth2_client_secret: str | None = None
            oauth2_scope: str = "wms.read wms.write"
            token_refresh_threshold: t.PositiveInt = 300

            @property
            def normalized_method(self) -> str:
                """Return auth method in canonical lowercase form."""
                return str(self.method).strip().lower()

            def validate_business_rules(self) -> p.Result[bool]:
                """Validate authentication configuration business rules."""
                basic_method = str(c.OracleWms.OracleWMSAuthMethod.BASIC)
                oauth2_method = str(c.OracleWms.OracleWMSAuthMethod.OAUTH2)
                if self.normalized_method == basic_method:
                    if not self.username or not self.password:
                        return r[bool].fail("Basic auth requires username and password")
                    return r[bool].ok(True)
                if self.normalized_method == oauth2_method:
                    if not self.oauth2_client_id or not self.oauth2_client_secret:
                        return r[bool].fail(
                            "OAuth2 requires client_id and client_secret",
                        )
                    return r[bool].ok(True)
                return r[bool].fail(f"Unsupported auth method: {self.method}")

        class EntitiesResponse(m.BaseModel):
            """Oracle WMS entities list response."""

            model_config: ClassVar[m.ConfigDict] = m.ConfigDict(extra="ignore")

            entities: t.StrSequence = u.Field(default_factory=tuple)

        class ApiCategoryResponse(m.BaseModel):
            """Oracle WMS API category response."""

            model_config: ClassVar[m.ConfigDict] = m.ConfigDict(extra="ignore")

            apis: Sequence[t.StrMapping] = u.Field(default_factory=tuple)

        class EntityDataResponse(m.BaseModel):
            """Oracle WMS entity data response."""

            model_config: ClassVar[m.ConfigDict] = m.ConfigDict(extra="ignore")

            data: Sequence[t.StrMapping] = u.Field(default_factory=tuple)

        # =====================================================================
        # DOMAIN ENTITIES - Composed DDD patterns
        # =====================================================================

        class WmsEntity(m.BaseModel):
            """Base WMS entity with identity."""

            model_config: ClassVar[m.ConfigDict] = m.ConfigDict(extra="forbid")

            id: Annotated[str, u.Field(description="Entity identifier")] = ""
            name: Annotated[str, u.Field(description="Entity name")] = ""
            created_at: Annotated[
                str | None,
                u.Field(description="Creation timestamp"),
            ] = None
            updated_at: Annotated[
                str | None,
                u.Field(description="Last update timestamp"),
            ] = None

        class InventoryItem(WmsEntity):
            """Inventory domain entity."""

            sku: Annotated[str, u.Field(description="Stock keeping unit")] = ""
            quantity: Annotated[
                t.NonNegativeInt,
                u.Field(description="Item quantity"),
            ] = 0
            location_id: Annotated[
                str,
                u.Field(description="Storage location identifier"),
            ] = ""
            status: Annotated[str, u.Field(description="Item status")] = "active"

        class Order(WmsEntity):
            """Order domain entity."""

            customer_id: Annotated[
                str,
                u.Field(description="Customer identifier"),
            ] = ""
            status: Annotated[str, u.Field(description="Order status")] = "pending"
            total_amount: Annotated[
                t.NonNegativeFloat,
                u.Field(description="Total order amount"),
            ] = 0.0
            items: Annotated[
                Sequence[t.ContainerValueMapping],
                u.Field(description="Order items"),
            ] = u.Field(default_factory=tuple)

        class Shipment(WmsEntity):
            """Shipment domain entity."""

            order_id: Annotated[
                str,
                u.Field(description="Associated order identifier"),
            ] = ""
            status: Annotated[str, u.Field(description="Shipment status")] = "pending"
            carrier: Annotated[
                str | None,
                u.Field(description="Shipping carrier name"),
            ] = None
            tracking_number: Annotated[
                str | None,
                u.Field(description="Shipment tracking number"),
            ] = None

        class PickingTask(WmsEntity):
            """Picking task domain entity."""

            wave_id: Annotated[str, u.Field(description="Wave identifier")] = ""
            status: Annotated[str, u.Field(description="Task status")] = "pending"
            items: Annotated[
                Sequence[t.ContainerValueMapping],
                u.Field(description="Task items"),
            ] = u.Field(default_factory=tuple)

        class Location(WmsEntity):
            """Location domain entity."""

            aisle: Annotated[str, u.Field(description="Aisle identifier")] = ""
            shelf: Annotated[str, u.Field(description="Shelf identifier")] = ""
            bin_: Annotated[str, u.Field(description="Bin identifier")] = ""
            zone: Annotated[str, u.Field(description="Zone identifier")] = ""

        # =====================================================================
        # VALUE OBJECTS - Immutable domain values
        # =====================================================================

        class WarehouseLocation(m.BaseModel):
            """Warehouse location value object."""

            model_config: ClassVar[m.ConfigDict] = m.ConfigDict(
                frozen=True, extra="forbid"
            )

            aisle: Annotated[str, u.Field(description="Aisle identifier")]
            shelf: Annotated[str, u.Field(description="Shelf identifier")]
            bin_: Annotated[str, u.Field(description="Bin identifier")]
            zone: Annotated[str, u.Field(description="Zone identifier")] = ""

            @property
            def full_location(self) -> str:
                """Get full location string."""
                return f"{self.zone}-{self.aisle}-{self.shelf}-{self.bin_}"

        class ApiCredentials(m.BaseModel):
            """API credentials value object."""

            model_config: ClassVar[m.ConfigDict] = m.ConfigDict(
                frozen=True, extra="forbid"
            )

            username: Annotated[str, u.Field(description="API username")]
            password: Annotated[str | None, u.Field(description="API password")] = None
            token: Annotated[str | None, u.Field(description="API token")] = None

        # =====================================================================
        # AGGREGATE ROOTS - Consistency boundaries
        # =====================================================================

        class WarehouseAggregate(m.AggregateRoot):
            """Warehouse aggregate root."""

            _flext_enforcement_exempt: ClassVar[bool] = True

            id: Annotated[str, u.Field(description="Warehouse identifier")]
            name: Annotated[str, u.Field(description="Warehouse name")]
            locations: Annotated[
                Sequence[FlextOracleWmsModels.OracleWms.WarehouseLocation],
                u.Field(description="Warehouse locations"),
            ] = u.Field(default_factory=tuple)
            inventory: Annotated[
                MutableSequence[FlextOracleWmsModels.OracleWms.InventoryItem],
                u.Field(description="Warehouse inventory items"),
            ] = u.Field(default_factory=list)

            def add_inventory(
                self, item: FlextOracleWmsModels.OracleWms.InventoryItem
            ) -> p.Result[bool]:
                """Add inventory to warehouse."""
                if any(i.sku == item.sku for i in self.inventory):
                    return r[bool].fail("SKU already exists")
                self.inventory.append(item)
                return r[bool].ok(True)

        # =========================================================================
        # DOMAIN SERVICES - Business logic composition
        # =========================================================================

        # Domain constants
        MAX_ENTITY_NAME_LENGTH: int = 50

        @staticmethod
        def calculate_inventory_value(
            item: FlextOracleWmsModels.OracleWms.InventoryItem, price: float
        ) -> float:
            """Calculate inventory value using domain logic."""
            return item.quantity * price

        @staticmethod
        def validate_entity_name(name: str) -> p.Result[str]:
            """Validate entity name using domain rules."""
            if (
                not name
                or len(name) > FlextOracleWmsModels.OracleWms.MAX_ENTITY_NAME_LENGTH
            ):
                return r[str].fail("Invalid entity name")
            return r[str].ok(name)


m = FlextOracleWmsModels

__all__: list[str] = ["FlextOracleWmsModels"]
