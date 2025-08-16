"""Compatibility models module mapping to wms_models.

Re-exports domain models for tests that import flext_oracle_wms.models directly.
"""

from __future__ import annotations

# Re-export all domain models from wms_models
from flext_oracle_wms.wms_models import *  # noqa: F403

# NOTE: Legacy compatibility layer removed - all models now use modern Pydantic patterns from wms_models.py
