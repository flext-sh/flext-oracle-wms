"""Models for Oracle WMS operations.

This module provides data models for Oracle WMS operations.
"""

from __future__ import annotations

from flext_core import FlextModels


class FlextOracleWmsModels(FlextModels):
    """Models for Oracle WMS operations.

    Extends FlextModels to avoid duplication and ensure consistency.
    All Oracle WMS models benefit from FlextModels patterns.
    """

    WmsRecord = dict["str", "object"]
    WmsRecords = list[WmsRecord]
