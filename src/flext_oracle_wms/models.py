# AUTO-GENERATED FILE — Regenerate with: make gen
"""FLEXT WMS Models - Generic WMS Domain Model.

domain-driven design with minimal declarations using composition.
Python 3.13+ syntax, one class per module, SOLID principles. Generic for any WMS.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_api import m

from flext_oracle_wms._models import (
    FlextOracleWmsConfigModels,
    FlextOracleWmsModelsDomain,
)


class FlextOracleWmsModels(m):
    """Generic WMS domain models with composition patterns.

    Single class per module following DDD, SOLID, and flext-core patterns.
    Uses Python 3.13+ syntax and AST-optimized declarations for minimal line count.
    Generic for any WMS system.
    """

    # =========================================================================
    # ORACLE WMS NAMESPACE - Domain-specific models
    # =========================================================================

    class OracleWms(FlextOracleWmsConfigModels, FlextOracleWmsModelsDomain):
        """Oracle WMS domain namespace -- m.OracleWms.*."""

        # =====================================================================
        # VALUE OBJECTS - Immutable domain values
        # =====================================================================

        # =====================================================================
        # AGGREGATE ROOTS - Consistency boundaries
        # =====================================================================


m = FlextOracleWmsModels
__all__: list[str] = ["FlextOracleWmsModels", "m"]
