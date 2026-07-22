"""Flext-oracle-wms internal model parts (composed by ``models.py`` via MRO).

Re-exports the pure config-model part classes so ``models.py`` composes the
``OracleWms`` namespace from a single package import. ``_models.config`` stays
pure-Pydantic (no project/flext imports) — the firebreak that lets
``c``/``t``/``p``/``m``/``u`` import config shapes without a cycle.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_oracle_wms._models.config import FlextOracleWmsConfigModels

__all__: list[str] = ["FlextOracleWmsConfigModels"]
