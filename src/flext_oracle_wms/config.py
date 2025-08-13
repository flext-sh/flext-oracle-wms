"""Backward-compatibility config shim.

Historically, tests imported config from `flext_oracle_wms.config`.
This module re-exports the modern config from `wms_config`.
"""
from __future__ import annotations

from .wms_config import FlextOracleWmsModuleConfig  # re-export

__all__ = ["FlextOracleWmsModuleConfig"]
