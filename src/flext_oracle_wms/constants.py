"""FLEXT Oracle WMS Constants - Oracle WMS integration constants.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import ClassVar

from flext_core import FlextConstants


class FlextOracleWmsConstants(FlextConstants):
    """Oracle WMS integration-specific constants following FLEXT unified pattern with nested domains."""

    class Connection:
        """Oracle WMS connection and API configuration constants."""

        DEFAULT_TIMEOUT = FlextConstants.Network.DEFAULT_TIMEOUT
        DEFAULT_MAX_RETRIES = FlextConstants.Reliability.MAX_RETRY_ATTEMPTS
        DEFAULT_RETRY_DELAY = FlextConstants.Reliability.RETRY_DELAY_SECONDS

    class Entities:
        """Oracle WMS entity types and definitions."""

        TYPES: ClassVar[list[str]] = [
            "INVENTORY",
            "SHIPMENT",
            "PICKING",
            "RECEIVING",
            "WAREHOUSE",
        ]

    class Processing:
        """Oracle WMS data processing configuration constants."""

        DEFAULT_BATCH_SIZE = FlextConstants.Performance.BatchProcessing.DEFAULT_SIZE
        MAX_BATCH_SIZE = FlextConstants.Performance.BatchProcessing.MAX_ITEMS
        DEFAULT_PAGE_SIZE = FlextConstants.Performance.Pagination.DEFAULT_PAGE_SIZE


__all__ = ["FlextOracleWmsConstants"]
