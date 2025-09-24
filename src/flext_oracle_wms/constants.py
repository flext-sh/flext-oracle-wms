"""FLEXT Oracle WMS Constants - Oracle WMS integration constants.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import ClassVar

from flext_core import FlextConstants


class FlextOracleWmsConstants(FlextConstants):
    """Oracle WMS integration-specific constants following flext-core patterns."""

    # Oracle WMS API Configuration
    DEFAULT_WMS_TIMEOUT = 30
    DEFAULT_MAX_RETRIES = 3
    DEFAULT_RETRY_DELAY = 1

    # WMS Entity Types
    WMS_ENTITY_TYPES: ClassVar[list[str]] = [
        "INVENTORY",
        "SHIPMENT",
        "PICKING",
        "RECEIVING",
        "WAREHOUSE",
    ]

    # WMS Operation Configuration
    DEFAULT_BATCH_SIZE = 1000
    MAX_BATCH_SIZE = 10000
    DEFAULT_PAGE_SIZE = 100


__all__ = ["FlextOracleWmsConstants"]
