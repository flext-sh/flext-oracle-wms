"""Backward-compatibility exceptions shim.

Provides `flext_oracle_wms.exceptions` import path by re-exporting the
exception classes from the consolidated exceptions module.
"""
from __future__ import annotations

from .wms_exceptions import *  # noqa: F401,F403 - re-export full hierarchy intentionally
