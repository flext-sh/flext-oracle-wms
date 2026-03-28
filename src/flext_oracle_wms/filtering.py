"""FLEXT Oracle WMS Filtering module -- backward-compat re-export.

All logic moved to _utilities/filtering.py. Import via u.OracleWms.Filtering or this shim.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_oracle_wms._utilities.filtering import (
    FlextOracleWmsDataValidationError,
    FlextOracleWmsFilterOperator,
    FlextOracleWmsOperatorFilter,
    FlextOracleWmsUtilitiesFiltering,
)

FlextOracleWmsFilter = FlextOracleWmsUtilitiesFiltering.Filter

__all__ = [
    "FlextOracleWmsDataValidationError",
    "FlextOracleWmsFilter",
    "FlextOracleWmsFilterOperator",
    "FlextOracleWmsOperatorFilter",
]
