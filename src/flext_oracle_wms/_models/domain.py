"""Generic WMS domain models for the OracleWms namespace.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Annotated, ClassVar

from flext_api import FlextApiModels, m

from flext_oracle_wms import c, t
from flext_oracle_wms._models.config import FlextModelsOracleWmsConfig


class FlextModelsOracleWmsDomain:
    """Oracle WMS domain models composed into ``m.OracleWms``."""

    class FlextOracleWmsOperatorFilter(FlextApiModels.BaseModel):
        """Operator filter model for WMS filtering operations."""

        operator: str
        value: t.OracleWms.FilterScalar | t.OracleWms.FilterList

    class EnvironmentConfig(FlextApiModels.BaseModel):
        """Oracle WMS environment configuration."""

        model_config: ClassVar[FlextApiModels.ConfigDict] = FlextApiModels.ConfigDict(
            extra="forbid",
            validate_assignment=True,
        )

        name: str = m.Field(description="Environment display name")
        base_url: str = m.Field(description="Oracle WMS base URL")
        timeout: int = m.Field(ge=1, description="Request timeout in seconds")
        retry_attempts: int = m.Field(ge=0, description="Retry attempts")

    class Entity(FlextApiModels.BaseModel):
        """Oracle WMS entity definition."""

        model_config: ClassVar[FlextApiModels.ConfigDict] = FlextApiModels.ConfigDict(
            extra="forbid"
        )

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
            m.Field(description="Whether entity supports incremental sync"),
        ] = False

        @m.field_validator("endpoint")
        @classmethod
        def _validate_endpoint_starts_with_slash(cls, v: str) -> str:
            if not v.startswith("/"):
                msg = "Endpoint must start with '/'"
                raise ValueError(msg)
            return v

    class ApiEndpoint(FlextModelsOracleWmsConfig.ApiEndpoint):
        """Typed Oracle WMS API endpoint definition (config owner, specialized).

        Extends the ``_models.config`` owner so the facade namespace
        overrides it covariantly (a valid subtype), and adds the domain
        validation (non-empty identifiers) and the documented defaults.
        """

        name: Annotated[str, m.Field(min_length=1)]
        method: Annotated[str, m.Field(min_length=1)]
        path: Annotated[str, m.Field(min_length=1)]
        version: Annotated[str, m.Field(min_length=1)]
        category: Annotated[str, m.Field(min_length=1)]
        description: str = ""
        since_version: str = c.OracleWms.WMS_API_BASELINE_VERSION

    class AuthSettings(FlextApiModels.BaseModel):
        """Authentication configuration for Oracle WMS flows."""

        method: str = c.OracleWms.OracleWMSAuthMethod.BASIC
        username: str | None = None
        password: str | None = None
        oauth2_client_id: str | None = None
        oauth2_client_secret: str | None = None
        oauth2_scope: str = "wms.read wms.write"
        token_refresh_threshold: t.PositiveInt = 300

        # return_type= kwarg dropped: it hit computed_field's kwargs-only
        # overload, which flext-core's `staticmethod(computed_field)` wrap
        # does not expose to pyrefly (flext-1wjg1.16 fleet defect); the
        # bare form already infers the type from the property annotation.
        @m.computed_field
        @property
        def normalized_method(self) -> str:
            """The auth method in canonical lowercase form."""
            return self.method.strip().lower()

    class EntitiesResponse(FlextApiModels.BaseModel):
        """Oracle WMS entities list response."""

        model_config: ClassVar[FlextApiModels.ConfigDict] = FlextApiModels.ConfigDict(
            extra="ignore"
        )

        entities: Sequence[str] = m.Field(default_factory=tuple)

    class ApiCategoryResponse(FlextApiModels.BaseModel):
        """Oracle WMS API category response."""

        model_config: ClassVar[FlextApiModels.ConfigDict] = FlextApiModels.ConfigDict(
            extra="ignore"
        )

        apis: Sequence[Mapping[str, str]] = m.Field(default_factory=tuple)

    class EntityDataResponse(FlextApiModels.BaseModel):
        """Oracle WMS entity data response."""

        model_config: ClassVar[FlextApiModels.ConfigDict] = FlextApiModels.ConfigDict(
            extra="ignore"
        )

        data: Sequence[Mapping[str, str]] = m.Field(default_factory=tuple)

    # =====================================================================
    # DOMAIN ENTITIES - Composed DDD patterns
    # =====================================================================
    class WmsEntity(FlextApiModels.BaseModel):
        """Base WMS entity with identity."""

        model_config: ClassVar[FlextApiModels.ConfigDict] = FlextApiModels.ConfigDict(
            extra="forbid"
        )

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

    class Location(WmsEntity):
        """Location domain entity."""

        aisle: Annotated[str, m.Field(description="Aisle identifier")] = ""
        shelf: Annotated[str, m.Field(description="Shelf identifier")] = ""
        bin_: Annotated[str, m.Field(description="Bin identifier")] = ""
        zone: Annotated[str, m.Field(description="Zone identifier")] = ""


__all__: list[str] = ["FlextModelsOracleWmsDomain"]
