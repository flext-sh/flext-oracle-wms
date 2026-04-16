"""FLEXT WMS Models - Generic WMS Domain Model.

domain-driven design with minimal declarations using composition.
Python 3.13+ syntax, one class per module, SOLID principles. Generic for any WMS.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import MutableSequence, Sequence
from typing import Annotated, ClassVar

from flext_api import m
from pydantic import ConfigDict, field_validator

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

            model_config: ClassVar[ConfigDict] = ConfigDict(extra="forbid")

            name: Annotated[str, m.Field(min_length=1, description="Entity name")]
            endpoint: Annotated[
                str,
                m.Field(min_length=1, description="API endpoint path"),
            ]
            description: Annotated[
                str | None,
                m.Field(description="Entity description"),
            ] = None
            primary_key: Annotated[
                str | None,
                m.Field(description="Primary key field"),
            ] = None
            replication_key: Annotated[
                str | None,
                m.Field(description="Replication key field"),
            ] = None
            supports_incremental: Annotated[
                bool,
                m.Field(
                    description="Whether entity supports incremental sync",
                ),
            ] = False

            @field_validator("endpoint")
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
                if len(self.name) > c.WmsEntities.MAX_ENTITY_NAME_LENGTH:
                    return r[bool].fail("Entity name is too long")
                if not self.endpoint:
                    return r[bool].fail("Entity endpoint is required")
                return r[bool].ok(True)

        class ApiResponse(m.BaseModel):
            """Oracle WMS API response model."""

            data: Annotated[
                t.ContainerValueMapping,
                m.Field(description="Response data"),
            ] = m.Field(default_factory=dict)
            status_code: Annotated[
                t.HttpStatusCode,
                m.Field(description="HTTP status code"),
            ] = 200
            success: Annotated[
                bool,
                m.Field(description="Whether request succeeded"),
            ] = True
            error_message: Annotated[
                str | None,
                m.Field(description="Error message if any"),
            ] = None

            def validate_response(self) -> p.Result[bool]:
                """Validate response state."""
                if not self.success and not self.error_message:
                    return r[bool].fail("Failed response must include error message")
                return r[bool].ok(True)

        class ApiEndpoint(m.BaseModel):
            """Typed Oracle WMS API endpoint definition."""

            name: Annotated[str, m.Field(min_length=1)]
            method: Annotated[str, m.Field(min_length=1)]
            path: Annotated[str, m.Field(min_length=1)]
            version: Annotated[str, m.Field(min_length=1)]
            category: Annotated[str, m.Field(min_length=1)]
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

            def validate_business_rules(self) -> p.Result[bool]:
                """Validate authentication configuration business rules."""
                if self.method == c.OracleWms.OracleWMSAuthMethod.BASIC:
                    if not self.username or not self.password:
                        return r[bool].fail("Basic auth requires username and password")
                    return r[bool].ok(True)
                if self.method == c.OracleWms.OracleWMSAuthMethod.OAUTH2:
                    if not self.oauth2_client_id or not self.oauth2_client_secret:
                        return r[bool].fail(
                            "OAuth2 requires client_id and client_secret",
                        )
                    return r[bool].ok(True)
                return r[bool].fail(f"Unsupported auth method: {self.method}")

        class EntitiesResponse(m.BaseModel):
            """Oracle WMS entities list response."""

            model_config: ClassVar[ConfigDict] = ConfigDict(extra="ignore")

            entities: t.StrSequence = m.Field(default_factory=list)

        class ApiCategoryResponse(m.BaseModel):
            """Oracle WMS API category response."""

            model_config: ClassVar[ConfigDict] = ConfigDict(extra="ignore")

            apis: Sequence[t.StrMapping] = m.Field(
                default_factory=lambda: list[t.StrMapping]()
            )

        class EntityDataResponse(m.BaseModel):
            """Oracle WMS entity data response."""

            model_config: ClassVar[ConfigDict] = ConfigDict(extra="ignore")

            data: Sequence[t.StrMapping] = m.Field(
                default_factory=lambda: list[t.StrMapping]()
            )

        # =====================================================================
        # DOMAIN ENTITIES - Composed DDD patterns
        # =====================================================================

        class WmsEntity(m.BaseModel):
            """Base WMS entity with identity."""

            model_config: ClassVar[ConfigDict] = ConfigDict(extra="forbid")

            id: Annotated[str, m.Field(description="Entity identifier")] = ""
            name: Annotated[str, m.Field(description="Entity name")] = ""
            created_at: Annotated[
                str | None,
                m.Field(description="Creation timestamp"),
            ] = None
            updated_at: Annotated[
                str | None,
                m.Field(description="Last update timestamp"),
            ] = None

        class InventoryItem(WmsEntity):
            """Inventory domain entity."""

            sku: Annotated[str, m.Field(description="Stock keeping unit")] = ""
            quantity: Annotated[
                t.NonNegativeInt,
                m.Field(description="Item quantity"),
            ] = 0
            location_id: Annotated[
                str,
                m.Field(description="Storage location identifier"),
            ] = ""
            status: Annotated[str, m.Field(description="Item status")] = "active"

        class Order(WmsEntity):
            """Order domain entity."""

            customer_id: Annotated[
                str,
                m.Field(description="Customer identifier"),
            ] = ""
            status: Annotated[str, m.Field(description="Order status")] = "pending"
            total_amount: Annotated[
                t.NonNegativeFloat,
                m.Field(description="Total order amount"),
            ] = 0.0
            items: Annotated[
                Sequence[t.ContainerValueMapping],
                m.Field(description="Order items"),
            ] = m.Field(default_factory=lambda: list[t.ContainerValueMapping]())

        class Shipment(WmsEntity):
            """Shipment domain entity."""

            order_id: Annotated[
                str,
                m.Field(description="Associated order identifier"),
            ] = ""
            status: Annotated[str, m.Field(description="Shipment status")] = "pending"
            carrier: Annotated[
                str | None,
                m.Field(description="Shipping carrier name"),
            ] = None
            tracking_number: Annotated[
                str | None,
                m.Field(description="Shipment tracking number"),
            ] = None

        class PickingTask(WmsEntity):
            """Picking task domain entity."""

            wave_id: Annotated[str, m.Field(description="Wave identifier")] = ""
            status: Annotated[str, m.Field(description="Task status")] = "pending"
            items: Annotated[
                Sequence[t.ContainerValueMapping],
                m.Field(description="Task items"),
            ] = m.Field(default_factory=lambda: list[t.ContainerValueMapping]())

        class Location(WmsEntity):
            """Location domain entity."""

            aisle: Annotated[str, m.Field(description="Aisle identifier")] = ""
            shelf: Annotated[str, m.Field(description="Shelf identifier")] = ""
            bin_: Annotated[str, m.Field(description="Bin identifier")] = ""
            zone: Annotated[str, m.Field(description="Zone identifier")] = ""

        # =====================================================================
        # VALUE OBJECTS - Immutable domain values
        # =====================================================================

        class WarehouseLocation(m.BaseModel):
            """Warehouse location value object."""

            model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")

            aisle: Annotated[str, m.Field(description="Aisle identifier")]
            shelf: Annotated[str, m.Field(description="Shelf identifier")]
            bin_: Annotated[str, m.Field(description="Bin identifier")]
            zone: Annotated[str, m.Field(description="Zone identifier")] = ""

            @property
            def full_location(self) -> str:
                """Get full location string."""
                return f"{self.zone}-{self.aisle}-{self.shelf}-{self.bin_}"

        class ApiCredentials(m.BaseModel):
            """API credentials value object."""

            model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")

            username: Annotated[str, m.Field(description="API username")]
            password: Annotated[str | None, m.Field(description="API password")] = None
            token: Annotated[str | None, m.Field(description="API token")] = None

        # =====================================================================
        # AGGREGATE ROOTS - Consistency boundaries
        # =====================================================================

        class WarehouseAggregate(m.AggregateRoot):
            """Warehouse aggregate root."""

            id: Annotated[str, m.Field(description="Warehouse identifier")]
            name: Annotated[str, m.Field(description="Warehouse name")]
            locations: Annotated[
                Sequence[FlextOracleWmsModels.OracleWms.WarehouseLocation],
                m.Field(description="Warehouse locations"),
            ] = m.Field(
                default_factory=lambda: list[
                    FlextOracleWmsModels.OracleWms.WarehouseLocation
                ]()
            )
            inventory: Annotated[
                MutableSequence[FlextOracleWmsModels.OracleWms.InventoryItem],
                m.Field(description="Warehouse inventory items"),
            ] = m.Field(
                default_factory=lambda: list[
                    FlextOracleWmsModels.OracleWms.InventoryItem
                ]()
            )

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


__all__: list[str] = ["FlextOracleWmsModels"]

m = FlextOracleWmsModels
