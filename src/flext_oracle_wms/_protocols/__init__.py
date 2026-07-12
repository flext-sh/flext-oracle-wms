"""Flext-oracle-wms internal protocol parts (composed by ``protocols.py`` via MRO).

Re-exports the structural config-domain protocol namespace so ``protocols.py``
composes ``p.OracleWms`` from a single package import. ``_protocols.config``
imports only ``typing`` — importable by ``c``/``t``/``p``/``m``/``u`` without a
cycle (foundation purity).

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_oracle_wms._protocols.config import FlextOracleWmsProtocolsConfig

__all__: list[str] = ["FlextOracleWmsProtocolsConfig"]
