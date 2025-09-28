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

        MAX_ENTITY_NAME_LENGTH: ClassVar[int] = 100
        ENTITY_NAME_PATTERN: ClassVar[str] = r"^[a-zA-Z][a-zA-Z0-9_]*$"

    class Processing:
        """Oracle WMS data processing configuration constants."""

        DEFAULT_BATCH_SIZE = FlextConstants.Performance.BatchProcessing.DEFAULT_SIZE
        MAX_BATCH_SIZE = FlextConstants.Performance.BatchProcessing.MAX_ITEMS
        DEFAULT_PAGE_SIZE = FlextConstants.Performance.Pagination.DEFAULT_PAGE_SIZE
        MAX_SCHEMA_DEPTH: ClassVar[int] = 10

    class Filtering:
        """Oracle WMS filtering configuration constants."""

        MAX_FILTER_CONDITIONS: ClassVar[int] = 50

    class ErrorMessages:
        """Oracle WMS error message constants."""

        ENTITY_VALIDATION_FAILED: ClassVar[str] = "Entity validation failed"
        DISCOVERY_FAILED: ClassVar[str] = "Entity discovery failed"
        INVALID_RESPONSE: ClassVar[str] = "Invalid API response"

    class ResponseFields:
        """Oracle WMS API response field constants."""

        RESULT_COUNT: ClassVar[str] = "result_count"
        RESULTS: ClassVar[str] = "results"
        TOTAL_COUNT: ClassVar[str] = "total_count"

    class Authentication:
        """Oracle WMS authentication constants."""

        MIN_TOKEN_LENGTH: ClassVar[int] = 10
        MIN_API_KEY_LENGTH: ClassVar[int] = 20

    class Pagination:
        """Oracle WMS pagination constants."""

        DEFAULT_PAGE_SIZE: ClassVar[int] = 100

    # Default environment
    DEFAULT_ENVIRONMENT: ClassVar[str] = "default"


__all__ = ["FlextOracleWmsConstants"]
