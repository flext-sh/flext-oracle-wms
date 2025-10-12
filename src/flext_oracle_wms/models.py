"""Models for Oracle WMS operations.

This module provides data models for Oracle WMS operations.
"""

from __future__ import annotations

from flext_core import FlextCore


class FlextOracleWmsModels(FlextCore.Models):
    """Models for Oracle WMS operations.

    Extends FlextCore.Models to avoid duplication and ensure consistency.
    All Oracle WMS models benefit from FlextCore.Models patterns.
    """

    WmsRecord = FlextCore.Types.Dict
    WmsRecords = list[WmsRecord]
