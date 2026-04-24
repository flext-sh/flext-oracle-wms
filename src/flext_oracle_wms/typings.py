"""FLEXT Oracle WMS Types.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Mapping,
    Sequence,
)

from flext_api import m, t


class FlextOracleWmsTypes(t):
    """Oracle WMS type definitions extending t via MRO."""

    class OracleWms:
        """Oracle WMS domain namespace (flat members per AGENTS.md §149)."""

        FLOAT_ADAPTER: m.TypeAdapter[float] = m.TypeAdapter(float)
        CONTAINER_VALUE_MAPPING_ADAPTER: m.TypeAdapter[t.JsonMapping] = m.TypeAdapter(
            t.JsonMapping
        )

        type FilterScalar = t.Scalar | None
        type FilterList = Sequence[FlextOracleWmsTypes.OracleWms.FilterScalar]
        type FilterRecordValue = (
            FlextOracleWmsTypes.OracleWms.FilterScalar
            | FlextOracleWmsTypes.OracleWms.FilterList
            | Mapping[
                str,
                FlextOracleWmsTypes.OracleWms.FilterScalar
                | FlextOracleWmsTypes.OracleWms.FilterList
                | Mapping[
                    str,
                    FlextOracleWmsTypes.OracleWms.FilterScalar
                    | FlextOracleWmsTypes.OracleWms.FilterList,
                ],
            ]
        )
        type FilterRecord = Mapping[
            str,
            FlextOracleWmsTypes.OracleWms.FilterScalar
            | FlextOracleWmsTypes.OracleWms.FilterList
            | Mapping[
                str,
                FlextOracleWmsTypes.OracleWms.FilterScalar
                | FlextOracleWmsTypes.OracleWms.FilterList,
            ],
        ]
        type NestedFilterValue = (
            FlextOracleWmsTypes.OracleWms.FilterScalar
            | FlextOracleWmsTypes.OracleWms.FilterList
            | Mapping[
                str,
                FlextOracleWmsTypes.OracleWms.FilterScalar
                | FlextOracleWmsTypes.OracleWms.FilterList
                | Mapping[
                    str,
                    FlextOracleWmsTypes.OracleWms.FilterScalar
                    | FlextOracleWmsTypes.OracleWms.FilterList,
                ],
            ]
        )


t = FlextOracleWmsTypes

__all__: list[str] = ["FlextOracleWmsTypes", "t"]
