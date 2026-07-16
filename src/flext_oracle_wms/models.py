"""FLEXT WMS Models - Generic WMS Domain Model.

domain-driven design with minimal declarations using composition.
Python 3.13+ syntax, one class per module, SOLID principles. Generic for any WMS.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Annotated, ClassVar

from flext_api import m, p, u

from flext_oracle_wms import c, p, t


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
            value: t.OracleWms.FilterScalar | t.OracleWms.FilterList

        class EnvironmentConfig(m.BaseModel):
            """Oracle WMS environment configuration."""

            model_config: ClassVar[p.ConfigDict] = m.ConfigDict(
                extra="forbid",
                validate_assignment=True,
            )

            name: str = u.Field(description="Environment display name")
            base_url: str = u.Field(description="Oracle WMS base URL")
            timeout: int = u.Field(ge=1, description="Request timeout in seconds")
            retry_attempts: int = u.Field(ge=0, description="Retry attempts")

        class Entity(m.BaseModel):
            """Oracle WMS entity definition."""

            model_config: ClassVar[p.ConfigDict] = m.ConfigDict(extra="forbid")

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

            @u.computed_field(return_type=str)
            @property
            def normalized_method(self) -> str:
                """The auth method in canonical lowercase form."""
                return self.method.strip().lower()

        class EntitiesResponse(m.BaseModel):
            """Oracle WMS entities list response."""

            model_config: ClassVar[p.ConfigDict] = m.ConfigDict(extra="ignore")

            entities: t.StrSequence = u.Field(default_factory=tuple)

        class ApiCategoryResponse(m.BaseModel):
            """Oracle WMS API category response."""

            model_config: ClassVar[p.ConfigDict] = m.ConfigDict(extra="ignore")

            apis: t.SequenceOf[t.StrMapping] = u.Field(default_factory=tuple)

        class EntityDataResponse(m.BaseModel):
            """Oracle WMS entity data response."""

            model_config: ClassVar[p.ConfigDict] = m.ConfigDict(extra="ignore")

            data: t.SequenceOf[t.StrMapping] = u.Field(default_factory=tuple)

        # =====================================================================
        # DOMAIN ENTITIES - Composed DDD patterns
        # =====================================================================

        class WmsEntity(m.BaseModel):
            """Base WMS entity with identity."""

            model_config: ClassVar[p.ConfigDict] = m.ConfigDict(extra="forbid")

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

        class Location(WmsEntity):
            """Location domain entity."""

            aisle: Annotated[str, u.Field(description="Aisle identifier")] = ""
            shelf: Annotated[str, u.Field(description="Shelf identifier")] = ""
            bin_: Annotated[str, u.Field(description="Bin identifier")] = ""
            zone: Annotated[str, u.Field(description="Zone identifier")] = ""

        # =====================================================================
        # VALUE OBJECTS - Immutable domain values
        # =====================================================================

        # =====================================================================
        # AGGREGATE ROOTS - Consistency boundaries
        # =====================================================================


m = FlextOracleWmsModels

__all__: list[str] = ["FlextOracleWmsModels", "m"]
