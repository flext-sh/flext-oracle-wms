"""FLEXT Oracle WMS Types - composition patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Mapping,
    Sequence,
)
from typing import Annotated, Literal

from flext_api import m, t, u

from flext_oracle_wms import c


class FlextOracleWmsTypes(t):
    """Oracle WMS types with composition.

    Uses Python 3.13+ syntax, reduces declarations through patterns.
    One class per module following SOLID principles.
    """

    class OracleWms:
        """Oracle WMS-specific project types."""

        FLOAT_ADAPTER: m.TypeAdapter[float] = m.TypeAdapter(float)
        CONTAINER_VALUE_MAPPING_ADAPTER: m.TypeAdapter[t.JsonMapping] = m.TypeAdapter(
            t.JsonMapping
        )

        # =========================================================================
        # TYPE ALIASES - Advanced composition for minimal declarations
        # =========================================================================

        type TRecord = t.JsonMapping
        type TRecordBatch = Sequence[t.JsonMapping]
        type TSchema = Mapping[str, t.JsonMapping]
        type TApiResponse = t.JsonMapping
        type TApiVersion = Literal["v2", "v1"]
        type TEntityId = Annotated[
            str, m.StringConstraints(min_length=1, max_length=100)
        ]
        type TEntityName = Annotated[
            str,
            m.StringConstraints(min_length=1, max_length=50, pattern=r"^[a-z0-9_]+$"),
        ]
        type TFilterValue = t.Scalar | None
        type TFilters = Mapping[str, t.Scalar | None]
        type TTimeout = Annotated[int, u.Field(ge=1, le=300)]

        type ProjectType = c.OracleWms.ProjectType
        type WmsProjectConfig = t.JsonMapping
        type WarehouseConfig = Mapping[str, t.Scalar | t.StrSequence]
        type InventoryConfig = Mapping[
            str,
            bool | str | t.JsonMapping,
        ]

        type WmsConfig = Mapping[
            str,
            t.Scalar | t.JsonMapping,
        ]
        type WmsEntity = Mapping[
            str,
            t.JsonValue | t.JsonMapping,
        ]
        type WmsRecord = t.JsonMapping
        type WmsRecords = Sequence[t.JsonMapping]

        class Core:
            """Core convenience type aliases for common patterns.

            Provides commonly used type aliases for consistency across the codebase.
            These are simple aliases but are used extensively, so provided for convenience.
            Access parent core types via inheritance from FlextOracleWmsTypes.
            """

            type Dict = t.JsonMapping
            "Type alias for generic dictionary (attribute name to value mapping)."
            type FilterScalar = t.Scalar | None
            type FilterList = Sequence[FlextOracleWmsTypes.OracleWms.Core.FilterScalar]
            type FilterRecordValue = (
                FlextOracleWmsTypes.OracleWms.Core.FilterScalar
                | FlextOracleWmsTypes.OracleWms.Core.FilterList
                | Mapping[
                    str,
                    FlextOracleWmsTypes.OracleWms.Core.FilterScalar
                    | FlextOracleWmsTypes.OracleWms.Core.FilterList
                    | Mapping[
                        str,
                        FlextOracleWmsTypes.OracleWms.Core.FilterScalar
                        | FlextOracleWmsTypes.OracleWms.Core.FilterList,
                    ],
                ]
            )
            type FilterRecord = Mapping[
                str,
                FlextOracleWmsTypes.OracleWms.Core.FilterScalar
                | FlextOracleWmsTypes.OracleWms.Core.FilterList
                | Mapping[
                    str,
                    FlextOracleWmsTypes.OracleWms.Core.FilterScalar
                    | FlextOracleWmsTypes.OracleWms.Core.FilterList,
                ],
            ]
            type NestedFilterValue = (
                FlextOracleWmsTypes.OracleWms.Core.FilterScalar
                | FlextOracleWmsTypes.OracleWms.Core.FilterList
                | Mapping[
                    str,
                    FlextOracleWmsTypes.OracleWms.Core.FilterScalar
                    | FlextOracleWmsTypes.OracleWms.Core.FilterList
                    | Mapping[
                        str,
                        FlextOracleWmsTypes.OracleWms.Core.FilterScalar
                        | FlextOracleWmsTypes.OracleWms.Core.FilterList,
                    ],
                ]
            )
            type HttpJsonObject = t.JsonMapping
            type FilterEntry = (
                FlextOracleWmsTypes.OracleWms.Core.FilterScalar
                | FlextOracleWmsTypes.OracleWms.Core.FilterList
            )


t = FlextOracleWmsTypes

__all__: list[str] = ["FlextOracleWmsTypes", "t"]
