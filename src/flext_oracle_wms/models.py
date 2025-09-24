"""Models for Oracle WMS operations.

This module provides data models for Oracle WMS operations.
"""

from flext_core import FlextModels


class FlextOracleWmsModels:
    """Models for Oracle WMS operations."""

    Core = FlextModels

    WmsRecord = dict[str, object]
    WmsRecords = list[WmsRecord]
