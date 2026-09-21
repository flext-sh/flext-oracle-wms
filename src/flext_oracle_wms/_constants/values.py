"""Scalar constants for flext-oracle-wms.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import ClassVar, Final

from flext_api import c


class FlextOracleWmsConstantsValues:
    """Scalar constants mixed into ``c.OracleWms`` and ``FlextOracleWmsConfig``."""

    class OracleWms:
        """WMS connection scalar constants - composed from base."""

        FLEXT_WMS_VERSION: Final[str] = "1.0.0"
        HTTP_BAD_REQUEST_THRESHOLD: Final[int] = 400

        class WmsEntities:
            """WMS entity configuration - patterns."""

            MAX_ENTITY_NAME_LENGTH: ClassVar[int] = 100

        class WmsProcessing:
            """WMS processing constants - domain-specific."""

            DEFAULT_BATCH_SIZE: Final[int] = c.DEFAULT_SIZE
            MAX_BATCH_SIZE: Final[int] = c.MAX_ITEMS

        class Filtering:
            """Filtering constants - minimal declaration."""

            MAX_FILTER_CONDITIONS: ClassVar[int] = 50

    class Config:
        """Config-class scalar constants mixed into ``FlextOracleWmsConfig``."""

        CONFIG_DIR: ClassVar[str] = c.CONFIG_DIR_NAME


__all__: list[str] = ["FlextOracleWmsConstantsValues"]
