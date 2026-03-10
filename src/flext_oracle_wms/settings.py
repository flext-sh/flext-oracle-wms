"""FLEXT WMS Configuration - Generic WMS integration with composition.

Uses Python 3.13+ syntax, reduces declarations through patterns.
One class per module following SOLID principles. Generic WMS configuration.
Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextSettings
from pydantic import ConfigDict, Field


class FlextOracleWmsSettings(FlextSettings):
    """Runtime settings for Oracle WMS client."""

    model_config = ConfigDict(extra="ignore")

    base_url: str = Field(default="http://localhost:8080", min_length=1)
    timeout: float = Field(default=30.0, ge=1.0, le=300.0)

    @classmethod
    def testing_config(cls) -> FlextOracleWmsSettings:
        """Build deterministic settings for tests."""
        return cls(base_url="http://localhost:8080", timeout=30.0)


__all__ = ["FlextOracleWmsSettings"]
