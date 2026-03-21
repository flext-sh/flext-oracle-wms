"""FLEXT Oracle WMS Types - composition patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping

from flext_core import FlextTypes, t as _core_t
from pydantic import BaseModel

from flext_oracle_wms.constants import c


class FlextOracleWmsTypes(FlextTypes):
    """Oracle WMS types with composition.

    Uses Python 3.13+ syntax, reduces declarations through patterns.
    One class per module following SOLID principles.
    """

    class OracleWms:
        """Oracle WMS-specific project types."""

        type ProjectType = c.ProjectType
        type WmsProjectConfig = dict[str, FlextTypes.ContainerValue]
        type WarehouseConfig = dict[str, str | int | bool | list[str]]
        type InventoryConfig = dict[
            str,
            bool | str | dict[str, FlextTypes.ContainerValue],
        ]

    type WmsConfig = dict[
        str,
        str | int | bool | dict[str, FlextTypes.ContainerValue],
    ]
    type WmsEntity = dict[
        str,
        FlextTypes.ContainerValue | dict[str, FlextTypes.ContainerValue],
    ]
    type WmsRecord = dict[str, FlextTypes.ContainerValue]
    type WmsRecords = list[dict[str, FlextTypes.ContainerValue]]

    class Core:
        """Core convenience type aliases for common patterns.

        Provides commonly used type aliases for consistency across the codebase.
        These are simple aliases but are used extensively, so provided for convenience.
        Access parent core types via inheritance from FlextOracleWmsTypes.
        """

        type Dict = dict[str, FlextTypes.ContainerValue]
        "Type alias for generic dictionary (attribute name to value mapping)."
        type FilterScalar = FlextTypes.Scalar | None
        type FilterList = list[FlextOracleWmsTypes.Core.FilterScalar]
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


t = FlextOracleWmsTypes
__all__ = ["FlextOracleWmsTypes", "t"]


class OperatorFilter(BaseModel):
    operator: str
    value: FlextOracleWmsTypes.Core.FilterScalar | FlextOracleWmsTypes.Core.FilterList


type HttpJsonObject = dict[str, _core_t.ContainerValue]
