"""FLEXT Oracle WMS Types - composition patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from flext_core import FlextTypes, t as _core_t

from flext_oracle_wms.constants import c


class FlextOracleWmsTypes(FlextTypes):
    """Oracle WMS types with composition.

    Uses Python 3.13+ syntax, reduces declarations through patterns.
    One class per module following SOLID principles.
    """

    class OracleWms:
        """Oracle WMS-specific project types."""

        type ProjectType = c.ProjectType
        type WmsProjectConfig = Mapping[str, FlextTypes.ContainerValue]
        type WarehouseConfig = Mapping[str, t.Scalar | t.StrSequence]
        type InventoryConfig = Mapping[
            str,
            bool | str | Mapping[str, FlextTypes.ContainerValue],
        ]

    type WmsConfig = Mapping[
        str,
        t.Scalar | Mapping[str, FlextTypes.ContainerValue],
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
        type FilterScalar = FlextTypes.Scalar | None
        type FilterList = Sequence[FlextOracleWmsTypes.Core.FilterScalar]
        type FilterRecordValue = (
            FlextOracleWmsTypes.Core.FilterScalar
            | FlextOracleWmsTypes.Core.FilterList
            | Mapping[
                str,
                FlextOracleWmsTypes.Core.FilterScalar
                | FlextOracleWmsTypes.Core.FilterList
                | Mapping[
                    str,
                    FlextOracleWmsTypes.Core.FilterScalar
                    | FlextOracleWmsTypes.Core.FilterList,
                ],
            ]
        )
        type FilterRecord = Mapping[
            str,
            FlextOracleWmsTypes.Core.FilterScalar
            | FlextOracleWmsTypes.Core.FilterList
            | Mapping[
                str,
                FlextOracleWmsTypes.Core.FilterScalar
                | FlextOracleWmsTypes.Core.FilterList,
            ],
        ]
        type NestedFilterValue = (
            FlextOracleWmsTypes.Core.FilterScalar
            | FlextOracleWmsTypes.Core.FilterList
            | Mapping[
                str,
                FlextOracleWmsTypes.Core.FilterScalar
                | FlextOracleWmsTypes.Core.FilterList
                | Mapping[
                    str,
                    FlextOracleWmsTypes.Core.FilterScalar
                    | FlextOracleWmsTypes.Core.FilterList,
                ],
            ]
        )
        type HttpJsonObject = Mapping[str, _core_t.ContainerValue]
        type FilterEntry = (
            FlextOracleWmsTypes.Core.FilterScalar | FlextOracleWmsTypes.Core.FilterList
        )


type HttpJsonObject = Mapping[str, _core_t.ContainerValue]

t = FlextOracleWmsTypes
__all__ = ["FlextOracleWmsTypes", "t"]
