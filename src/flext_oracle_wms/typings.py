# AUTO-GENERATED FILE — Regenerate with: make gen
"""FLEXT Oracle WMS Types.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_api import FlextApiTypes

from flext_oracle_wms._typings import FlextOracleWmsTypesDomain


class FlextOracleWmsTypes(FlextApiTypes):
    """Oracle WMS type definitions extending t via MRO."""

    class OracleWms(FlextOracleWmsTypesDomain):
        """Oracle WMS namespace composing the ``_typings`` family base."""


t = FlextOracleWmsTypes
__all__: list[str] = ["FlextOracleWmsTypes", "t"]
