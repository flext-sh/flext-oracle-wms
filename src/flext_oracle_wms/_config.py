"""FlextOracleWmsConfig — frozen, validated config singleton (ADR-005 / cosmos pattern).

Every ``config/*.yaml`` file is auto-discovered and deep-merged at first
``fetch_global`` call. Each root-level YAML domain is a declared typed field
validated once into the pure-Pydantic ``_models.config`` shapes and exposed as
``config.<domain>`` — never a model-less dict subscript.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Annotated, Self

from flext_cli import FlextCliConfig
from flext_core import m, t

from flext_oracle_wms._models.config import FlextOracleWmsConfigModels


class FlextOracleWmsConfig(FlextCliConfig):
    """OracleWms config auto-loaded from ``config/*.yaml`` and validated via models.

    The fleet-converged config inherits only the declared frozen config
    capability base (``config_bases`` precedence: meltano -> cli -> core); the
    adjustable runtime settings keep their own independent lifecycle.
    """

    # Instance machinery stays plain object semantics so no upstream singleton
    # ``__new__`` leaks into the config singleton; the inherited pydantic
    # ``__init__`` still runs the frozen, YAML-validated construction and the
    # inherited pydantic ``__setattr__`` keeps the frozen guard.
    def __new__(cls, *args: t.JsonValue, **kwargs: t.JsonValue) -> Self:
        _ = args, kwargs
        return object.__new__(cls)

    # LSP requires ``__eq__``'s parameter to accept every object; the
    # ``ban-broad-annotation`` dunder carve-out does not reach typed parameters,
    # so this is the scoped admission of that tooling conflict (the only correct
    # annotation for an equality operand). ``__new__`` above uses ``t.JsonValue``.
    def __eq__(self, other: object) -> bool:  # ast-grep-ignore: ban-broad-annotation
        """Identity equality per the frozen-config singleton contract.

        Returns:
            The resulting ``bool``.

        """
        return object.__eq__(self, other)

    def __hash__(self) -> int:
        """Identity hash per the frozen-config singleton contract.

        Returns:
            The resulting ``int``.

        """
        return object.__hash__(self)

    # NOTE (multi-agent): config-scaffold — the packaged ``config/`` dir name
    # is owned by ``flext_core`` (``CONFIG_DIR_NAME``); ``FlextConfig`` anchors
    # the YAML SSOT to the packaged ``config/`` regardless of the caller's CWD.

    http: Annotated[
        FlextOracleWmsConfigModels.Http,
        m.Field(description="HTTP response-classification thresholds."),
    ]
    api: Annotated[
        FlextOracleWmsConfigModels.Api,
        m.Field(description="Runtime API connection defaults."),
    ]
    processing: Annotated[
        FlextOracleWmsConfigModels.Processing,
        m.Field(description="Batch, page and schema processing limits."),
    ]
    filtering: Annotated[
        FlextOracleWmsConfigModels.Filtering,
        m.Field(description="Query-filter construction limits."),
    ]
    entities: Annotated[
        FlextOracleWmsConfigModels.Entities,
        m.Field(description="Entity-name validation rules."),
    ]
    auth: Annotated[
        FlextOracleWmsConfigModels.Auth,
        m.Field(description="OAuth2 authentication policy."),
    ]
    environments: Annotated[
        FlextOracleWmsConfigModels.Environments,
        m.Field(description="Named Oracle WMS environment base URLs."),
    ]
    api_endpoints: Annotated[
        t.MappingKV[str, FlextOracleWmsConfigModels.ApiEndpoint],
        m.Field(description="Oracle WMS API endpoint catalog by name."),
    ]

config: FlextOracleWmsConfig = FlextOracleWmsConfig.fetch_global()
"""Pre-instantiated frozen config singleton.

Exposed as ``from flext_oracle_wms import config``.
"""

__all__: list[str] = ["FlextOracleWmsConfig", "config"]
