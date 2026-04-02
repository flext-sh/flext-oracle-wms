"""FLEXT WMS Models - Generic WMS Domain Model.

domain-driven design with minimal declarations using composition.
Python 3.13+ syntax, one class per module, SOLID principles. Generic for any WMS.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, MutableSequence, Sequence
from typing import Annotated, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, field_validator

from flext_core import FlextModels, r
from flext_oracle_wms import FlextOracleWmsConstants as c, FlextOracleWmsTypes as t


class FlextOracleWmsModels(FlextModels):
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

        class FlextOracleWmsOperatorFilter(BaseModel):
            """Operator filter model for WMS filtering operations."""

            operator: str
            value: t.OracleWms.Core.FilterScalar | t.OracleWms.Core.FilterList

        class Entity(BaseModel):
            """Oracle WMS entity definition."""

            model_config: ClassVar[ConfigDict] = ConfigDict(extra="forbid")

            name: Annotated[str, Field(min_length=1, description="Entity name")]
            endpoint: Annotated[
                str,
                Field(min_length=1, description="API endpoint path"),
            ]
            description: Annotated[
                str | None,
                Field(description="Entity description"),
            ] = None
            primary_key: Annotated[
                str | None,
                Field(description="Primary key field"),
            ] = None
            replication_key: Annotated[
                str | None,
                Field(description="Replication key field"),
            ] = None
            supports_incremental: Annotated[
                bool,
                Field(
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

            def validate_entity(self) -> r[bool]:
                """Validate entity configuration."""
                if not self.name:
                    return r[bool].fail("Entity name is required")
                if len(self.name) > c.WmsEntities.MAX_ENTITY_NAME_LENGTH:
                    return r[bool].fail("Entity name is too long")
                if not self.endpoint:
                    return r[bool].fail("Entity endpoint is required")
                return r[bool].ok(True)

        class ApiResponse(BaseModel):
            """Oracle WMS API response model."""

            data: Annotated[
                t.ContainerValueMapping,
                Field(description="Response data"),
            ] = Field(default_factory=dict)
            status_code: Annotated[
                t.HttpStatusCode,
                Field(description="HTTP status code"),
            ] = 200
            success: Annotated[
                bool,
                Field(description="Whether request succeeded"),
            ] = True
            error_message: Annotated[
                str | None,
                Field(description="Error message if any"),
            ] = None

            def validate_response(self) -> r[bool]:
                """Validate response state."""
                if not self.success and not self.error_message:
                    return r[bool].fail("Failed response must include error message")
                return r[bool].ok(True)

        class ApiEndpoint(BaseModel):
            """Typed Oracle WMS API endpoint definition."""

            name: Annotated[str, Field(min_length=1)]
            method: Annotated[str, Field(min_length=1)]
            path: Annotated[str, Field(min_length=1)]
            version: Annotated[str, Field(min_length=1)]
            category: Annotated[str, Field(min_length=1)]
            description: str = ""
            since_version: str = "6.1"

        class AuthSettings(BaseModel):
            """Authentication configuration for Oracle WMS flows."""

            method: str = c.OracleWms.OracleWMSAuthMethod.BASIC
            username: str | None = None
            password: str | None = None
            oauth2_client_id: str | None = None
            oauth2_client_secret: str | None = None
            oauth2_scope: str = "wms.read wms.write"
            token_refresh_threshold: t.PositiveInt = 300

            def validate_business_rules(self) -> r[bool]:
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

        class EntitiesResponse(BaseModel):
            """Oracle WMS entities list response."""

            model_config: ClassVar[ConfigDict] = ConfigDict(extra="ignore")

            entities: t.StrSequence = Field(default_factory=list)

        class ApiCategoryResponse(BaseModel):
            """Oracle WMS API category response."""

            model_config: ClassVar[ConfigDict] = ConfigDict(extra="ignore")

            apis: Sequence[t.StrMapping] = Field(
                default_factory=lambda: list[t.StrMapping]()
            )

        class EntityDataResponse(BaseModel):
            """Oracle WMS entity data response."""

            model_config: ClassVar[ConfigDict] = ConfigDict(extra="ignore")

            data: Sequence[t.StrMapping] = Field(
                default_factory=lambda: list[t.StrMapping]()
            )

        # =====================================================================
        # DOMAIN ENTITIES - Composed DDD patterns
        # =====================================================================

        class WmsEntity(BaseModel):
            """Base WMS entity with identity."""

            model_config: ClassVar[ConfigDict] = ConfigDict(extra="forbid")

            id: Annotated[str, Field(description="Entity identifier")] = ""
            name: Annotated[str, Field(description="Entity name")] = ""
            created_at: Annotated[
                str | None,
                Field(description="Creation timestamp"),
            ] = None
            updated_at: Annotated[
                str | None,
                Field(description="Last update timestamp"),
            ] = None

        class InventoryItem(WmsEntity):
            """Inventory domain entity."""

            sku: Annotated[str, Field(description="Stock keeping unit")] = ""
            quantity: Annotated[
                t.NonNegativeInt,
                Field(description="Item quantity"),
            ] = 0
            location_id: Annotated[
                str,
                Field(description="Storage location identifier"),
            ] = ""
            status: Annotated[str, Field(description="Item status")] = "active"

        class Order(WmsEntity):
            """Order domain entity."""

            customer_id: Annotated[
                str,
                Field(description="Customer identifier"),
            ] = ""
            status: Annotated[str, Field(description="Order status")] = "pending"
            total_amount: Annotated[
                t.NonNegativeFloat,
                Field(description="Total order amount"),
            ] = 0.0
            items: Annotated[
                Sequence[t.ContainerValueMapping],
                Field(description="Order items"),
            ] = Field(default_factory=lambda: list[t.ContainerValueMapping]())

        class Shipment(WmsEntity):
            """Shipment domain entity."""

            order_id: Annotated[
                str,
                Field(description="Associated order identifier"),
            ] = ""
            status: Annotated[str, Field(description="Shipment status")] = "pending"
            carrier: Annotated[
                str | None,
                Field(description="Shipping carrier name"),
            ] = None
            tracking_number: Annotated[
                str | None,
                Field(description="Shipment tracking number"),
            ] = None

        class PickingTask(WmsEntity):
            """Picking task domain entity."""

            wave_id: Annotated[str, Field(description="Wave identifier")] = ""
            status: Annotated[str, Field(description="Task status")] = "pending"
            items: Annotated[
                Sequence[t.ContainerValueMapping],
                Field(description="Task items"),
            ] = Field(default_factory=lambda: list[t.ContainerValueMapping]())

        class Location(WmsEntity):
            """Location domain entity."""

            aisle: Annotated[str, Field(description="Aisle identifier")] = ""
            shelf: Annotated[str, Field(description="Shelf identifier")] = ""
            bin_: Annotated[str, Field(description="Bin identifier")] = ""
            zone: Annotated[str, Field(description="Zone identifier")] = ""

        # =====================================================================
        # VALUE OBJECTS - Immutable domain values
        # =====================================================================

        class WarehouseLocation(BaseModel):
            """Warehouse location value t.NormalizedValue."""

            model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")

            aisle: Annotated[str, Field(description="Aisle identifier")]
            shelf: Annotated[str, Field(description="Shelf identifier")]
            bin_: Annotated[str, Field(description="Bin identifier")]
            zone: Annotated[str, Field(description="Zone identifier")] = ""

            @property
            def full_location(self) -> str:
                """Get full location string."""
                return f"{self.zone}-{self.aisle}-{self.shelf}-{self.bin_}"

        class ApiCredentials(BaseModel):
            """API credentials value t.NormalizedValue."""

            model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")

            username: Annotated[str, Field(description="API username")]
            password: Annotated[str | None, Field(description="API password")] = None
            token: Annotated[str | None, Field(description="API token")] = None

        # =====================================================================
        # ENUMS - Aliases from constants.py (single source of truth)
        # =====================================================================

        EntityType: type[c.OracleWms.WmsEntityType] = c.OracleWms.WmsEntityType
        OperationStatus: type[c.OracleWms.WmsOperationStatus] = (
            c.OracleWms.WmsOperationStatus
        )

        # =====================================================================
        # AGGREGATE ROOTS - Consistency boundaries
        # =====================================================================

        class WarehouseAggregate(FlextModels.AggregateRoot):
            """Warehouse aggregate root."""

            id: str
            name: str
            locations: Sequence[FlextOracleWmsModels.OracleWms.WarehouseLocation] = (
                Field(
                    default_factory=lambda: list[
                        FlextOracleWmsModels.OracleWms.WarehouseLocation
                    ]()
                )
            )
            inventory: MutableSequence[FlextOracleWmsModels.OracleWms.InventoryItem] = (
                Field(
                    default_factory=lambda: list[
                        FlextOracleWmsModels.OracleWms.InventoryItem
                    ]()
                )
            )

            def add_inventory(
                self, item: FlextOracleWmsModels.OracleWms.InventoryItem
            ) -> r[bool]:
                """Add inventory to warehouse."""
                if any(i.sku == item.sku for i in self.inventory):
                    return r[bool].fail("SKU already exists")
                self.inventory.append(item)
                return r[bool].ok(True)

        # =========================================================================
        # TYPE ALIASES - Advanced composition for minimal declarations
        # =========================================================================

        type TRecord = t.ContainerValueMapping
        type TRecordBatch = Sequence[t.ContainerValueMapping]
        type TSchema = Mapping[str, t.ContainerValueMapping]
        type TApiResponse = t.ContainerValueMapping
        type TApiVersion = Literal["v2", "v1"]
        type TEntityId = Annotated[str, StringConstraints(min_length=1, max_length=100)]
        type TEntityName = Annotated[
            str,
            StringConstraints(min_length=1, max_length=50, pattern=r"^[a-z0-9_]+$"),
        ]
        type TFilterValue = t.Scalar | None
        type TFilters = Mapping[str, t.Scalar | None]
        type TTimeout = Annotated[int, Field(ge=1, le=300)]

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
        def validate_entity_name(name: str) -> r[str]:
            """Validate entity name using domain rules."""
            if (
                not name
                or len(name) > FlextOracleWmsModels.OracleWms.MAX_ENTITY_NAME_LENGTH
            ):
                return r[str].fail("Invalid entity name")
            return r[str].ok(name)


__all__ = ["FlextOracleWmsModels"]

m = FlextOracleWmsModels
