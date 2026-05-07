"""FLEXT Oracle WMS Types.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_api import t


class FlextOracleWmsTypes(t):
    """Oracle WMS type definitions extending t via MRO."""

    class OracleWms:
        """Oracle WMS domain namespace (flat members per AGENTS.md §149)."""

        type FilterScalar = t.Scalar | None
        type FilterList = t.SequenceOf[FlextOracleWmsTypes.OracleWms.FilterScalar]
        type FilterRecordValue = (
            FlextOracleWmsTypes.OracleWms.FilterScalar
            | FlextOracleWmsTypes.OracleWms.FilterList
            | t.MappingKV[
                str,
                FlextOracleWmsTypes.OracleWms.FilterScalar
                | FlextOracleWmsTypes.OracleWms.FilterList
                | t.MappingKV[
                    str,
                    FlextOracleWmsTypes.OracleWms.FilterScalar
                    | FlextOracleWmsTypes.OracleWms.FilterList,
                ],
            ]
        )
        type FilterRecord = t.MappingKV[
            str,
            FlextOracleWmsTypes.OracleWms.FilterScalar
            | FlextOracleWmsTypes.OracleWms.FilterList
            | t.MappingKV[
                str,
                FlextOracleWmsTypes.OracleWms.FilterScalar
                | FlextOracleWmsTypes.OracleWms.FilterList,
            ],
        ]
        type NestedFilterValue = (
            FlextOracleWmsTypes.OracleWms.FilterScalar
            | FlextOracleWmsTypes.OracleWms.FilterList
            | t.MappingKV[
                str,
                FlextOracleWmsTypes.OracleWms.FilterScalar
                | FlextOracleWmsTypes.OracleWms.FilterList
                | t.MappingKV[
                    str,
                    FlextOracleWmsTypes.OracleWms.FilterScalar
                    | FlextOracleWmsTypes.OracleWms.FilterList,
                ],
            ]
        )


t = FlextOracleWmsTypes

__all__: list[str] = ["FlextOracleWmsTypes", "t"]
