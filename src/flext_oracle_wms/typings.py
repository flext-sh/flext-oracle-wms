"""FLEXT Oracle WMS Types - composition patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Annotated, Literal

from flext_api import t
from pydantic import Field, StringConstraints, TypeAdapter

from flext_oracle_wms import c


class FlextOracleWmsTypes(t):
    """Oracle WMS types with composition.

    Uses Python 3.13+ syntax, reduces declarations through patterns.
    One class per module following SOLID principles.
    """

    class OracleWms:
        """Oracle WMS-specific project types."""

        FLOAT_ADAPTER: TypeAdapter[float] = TypeAdapter(float)
        CONTAINER_VALUE_MAPPING_ADAPTER: TypeAdapter[t.ContainerValueMapping] = (
            TypeAdapter(t.ContainerValueMapping)
        )

        # =========================================================================
        # TYPE ALIASES - Advanced composition for minimal declarations
        # =========================================================================

        type TRecord = t.ContainerValueMapping
        type TRecordBatch = Sequence[t.ContainerValueMapping]
        type TSchema = Mapping[str, t.ContainerValueMapping]
        type TApiResponse = t.ContainerValueMapping
        type TApiVersion = Literal["v2", "v1"]
        type TEntityId = Annotated[str, StringConstraints(min_length=1, max_length=100)]
        type TEntityName = Annotated[
            str,
            StringConstraints(min_length=1, max_length=50, pattern=r"^[a-z0-9_]+$"),
        ]
        type TFilterValue = t.OptionalScalar
        type TFilters = Mapping[str, t.OptionalScalar]
        type TTimeout = Annotated[int, Field(ge=1, le=300)]

        type ProjectType = c.OracleWms.ProjectType
        type WmsProjectConfig = t.ContainerValueMapping
        type WarehouseConfig = Mapping[str, t.Scalar | t.StrSequence]
        type InventoryConfig = Mapping[
            str,
            bool | str | t.ContainerValueMapping,
        ]

        type WmsConfig = Mapping[
            str,
            t.Scalar | t.ContainerValueMapping,
        ]
        type WmsEntity = Mapping[
            str,
            t.ContainerValue | t.ContainerValueMapping,
        ]
        type WmsRecord = t.ContainerValueMapping
        type WmsRecords = Sequence[t.ContainerValueMapping]

        class Core:
            """Core convenience type aliases for common patterns.

            Provides commonly used type aliases for consistency across the codebase.
            These are simple aliases but are used extensively, so provided for convenience.
            Access parent core types via inheritance from FlextOracleWmsTypes.
            """

            type Dict = t.ContainerValueMapping
            "Type alias for generic dictionary (attribute name to value mapping)."
            type FilterScalar = t.OptionalScalar
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
            type HttpJsonObject = t.ContainerValueMapping
            type FilterEntry = (
                FlextOracleWmsTypes.OracleWms.Core.FilterScalar
                | FlextOracleWmsTypes.OracleWms.Core.FilterList
            )


t = FlextOracleWmsTypes

__all__: list[str] = ["FlextOracleWmsTypes", "t"]
