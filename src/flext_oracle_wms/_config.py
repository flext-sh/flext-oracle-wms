"""FlextOracleWmsConfig — frozen config singleton for flext-oracle-wms (ADR-005 §7).

Model-less: business rules live in ``config/*.yaml`` under the ``OracleWms:`` key and
are exposed through the open ``config.OracleWms`` namespace (``extra="allow"``), with
no per-domain model. Access is ``config.OracleWms.<domain>[<key>...]``.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from flext_cli import FlextCliConfig


class _OracleWmsNamespace(BaseModel):
    """Open, frozen namespace exposing every ``config/*.yaml`` domain model-less."""

    model_config = ConfigDict(extra="allow", frozen=True)


class FlextOracleWmsConfig(FlextCliConfig):
    """OracleWms config auto-loaded model-less from ``config/*.yaml``."""

    OracleWms: _OracleWmsNamespace = _OracleWmsNamespace()


config: FlextOracleWmsConfig = FlextOracleWmsConfig.fetch_global()
"""Pre-instantiated frozen config singleton — ``from flext_oracle_wms import config``."""

__all__: list[str] = ["FlextOracleWmsConfig", "config"]
