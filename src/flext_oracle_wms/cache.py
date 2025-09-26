"""Backward-compatibility cache shim.

Provides legacy import path `flext_oracle_wms.cache` by re-exporting
cache components from the consolidated discovery module `wms_discovery`.


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from .wms_discovery import (
    FlextOracleWmsCacheConfig,
    FlextOracleWmsCacheEntry,
    FlextOracleWmsCacheManager,
    FlextOracleWmsCacheStats,
    # REMOVED: flext_oracle_wms_create_cache_manager - use FlextOracleWmsCacheManager directly
)

__all__ = [
    "FlextOracleWmsCacheConfig",
    "FlextOracleWmsCacheEntry",
    "FlextOracleWmsCacheManager",
    "FlextOracleWmsCacheStats",
    # REMOVED: flext_oracle_wms_create_cache_manager - use FlextOracleWmsCacheManager directly
]
