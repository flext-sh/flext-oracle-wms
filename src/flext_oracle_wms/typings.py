"""FLEXT Oracle WMS Types - composition patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Annotated, Literal

from flext_core import FlextTypes
from pydantic import Field, StringConstraints

from flext_oracle_wms import c


class FlextOracleWmsTypes(FlextTypes):
    """Oracle WMS types with composition.

    Uses Python 3.13+ syntax, reduces declarations through patterns.
    One class per module following SOLID principles.
    """

    class OracleWms:
        """Oracle WMS-specific project types."""

        # =========================================================================
        # TYPE ALIASES - Advanced composition for minimal declarations
        # =========================================================================

        type TRecord = Mapping[str, FlextTypes.ContainerValue]
        type TRecordBatch = Sequence[Mapping[str, FlextTypes.ContainerValue]]
        type TSchema = Mapping[str, Mapping[str, FlextTypes.ContainerValue]]
        type TApiResponse = Mapping[str, FlextTypes.ContainerValue]
        type TApiVersion = Literal["v2", "v1"]
        type TEntityId = Annotated[str, StringConstraints(min_length=1, max_length=100)]
        type TEntityName = Annotated[
            str,
            StringConstraints(min_length=1, max_length=50, pattern=r"^[a-z0-9_]+$"),
        ]
        type TFilterValue = FlextTypes.OptionalScalar
        type TFilters = Mapping[str, FlextTypes.OptionalScalar]
        type TPaginationInfo = Mapping[str, int]
        type TTimeout = Annotated[int, Field(ge=1, le=300)]

        type ProjectType = c.OracleWms.ProjectType
        type WmsProjectConfig = Mapping[str, FlextTypes.ContainerValue]
        type WarehouseConfig = Mapping[str, FlextTypes.Scalar | FlextTypes.StrSequence]
        type InventoryConfig = Mapping[
            str,
            bool | str | Mapping[str, FlextTypes.ContainerValue],
        ]

        type WmsConfig = Mapping[
            str,
            FlextTypes.Scalar | Mapping[str, FlextTypes.ContainerValue],
        ]
        type WmsEntity = Mapping[
            str,
            FlextTypes.ContainerValue | Mapping[str, FlextTypes.ContainerValue],
        ]
        type WmsRecord = Mapping[str, FlextTypes.ContainerValue]
        type WmsRecords = Sequence[Mapping[str, FlextTypes.ContainerValue]]

        class Core:
            """Core convenience type aliases for common patterns.

            Provides commonly used type aliases for consistency across the codebase.
            These are simple aliases but are used extensively, so provided for convenience.
            Access parent core types via inheritance from FlextOracleWmsTypes.
            """

            type Dict = Mapping[str, FlextTypes.ContainerValue]
            "Type alias for generic dictionary (attribute name to value mapping)."
            type FilterScalar = FlextTypes.OptionalScalar
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
            type HttpJsonObject = Mapping[str, FlextTypes.ContainerValue]
            type FilterEntry = (
                FlextOracleWmsTypes.OracleWms.Core.FilterScalar
                | FlextOracleWmsTypes.OracleWms.Core.FilterList
            )


t = FlextOracleWmsTypes
__all__ = ["FlextOracleWmsTypes", "t"]
