"""FlextOracleWmsConfig — frozen, validated config singleton (ADR-005 / cosmos pattern).

Every ``config/*.yaml`` file is auto-discovered and deep-merged at first
``fetch_global`` call (model-less, ``extra=allow`` at the FlextConfig base). The
flat YAML is then validated into the pure-Pydantic ``_models.config`` shapes and
exposed as typed domain objects under ``config.OracleWms.<domain>`` — never a
model-less dict subscript.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from functools import cached_property
from pathlib import Path
from typing import TYPE_CHECKING, ClassVar

from flext_core import FlextConfig
from flext_oracle_wms._models.config import FlextOracleWmsConfigModels

# NOTE (multi-agent): config-scaffold — accessor typed by PROTOCOL (p), never
# the model class; the protocol module enters under TYPE_CHECKING only.

if TYPE_CHECKING:
    from flext_oracle_wms._protocols.config import FlextOracleWmsProtocolsConfig


class FlextOracleWmsConfig(FlextConfig):
    """OracleWms config auto-loaded from ``config/*.yaml`` and validated via models."""

    # NOTE (multi-agent): config-scaffold — anchored to the package dir so the YAML
    # SSOT loads regardless of the caller's CWD (library code must not depend on CWD).
    CONFIG_DIR: ClassVar[str] = str(Path(__file__).resolve().parent / "config")

    @cached_property
    def OracleWms(self) -> FlextOracleWmsProtocolsConfig.Config:
        """Validated ``OracleWms`` config domains from the model-less YAML."""
        return FlextOracleWmsConfigModels.Root.model_validate(
            dict(self.model_extra or {})
        )


config: FlextOracleWmsConfig = FlextOracleWmsConfig.fetch_global()
"""Pre-instantiated frozen config singleton — ``from flext_oracle_wms import config``."""

__all__: list[str] = ["FlextOracleWmsConfig", "config"]
