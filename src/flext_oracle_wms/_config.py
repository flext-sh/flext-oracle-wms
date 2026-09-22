"""FlextOracleWmsConfig — frozen, validated config singleton (ADR-005 / cosmos pattern).

Every ``config/*.yaml`` file is auto-discovered and deep-merged at first
``fetch_global`` call (model-less, ``extra=allow`` at the FlextConfig base). The
flat YAML is then validated into the pure-Pydantic ``_models.config`` shapes and
exposed as typed domain objects under ``config.oracle_wms.<domain>`` — never a
model-less dict subscript.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, Self

from flext_core import FlextConfig, FlextSettings

from ._constants.values import FlextOracleWmsConstantsValues
from ._models.config import FlextOracleWmsConfigModels

if TYPE_CHECKING:
    # NOTE (multi-agent): config-scaffold — accessor typed by PROTOCOL (p), never
    # the model class; the protocol module enters under TYPE_CHECKING only.
    from ._protocols.config import FlextOracleWmsProtocolsConfig


class FlextOracleWmsConfig(
    FlextSettings, FlextConfig, FlextOracleWmsConstantsValues.Config
):
    """OracleWms config auto-loaded from ``config/*.yaml`` and validated via models.

    MRO carries ``FlextSettings`` FIRST (ENFORCE-042); the class stays a frozen,
    YAML-validated config singleton.
    """

    # ENFORCE-042 namespace-holder contract: ``FlextSettings`` contributes
    # namespacing only — instance machinery stays plain object semantics so the
    # settings singleton ``__new__`` cannot leak into the config singleton.
    # The inherited pydantic ``__init__`` still runs the frozen, YAML-validated
    # construction, and the inherited pydantic ``__setattr__`` keeps the frozen
    # guard.
    def __new__(cls, *args: object, **kwargs: object) -> Self:
        _ = args, kwargs
        return object.__new__(cls)

    __eq__ = object.__eq__

    __hash__ = object.__hash__

    # NOTE (multi-agent): config-scaffold — ``CONFIG_DIR`` (the packaged
    # config-dir name, ``c.CONFIG_DIR_NAME``) is owned by
    # ``flext_oracle_wms._constants`` (``FlextOracleWmsConstantsValues.Config``)
    # and inherited above; ``FlextConfig._config_dir()`` anchors the YAML SSOT
    # to the packaged ``config/`` regardless of the caller's CWD.

    @cached_property
    def oracle_wms(self) -> FlextOracleWmsProtocolsConfig.Config:
        """Validated ``OracleWms`` config domains from the model-less YAML."""
        return FlextOracleWmsConfigModels.Root.model_validate(
            dict(self.model_extra or {})
        )


config: FlextOracleWmsConfig = FlextOracleWmsConfig.fetch_global()
"""Pre-instantiated frozen config singleton — ``from flext_oracle_wms import config``."""

__all__: list[str] = ["FlextOracleWmsConfig", "config"]
