"""FLEXT Oracle WMS Types.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_api import FlextApiTypes

from flext_oracle_wms._typings import domain as _domain_types


class FlextOracleWmsTypes(FlextApiTypes):
    """Oracle WMS type definitions extending t via MRO."""

    class OracleWms:
        """Oracle WMS domain namespace (flat members per AGENTS.md §149)."""

        FilterScalar = _domain_types.FilterScalar
        FilterList = _domain_types.FilterList
        FilterEntry = _domain_types.FilterEntry
        FilterRecordValue = _domain_types.FilterRecordValue
        FilterRecord = _domain_types.FilterRecord
        NestedFilterValue = _domain_types.NestedFilterValue


t = FlextOracleWmsTypes

__all__: list[str] = ["FlextOracleWmsTypes", "t"]
