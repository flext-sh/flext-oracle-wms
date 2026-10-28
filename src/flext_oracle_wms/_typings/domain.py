"""Oracle WMS filter type alias declarations.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_api import FlextApiTypes

if TYPE_CHECKING:
    from flext_oracle_wms import m


class FlextOracleWmsTypesDomain:
    """Oracle WMS filter aliases composed into ``t.OracleWms``."""

    type FilterScalar = FlextApiTypes.Scalar | None
    type FilterList = FlextApiTypes.Sequence[FilterScalar]
    type FilterEntry = (
        FilterScalar | FilterList | m.OracleWms.FlextOracleWmsOperatorFilter
    )
    type FilterRecordValue = (
        FilterScalar
        | FilterList
        | FlextApiTypes.Mapping[
            str,
            FilterScalar
            | FilterList
            | FlextApiTypes.Mapping[
                str,
                FilterScalar | FilterList,
            ],
        ]
    )
    type FilterRecord = FlextApiTypes.Mapping[
        str,
        FilterScalar
        | FilterList
        | FlextApiTypes.Mapping[
            str,
            FilterScalar | FilterList,
        ],
    ]
    # Same recursive union as ``FilterRecordValue`` — one owner defines the
    # filter-value shape; this name re-exports it.
    type NestedFilterValue = FilterRecordValue


__all__: list[str] = ["FlextOracleWmsTypesDomain"]
