"""Config-domain protocols part (composed into ``p.OracleWms`` via MRO).

Structural, field-level protocols for the validated config domains — never
model classes, never ``Any``/``object``. No runtime project imports; importable
by ``c``/``t``/``p``/``m``/``u`` without creating a cycle (foundation purity).

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Protocol, runtime_checkable


class FlextOracleWmsProtocolsConfig:
    """Config-domain protocol namespace (structural types; no project imports)."""

    @runtime_checkable
    class Http(Protocol):
        """Structural surface of the validated ``http`` config domain."""

        @property
        def bad_request_threshold(self) -> int: ...

    @runtime_checkable
    class Api(Protocol):
        """Structural surface of the validated ``api`` config domain."""

        @property
        def version_default(self) -> str: ...
        @property
        def timeout_default(self) -> int: ...
        @property
        def max_retries(self) -> int: ...
        @property
        def retry_delay(self) -> int: ...

    @runtime_checkable
    class Processing(Protocol):
        """Structural surface of the validated ``processing`` config domain."""

        @property
        def default_batch_size(self) -> int: ...
        @property
        def max_batch_size(self) -> int: ...
        @property
        def default_page_size(self) -> int: ...
        @property
        def max_schema_depth(self) -> int: ...

    @runtime_checkable
    class Filtering(Protocol):
        """Structural surface of the validated ``filtering`` config domain."""

        @property
        def max_filter_conditions(self) -> int: ...

    @runtime_checkable
    class Entities(Protocol):
        """Structural surface of the validated ``entities`` config domain."""

        @property
        def max_entity_name_length(self) -> int: ...

    @runtime_checkable
    class Auth(Protocol):
        """Structural surface of the validated ``auth`` config domain."""

        @property
        def oauth2_token_endpoint(self) -> str: ...
        @property
        def oauth2_scope_default(self) -> str: ...

    @runtime_checkable
    class Environments(Protocol):
        """Structural surface of the validated ``environments`` config domain."""

        @property
        def default(self) -> str: ...
        @property
        def test(self) -> str: ...
        @property
        def production(self) -> str: ...

    @runtime_checkable
    class ApiEndpoint(Protocol):
        """Structural surface of a validated Oracle WMS API endpoint."""

        @property
        def name(self) -> str: ...
        @property
        def method(self) -> str: ...
        @property
        def path(self) -> str: ...
        @property
        def version(self) -> str: ...
        @property
        def category(self) -> str: ...
        @property
        def description(self) -> str: ...
        @property
        def since_version(self) -> str: ...

    @runtime_checkable
    class Config(Protocol):
        """Structural surface of ``config.OracleWms`` (validated domains)."""

        @property
        def http(self) -> FlextOracleWmsProtocolsConfig.Http: ...
        @property
        def api(self) -> FlextOracleWmsProtocolsConfig.Api: ...
        @property
        def processing(self) -> FlextOracleWmsProtocolsConfig.Processing: ...
        @property
        def filtering(self) -> FlextOracleWmsProtocolsConfig.Filtering: ...
        @property
        def entities(self) -> FlextOracleWmsProtocolsConfig.Entities: ...
        @property
        def auth(self) -> FlextOracleWmsProtocolsConfig.Auth: ...
        @property
        def environments(self) -> FlextOracleWmsProtocolsConfig.Environments: ...
        @property
        def api_endpoints(
            self,
        ) -> Mapping[str, FlextOracleWmsProtocolsConfig.ApiEndpoint]: ...


__all__: list[str] = ["FlextOracleWmsProtocolsConfig"]
