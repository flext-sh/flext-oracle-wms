# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Oracle Wms. Typings package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_oracle_wms._typings.domain import (
        FilterEntry,
        FilterList,
        FilterRecord,
        FilterRecordValue,
        FilterScalar,
        NestedFilterValue,
    )


__all__: tuple[str, ...] = (
    "FilterEntry",
    "FilterList",
    "FilterRecord",
    "FilterRecordValue",
    "FilterScalar",
    "NestedFilterValue",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FilterEntry": ".domain",
        "FilterList": ".domain",
        "FilterRecord": ".domain",
        "FilterRecordValue": ".domain",
        "FilterScalar": ".domain",
        "NestedFilterValue": ".domain",
    }),
    public_exports=__all__,
)
