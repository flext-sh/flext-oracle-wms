"""Oracle WMS discovery and service protocol contracts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Protocol, runtime_checkable

from flext_api import FlextApiProtocols

if TYPE_CHECKING:
    from collections.abc import Mapping

    from flext_oracle_wms import t
    from flext_oracle_wms._typings import FlextOracleWmsTypesDomain


class FlextOracleWmsProtocolsDomain:
    """Oracle WMS domain protocol contracts composed into ``p.OracleWms``."""

    @runtime_checkable
    class EntityDiscoveryClient(Protocol):
        """Protocol for the entity discovery client used by the discovery."""

        def discover_entities(self) -> FlextApiProtocols.Result[Sequence[str]]:
            """Discover available entities.

            Returns:
                Result wrapping the discovered entity names.

            """
            ...

    @runtime_checkable
    class WmsService(FlextApiProtocols.Service[None], Protocol):
        """Unified WMS service protocol with operation dispatch."""

        def execute_wms_operation(
            self,
            operation: str,
            settings: t.JsonMapping,
            **params: t.Scalar,
        ) -> FlextApiProtocols.Result[t.JsonValue]:
            """Execute WMS operation with unified interface.

            Args:
                operation: Operation type (auth, discovery, inventory,
                    and so on).
                settings: Operation configuration.
                **params: Operation parameters.

            Returns:
                Result wrapping the operation output or an error.

            """
            ...

    @runtime_checkable
    class FlextOracleWmsOperatorFilter(FlextApiProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        operator: str

        @property
        def value(
            self,
        ) -> (
            FlextOracleWmsTypesDomain.FilterScalar
            | FlextOracleWmsTypesDomain.FilterList
        ):
            """Structural member projected from the owning model."""
            ...

    @runtime_checkable
    class EnvironmentConfig(FlextApiProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        name: str
        base_url: str
        timeout: int
        retry_attempts: int

    @runtime_checkable
    class Entity(FlextApiProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def name(self) -> str:
            """Entity name."""
            ...

        @property
        def endpoint(self) -> str:
            """API endpoint path."""
            ...

        @property
        def description(self) -> str | None:
            """Entity description."""
            ...

        @property
        def primary_key(self) -> str | None:
            """Primary key field."""
            ...

        @property
        def replication_key(self) -> str | None:
            """Replication key field."""
            ...

        @property
        def supports_incremental(self) -> bool:
            """Whether entity supports incremental sync."""
            ...

    @runtime_checkable
    class ApiEndpoint(FlextApiProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def name(self) -> str:
            """Structural member projected from the owning model."""
            ...

        @property
        def method(self) -> str:
            """Structural member projected from the owning model."""
            ...

        @property
        def path(self) -> str:
            """Structural member projected from the owning model."""
            ...

        @property
        def version(self) -> str:
            """Structural member projected from the owning model."""
            ...

        @property
        def category(self) -> str:
            """Structural member projected from the owning model."""
            ...

        @property
        def description(self) -> str:
            """Structural member projected from the owning model."""
            ...

        @property
        def since_version(self) -> str:
            """Structural member projected from the owning model."""
            ...

    @runtime_checkable
    class AuthSettings(FlextApiProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        method: str
        username: str | None
        password: str | None
        oauth2_client_id: str | None
        oauth2_client_secret: str | None
        oauth2_scope: str
        token_refresh_threshold: t.PositiveInt

        @property
        def normalized_method(self) -> str:
            """The auth method in canonical lowercase form."""
            ...

    @runtime_checkable
    class EntitiesResponse(FlextApiProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        entities: Sequence[str]

    @runtime_checkable
    class ApiCategoryResponse(FlextApiProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        apis: Sequence[Mapping[str, str]]

    @runtime_checkable
    class EntityDataResponse(FlextApiProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        data: Sequence[Mapping[str, str]]

    @runtime_checkable
    class WmsEntity(FlextApiProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def id(self) -> str:
            """Entity identifier."""
            ...

        @property
        def name(self) -> str:
            """Entity name."""
            ...

        @property
        def created_at(self) -> str | None:
            """Creation timestamp."""
            ...

        @property
        def updated_at(self) -> str | None:
            """Last update timestamp."""
            ...

    @runtime_checkable
    class InventoryItem(FlextApiProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def id(self) -> str:
            """Entity identifier."""
            ...

        @property
        def name(self) -> str:
            """Entity name."""
            ...

        @property
        def created_at(self) -> str | None:
            """Creation timestamp."""
            ...

        @property
        def updated_at(self) -> str | None:
            """Last update timestamp."""
            ...

        @property
        def sku(self) -> str:
            """Stock keeping unit."""
            ...

        @property
        def quantity(self) -> t.NonNegativeInt:
            """Item quantity."""
            ...

        @property
        def location_id(self) -> str:
            """Storage location identifier."""
            ...

        @property
        def status(self) -> str:
            """Item status."""
            ...

    @runtime_checkable
    class Shipment(FlextApiProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def id(self) -> str:
            """Entity identifier."""
            ...

        @property
        def name(self) -> str:
            """Entity name."""
            ...

        @property
        def created_at(self) -> str | None:
            """Creation timestamp."""
            ...

        @property
        def updated_at(self) -> str | None:
            """Last update timestamp."""
            ...

        @property
        def order_id(self) -> str:
            """Associated order identifier."""
            ...

        @property
        def status(self) -> str:
            """Shipment status."""
            ...

        @property
        def carrier(self) -> str | None:
            """Shipping carrier name."""
            ...

        @property
        def tracking_number(self) -> str | None:
            """Shipment tracking number."""
            ...

    @runtime_checkable
    class Location(FlextApiProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def id(self) -> str:
            """Entity identifier."""
            ...

        @property
        def name(self) -> str:
            """Entity name."""
            ...

        @property
        def created_at(self) -> str | None:
            """Creation timestamp."""
            ...

        @property
        def updated_at(self) -> str | None:
            """Last update timestamp."""
            ...

        @property
        def aisle(self) -> str:
            """Aisle identifier."""
            ...

        @property
        def shelf(self) -> str:
            """Shelf identifier."""
            ...

        @property
        def bin_(self) -> str:
            """Bin identifier."""
            ...

        @property
        def zone(self) -> str:
            """Zone identifier."""
            ...


__all__: list[str] = ["FlextOracleWmsProtocolsDomain"]
