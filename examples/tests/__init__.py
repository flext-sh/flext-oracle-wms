# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Oracle Wms package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if _t.TYPE_CHECKING:
    from flext_oracle_wms.test_declarative_example import (
        FlextOracleWmsClient,
        load_env_config,
    )
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".test_declarative_example": (
            "FlextOracleWmsClient",
            "load_env_config",
        ),
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)

__all__ = [
    "FlextOracleWmsClient",
    "load_env_config",
]
