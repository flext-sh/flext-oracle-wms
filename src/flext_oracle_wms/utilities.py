"""FLEXT Oracle WMS Utilities - Domain-specific utilities extending FlextUtilities.

This module provides Oracle WMS-specific utility functions extending FlextUtilities
from flext-core. Uses advanced builder patterns and composition for clean code.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext import u as u_core


class FlextOracleWmsUtilities(u_core):
    """Oracle WMS utilities extending FlextUtilities with domain-specific helpers.

    Architecture: Extends FlextUtilities with Oracle WMS-specific operations.
    Uses composition and delegation to maximize reuse of base utilities.
    """


u = FlextOracleWmsUtilities

__all__ = [
    "FlextOracleWmsUtilities",
    "u",
]
