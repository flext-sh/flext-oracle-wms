"""Oracle WMS discovery and service protocol contracts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING, Protocol, runtime_checkable

from flext_api import FlextApiProtocols

from flext_oracle_wms.typings import t

if TYPE_CHECKING:
    pass


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
    class FlextOracleWmsOperatorFilter(FlextApiProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        operator: str
        value: t.OracleWms.FilterScalar | t.OracleWms.FilterList

    @runtime_checkable
    class EnvironmentConfig(FlextApiProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        name: str
        base_url: str
        timeout: int
        retry_attempts: int

    @runtime_checkable
    class Entity(FlextApiProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        name: str
        endpoint: str
        description: str | None
        primary_key: str | None
        replication_key: str | None
        supports_incremental: bool

    @runtime_checkable
    class ApiEndpoint(FlextApiProtocols.BaseModel, Protocol):
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
    class AuthSettings(FlextApiProtocols.BaseModel, Protocol):
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
    class EntitiesResponse(FlextApiProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        entities: Sequence[str]

    @runtime_checkable
    class ApiCategoryResponse(FlextApiProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        apis: Sequence[Mapping[str, str]]

    @runtime_checkable
    class EntityDataResponse(FlextApiProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        data: Sequence[Mapping[str, str]]

    @runtime_checkable
    class WmsEntity(FlextApiProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        id: str
        name: str
        created_at: str | None
        updated_at: str | None

    @runtime_checkable
    class InventoryItem(WmsEntity, Protocol):
        """Structural data contract projected from the owning model."""

        sku: str
        quantity: t.NonNegativeInt
        location_id: str
        status: str

    @runtime_checkable
    class Shipment(WmsEntity, Protocol):
        """Structural data contract projected from the owning model."""

        order_id: str
        status: str
        carrier: str | None
        tracking_number: str | None

    @runtime_checkable
    class Location(WmsEntity, Protocol):
        """Structural data contract projected from the owning model."""

        aisle: str
        shelf: str
        bin_: str
        zone: str


__all__: list[str] = ["FlextOracleWmsProtocolsDomain"]
